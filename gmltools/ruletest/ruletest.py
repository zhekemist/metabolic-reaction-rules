# --- IMPORTS ---
import itertools
import json
import os
import sys
import logging

from ..modimport import mod

# --- DEFINITIONS ---

stdout_fd = sys.stdout.fileno()
old_stdout = os.dup(stdout_fd)


def redirect_stdout(): # to prevent MØÐ from flooding the terminal with warnings about stereochemistry
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, stdout_fd)
    os.close(devnull)


def restore_stdout():
    os.dup2(old_stdout, stdout_fd)


class RuleTest:
    LABEL_SETTINGS = mod.LabelSettings(mod.LabelType.Term, mod.LabelRelation.Unification)

    def __init__(self, reactions_path, compounds_path, ec_class, config_path=None):
        if config_path:
            with open(config_path, 'r') as file:
                config = json.load(file)
        else:
            config = {'cofactors': [], 'cofactor_ids': []}

        cofactor_ids = set(config['cofactor_ids'])  # cofactor ids respective to the compound data

        redirect_stdout()
        self.cofactors = [mod.graphDFS(i, i) for i in config['cofactors']]
        self.cofactor_ids = set(config['cofactors'])  # cofactors ids respective to the just created graphs
        self.load_compounds(compounds_path, cofactor_ids)
        self.load_reactions(reactions_path, ec_class, cofactor_ids)
        restore_stdout()

        logging.debug(f'{len(self.compounds)} compounds loaded.')

    def load_compounds(self, data_path, cofactor_ids):
        with open(data_path, 'r') as file:
            compound_data = json.load(file)

        compounds = {}
        for compound in compound_data:
            cid = compound['id']
            if cid in cofactor_ids:  # do not load cofactors, as they will be added as customized structures later
                continue
            if 'smiles' in compound:
                compounds[cid] = mod.Graph.fromSMILES(compound['smiles'], cid)
            elif 'graphDFS' in compound:
                compounds[cid] = mod.Graph.fromDFS(compound['graphDFS'], cid)
        self.compounds = compounds

    def load_reactions(self, data_path, ec_class, cofactor_ids):
        with open(data_path, 'r') as file:
            reaction_data = json.load(file)

        # these two sets will represent the compounds, which occur in these positions in the reference data
        self.educts = set()
        self.products = set()

        for reaction in reaction_data:
            if any(i.startswith(ec_class) for i in reaction['ec']):
                for side in ['rhs', 'lhs']:
                    other_side = 'rhs' if side == 'lhs' else 'lhs'
                    if reaction['to_' + side]:
                        # add reactants to the respective sets
                        self.educts.update(i['id']
                                           for i in reaction['equation_decomposed'][other_side]
                                           if i['id'] not in cofactor_ids)
                        self.products.update(i['id']
                                             for i in reaction['equation_decomposed'][side]
                                             if i['id'] not in cofactor_ids)

    def test_set_of_rules(self, rules):
        """
        this is the method, which should be called for testing, when using this class;
        rules should be a list of MØD graph rewrite rule objects
        """
        results = {}
        total_products = set()
        total_candidates = set()
        for rule in rules:
            candidates, products, result = self.test_rule(rule)
            results[rule.name] = result
            total_candidates |= candidates
            total_products |= products
        results = {
            'total': {
                'educt_missing': self.educts - total_candidates,
                'product_missing': self.products - total_products
            },
            'individual': results
        }
        return results

    def test_rule(self, rule):
        educt_candidates = self.get_candidates(rule)
        educt_surplus = educt_candidates - self.educts
        educts = [self.compounds[cid] for cid in (educt_candidates & self.educts)]
        # this strangely seem to reduce the occurrence of MØD's performance bug
        educts = sorted(educts, key=lambda g: (g.numVertices, g.name))
        logging.debug(f"{len(educts)} Educts from {len(self.educts)} found.")

        strategy = (mod.addUniverse(self.cofactors) >> mod.addSubset(educts) >> rule)
        derivation = mod.DG(labelSettings=RuleTest.LABEL_SETTINGS,
                            graphDatabase=itertools.chain(self.cofactors, self.compounds.values()))
        logging.debug("Started derivation.")
        with derivation.build() as dg:
            dg.execute(strategy)
        logging.debug("Finished derivation.")
        products = {vertex.graph.name if not vertex.graph.name.startswith("p")
                    else f'graphDFS:{vertex.graph.graphDFS}'
                    for vertex in derivation.vertices if (vertex.inDegree > 0)}
        products -= self.cofactor_ids
        product_surplus = products - self.products

        logging.debug("Finished testing.")

        return educt_candidates, products, {
            'educt_surplus': educt_surplus,
            'product_surplus': product_surplus
        }

    def get_candidates(self, rule):
        candidates = set()
        educts = RuleTest.extract_educts(rule)
        for cid, compound in self.compounds.items():
            for educt in educts:
                if educt.monomorphism(compound, labelSettings=RuleTest.LABEL_SETTINGS) > 0:
                    candidates.add(cid)
                    break
        return candidates

    @staticmethod
    def extract_educts(rule):
        # split the left side of the rule into its individual connected components
        gmlrule = "graph ["
        for vertex in rule.left.vertices:
            gmlrule += f'node [ id {vertex.id} label "{vertex.stringLabel}" ] '
        for edge in rule.left.edges:
            gmlrule += f'edge [ source {edge.source.id} target {edge.target.id} label "{edge.stringLabel}" ] '
        gmlrule += "]"
        graphs = mod.Graph.fromGMLStringMulti(gmlrule)
        return graphs
