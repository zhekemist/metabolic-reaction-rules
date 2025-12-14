# ---- IMPORTS ----

import argparse
import itertools
import os
import re
from dataclasses import dataclass

from gmltools.modimport import mod


# ---- HELPER CLASSES ----

@dataclass(slots=True, frozen=True)
class Group:
    label: str  # corresponds to "{<group-symbol>}"
    link_id: int
    link_label: str
    gml_string: str  # GML graph definition after the header
    ids: list[int]  # ids of the contained nodes
    variables: set[str]  # contained first-order variables

    @staticmethod
    def from_gml(gml_head, gml_body):
        """
        gml_head: header part of the group definition, e.g. {Group:Et:0}
        gml_body: graph GML of the group
        """
        mod.Graph.fromGMLString(gml_body)  # TODO: move validation to compiler
        gml_body = gml_body[gml_body.find("[") + 1:gml_body.rfind("]")]
        gml_head = gml_head.split(":")

        label = "{" + gml_head[1] + "}"
        link_id = int(gml_head[2][:-1])
        link_label = re.search(rf'node\s*\[\s*id\s+{link_id}\s+label\s+"(\w+)"\s*]', gml_body)
        if not link_label:
            raise RuntimeError(f"Link node not found in group {gml_head}")
        link_label = link_label.group(1)
        ids = [int(x) for x in re.findall(r'id\s+(\d+)', gml_body)]
        variables = set(re.findall(r'label "\s*(_\w+)\s*"', gml_body))
        return Group(label, link_id, link_label, gml_body, ids, variables)


@dataclass(slots=True, frozen=True)
class Template:
    gml_template: str
    constraints: dict[str, list[str | list[str] | None]]

    # constraints stores the information extracted from constrainLabelAny elements as follows:
    # key: first-order variable
    # value: options for the variable:
    #   [None] = variable is unconstrained
    #   ["{Et}", "{Me}", ["H", "O"]] = options for the variable were "{Et}", "{Me}", "H" and "O"
    #     => all the non-group options are seen as a single one

    def __getattr__(self, name):
        if name == "variables":
            return set(re.findall(rf'node\s*\[\s*id\s+\d+\s+label\s+"\s*(_\w+)\s*"\s*]', self.gml_template))
        elif name == "vacant_id":
            ids = [int(x) for x in re.findall(r'id\s+(\w+)', self.gml_template)]
            return max(ids) + 1
        else:
            raise AttributeError(f"Template has no attribute {name}.")

    @staticmethod
    def from_gml(gml_body):
        gml_body, constraints = Template.extract_constraints(gml_body)
        return Template(gml_body, constraints)

    @staticmethod
    def extract_constraints(gml_string):
        pattern = re.compile(
            r'constrainLabelAny\s+\[\s*(label\s*"\w*")\s*labels\s*\[(\s*(?:label\s*"(\w|{|})*"|\s*)+)]\s*]',
            re.DOTALL
        )
        matches = pattern.finditer(gml_string)
        constraints = {match.group(1).split('"')[1]: match.group(2).split('"')[1::2] for match in matches}
        gml_string = re.sub(pattern, '', gml_string)  # delete all constraints from the GML string
        constraints = {target: [[x for x in labels if "{" not in x]] + [x for x in labels if "{" in x]
                       for target, labels in constraints.items()}
        constraints.update({x: [None] for x in
                            re.findall(rf'node\s*\[\s*id\s+\d+\s+label\s+"\s*(_\w+)\s*"\s*]', gml_string)
                            if x not in constraints})
        return gml_string, constraints


