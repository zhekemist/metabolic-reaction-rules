# --- IMPORTS ---
import glob
import itertools
from collections import deque

import mod

from gmltools.specialization.dataloading import DataLoader
from gmltools.specialization.metrics import SpecialRuleTest, StandardOptimizer
from mcs import find_mcs_of_set, merge_mcs_with_rule, get_environments, partition_environments
from reactionmatching import ReactionMatcher


# --- MAIN PART ---

class SubState:

    def __init__(self, gml_rule, graph_ids, graphs, mcses):
        self.gml_rule = gml_rule
        self.graph_ids = graph_ids
        self.graphs = graphs
        self.mcses = mcses

    @staticmethod
    def from_start_data(gml_rule, graph_ids, graphs):
        mcses = [find_mcs_of_set(i) for i in graphs]
        graph_ids, graphs = zip(*sorted(zip(graph_ids, graphs), key=lambda x: x[0]))
        return SubState(gml_rule, tuple(graph_ids), list(graphs), mcses)

    def __hash__(self):
        return hash((self.gml_rule, self.graph_ids))

    def get_successors(self):
        # calc different split => return list of lists of substates
        successors = []
        for pos, (ids_per_comp, graphs_per_comp, mcs_per_comp) in enumerate(
                zip(self.graph_ids, self.graphs, self.mcses)):
            environments = [
                get_environments(mcs_per_comp, graph) for graph in graphs_per_comp
            ]
            groups = partition_environments(environments)
            new_sub_states = []
            for group in groups:
                graph_ids = [ids_per_comp[i] for i in group]
                graphs = [graphs_per_comp[i] for i in group]
                graph_ids, graphs = zip(*sorted(zip(graph_ids, graphs), key=lambda x: x[0]))
                mcs = find_mcs_of_set(graphs)
                new_sub_state = SubState(self.gml_rule, list(self.graph_ids), self.graphs.copy(), self.mcses.copy())
                new_sub_state.graph_ids[pos] = tuple(graph_ids)
                new_sub_state.graph_ids = tuple(new_sub_state.graph_ids)
                new_sub_state.graphs[pos] = graphs
                new_sub_state.mcses[pos] = mcs
                new_sub_states.append(new_sub_state)
            successors.append(new_sub_states)
        return successors

    def get_gml_rule(self):
        gml_rule = self.gml_rule
        for mcs in self.mcses:
            gml_rule = merge_mcs_with_rule(gml_rule, mcs)
        return gml_rule


class SpecializationSearcher:
    def __init__(self, optimizer, gml_rules, data):
        self.optimizer = optimizer
        self.start_state = self.prepare_search(gml_rules, data.compounds, data.reactions)

    @staticmethod
    def prepare_search(gml_rules, compounds, reactions):
        next_id = itertools.count(0)
        first_state = []
        for gml_rule in gml_rules:
            matcher = ReactionMatcher(gml_rule, compounds)
            possible_graph_ids = [[] for _ in range(0, len(matcher.components['educts']))]
            possible_graphs = [[] for _ in range(0, len(matcher.components['educts']))]
            for reaction in reactions:
                possible_bindings = matcher.match(reaction)
                for binding in possible_bindings:
                    bound_graphs = matcher.bind_graphs(binding)
                    for i, bound_graph in enumerate(bound_graphs):
                        bg_id = next(next_id)
                        bound_graph['id'] = bg_id
                        possible_graph_ids[i].append(bg_id)
                        possible_graphs[i].append(bound_graph)
            first_state.append(
                SubState.from_start_data(gml_rule, possible_graph_ids, possible_graphs)
            )
        return tuple(sorted(first_state, key=lambda x: hash(x)))

    def run_search(self):
        visited_states = set()
        next_states = deque()
        next_states.append(self.start_state)
        while next_states:
            current_state = next_states.popleft()
            if current_state in visited_states:
                continue
            visited_states.add(current_state)
            expand = self.optimizer.evaluate_state(current_state)
            if expand:
                successors = self.get_successors(current_state)
                deque.extendleft(successors)
        result = [
            [sub_state.get_gml_rule() for sub_state in state]
            for state in self.optimizer.get_optimal_states()
        ]
        return result

    @staticmethod
    def get_successors(state):
        successor_states = []
        for pos, sub_state in enumerate(state):
            for new_sub_states in sub_state.get_successors():
                new_state = list(state)
                del new_state[pos]
                new_state += new_sub_states
                successor_states.append(tuple(sorted(new_state, key=lambda x: hash(x))))
        return successor_states


# --- LIVE TEST ---

rule_files = glob.glob('data/rules/1_1_1_*.gml')
gml_rules = [mod.ruleGML(path).getGMLString() for path in rule_files]
data = DataLoader('data/iAF1260b_reacs.json', 'data/iAF1260b_chems.json', '1.1.1', 'data/test_config.json')
rule_test = SpecialRuleTest(data.compounds, data.reactions)
optimizer = StandardOptimizer(rule_test)
specializer = SpecializationSearcher(optimizer, gml_rules, data)
result = specializer.run_search()
print(result)