class Derivation:  # = one step in the process of recursively substituting group symbols
    __slots__ = "compiler", "gml_string", "unresolved_vars", "mangling_map", "map_changed"

    def __init__(self, compiler, gml_string, unresolved_vars, mangling_map):
        self.compiler = compiler
        self.gml_string = gml_string  # current GML string of the reaction rule
        # first-order variables, where not at all group options from the constraints were already substituted
        self.unresolved_vars = unresolved_vars
        self.mangling_map = mangling_map  # map keeping track of what unique number to append to the var next
        self.map_changed = False  # for the "copy-on-write" functionality

    def is_resolved(self):
        return not self.unresolved_vars

    def derive(self):  # conduct the next recursive steps
        constraints = {x: y for x, y in self.compiler.template.constraints.items()
                       if x in self.unresolved_vars}
        self.unresolved_vars.clear()
        for substitution in Derivation.generate_substitutions(constraints):
            yield self.apply(substitution)

    def apply(self, substitution):
        result = Derivation(self.compiler, self.gml_string, self.unresolved_vars.copy(), self.mangling_map)
        for var, term in substitution.items():
            if isinstance(term, list):  # term is a list of vanilla options
                result.insert_constraint(var, term)
            elif isinstance(term, str):  # term is a group symbol
                result.gml_string = re.sub(rf'(node\s*\[\s*id\s+\d+\s+label\s+"){var}("\s*])',
                                           rf'\1{term}\2',
                                           result.gml_string)
            elif term is None:  # variable is unconstrained
                result.gml_string = re.sub(rf'(node\s*\[\s*id\s+\d+\s+label\s+"){var}("\s*])',
                                           rf'\1{result.mangle_var(var)}\2',
                                           result.gml_string)
            # result.unresolved_vars.remove(var)
        result.expand_template_terms()
        return result

    def insert_constraint(self, var, terms):
        # insert a vanilla GML constraint, which does not require further attention, i.e. not options are group symbols
        constraint_template = 'constrainLabelAny [ label "{}" labels [{}]]'
        labels_str = " ".join(f'label "{term}"' for term in terms)
        mangled_var = self.mangle_var(var)
        self.gml_string = re.sub(rf'label\s+"{var}"', f'label "{mangled_var}"', self.gml_string)
        constraint_str = constraint_template.format(mangled_var, labels_str)
        ins_pt = self.gml_string.find("[") + 1
        self.gml_string = self.gml_string[:ins_pt] + constraint_str + self.gml_string[ins_pt:]

    def expand_template_terms(self):  # find group symbols in the rule and substitute them with their graph
        target_pattern = r'node\s*\[\s*id\s+(\d+)\s+label\s+"({\w+})"\s*\]'
        while True:
            targets = re.findall(target_pattern, self.gml_string)
            if not targets:
                return
            for target_id, group_label in targets:
                self.insert_group(target_id, group_label)

    def insert_group(self, target_id, group_label):
        """
        substitutes the node with target_id with the graph of the group with the label group_label
        """
        group = self.compiler.groups[group_label]

        # remap node ids in the group graph to avoid conflicts with already existing ids
        id_mapping = {x: next(self.compiler.vacant_id) for x in group.ids}
        # apply remapping to the GML string of the group
        group_str = re.sub(r'(id|source|target)\s+(\d+)(\s+|])',
                           lambda m: rf"{m.group(1)} {id_mapping[int(m.group(2))]}{m.group(3)}",
                           group.gml_string)
        ins_pt = self.gml_string.find("[", self.gml_string.find("context")) + 1
        self.gml_string = self.gml_string[:ins_pt] + group_str + self.gml_string[ins_pt:]
        link_id = id_mapping[group.link_id]
        self.gml_string = re.sub(rf'node\s*\[\s*id\s+{target_id}\s+label\s+"' r'{\w+}"\s*]',
                                 '',
                                 self.gml_string)
        # replace references to the substituted node with ones to the inserted link node
        self.gml_string = re.sub(rf'(id|source|target)\s+{target_id}(\s+|])',
                                 rf'\1 {link_id} \2',
                                 self.gml_string)
        self.unresolved_vars |= group.variables

    def mangle_var(self, var):
        if var not in self.mangling_map:
            if not self.map_changed:
                self.map_changed = True
                self.mangling_map = self.mangling_map.copy()
            self.mangling_map[var] = 0
        else:
            self.mangling_map[var] += 1
        return f"{var}_{self.mangling_map[var]}"

    def unmangle_var(self, var):
        if var in self.mangling_map:
            var = var[:var.rfind("_")]
        return var

    @staticmethod
    def generate_substitutions(constraints):
        # substitution = binding every first-order variable to one of its options
        # this function generates every possible substitution by using the "cartesian product" between
        # the options of the different variables
        substitutions = ({y: combination[x] for x, y in enumerate(constraints)}
                         for combination in itertools.product(*constraints.values()))
        substitutions = filter(lambda el: not any(len(x) == 0 for x in el.values() if isinstance(x, list)),
                               substitutions)
        return substitutions


class TemplateCompiler:
    __slots__ = "template", "groups", "vacant_id"

    def __init__(self, template, groups):
        self.template = template
        self.groups = groups
        self.vacant_id = itertools.count(template.vacant_id)  # next id not conflicting with any existing node ids

    def derive_rules(self):
        init_derivation = Derivation(self, self.template.gml_template, self.template.variables, {})
        new_derivations = [init_derivation]
        result_rules = []
        while incomplete_derivations := new_derivations:
            new_derivations = []
            for derivation in incomplete_derivations:
                for new_derivation in derivation.derive():
                    if new_derivation.is_resolved():
                        # loading the derived rule into an MØD object as a safeguard
                        result_rules.append(mod.ruleGMLString(new_derivation.gml_string))
                    else:
                        new_derivations.append(new_derivation)
        return result_rules

    @staticmethod
    def compile_file(file_path, out_dir, group_file_path=None):
        """
        reads template from file_path, optionally appending external group definitions
        and writes the resulting rules out
        """
        with open(file_path, "r") as file:
            string = file.read()
        if group_file_path:
            with open(group_file_path, "r") as file:
                string += file.read()
        rules = TemplateCompiler.compile_string(string)
        if not os.path.exists(out_dir):
            os.makedirs(f"./{out_dir}")
        file_prefix = os.path.join(out_dir, os.path.split(file_path)[1].split(".")[0])
        for nr, rule in enumerate(rules):
            with open(rf"{file_prefix}_{nr}.gml", "w") as file:
                file.write(rule.getGMLString())

    @staticmethod
    def compile_string(string):
        """
        compiles a GML template string and returns the result vanilla GML rules
        as MØD rewrite rule objects for direct further usage
        """
        template_str, group_strs = TemplateCompiler.parse_string(string)
        template = Template.from_gml(template_str)
        groups = [Group.from_gml(x[0], x[1]) for x in group_strs]
        groups = {x.label: x for x in groups}
        compiler = TemplateCompiler(template, groups)
        return compiler.derive_rules()

    @staticmethod
    def parse_string(string):
        keywords = re.finditer(r'({(?:\w|:)+})((?:"{\w*}"|[^{])+)', string, flags=re.DOTALL)
        template_match = None
        group_matches = []
        for match in keywords:
            match_head = match.group(1)
            if match_head == "{Template}":
                if template_match is not None:
                    raise RuntimeError("Can't have two template rules.")
                template_match = match
            elif re.match(r"{Group:\w+:\d+}", match_head) is not None:
                group_matches.append(match)
            else:
                raise RuntimeError(f"Unexpected Keyword: {match_head}")

        if template_match and group_matches:
            template_str = template_match.group(2)
            group_strs = [(x.group(1), x.group(2)) for x in group_matches]
        else:
            raise RuntimeError(f"No Template or Group found.")
        return template_str, group_strs


# ---- FRONT END ---

def run():
    parser = argparse.ArgumentParser(prog="GML Template Compiler",
                                     description="Simple compiler to transform GML templates into vanilla GML rules.")
    parser.add_argument("-t", "--template",
                        action="append",
                        required=True,
                        type=str,
                        metavar="path/to/template.gml",
                        help="multiple paths are accepted")
    parser.add_argument("-o", "--out-dir",
                        default="./compiler_out",
                        dest="out_dir",
                        type=str,
                        metavar="output directory"
                        )
    parser.add_argument("-g", "--groups-file",
                        type=str,
                        metavar="path/to/groups/file.gml",
                        help="file with more group definitions"
                        )
    args = parser.parse_args()
    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)
    if not args.groups_file:
        for dir_path, _, files in os.walk("."):
            if "groups.gml" in files:
                args.groups_file = os.path.join(dir_path, "groups.gml")
                break
    for path in args.template:
        TemplateCompiler.compile_file(path, args.out_dir, args.groups_file)


if __name__ == "__main__":
    run()
