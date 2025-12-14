from common import convert_ig_graph_to_modgraph
from gmltools.modimport import mod
from gmltools.ruletest import RuleTest
from math import inf


class SpecialRuleTest(RuleTest):
    def __init__(self, compounds, reactions):
        self.compounds = {i: convert_ig_graph_to_modgraph(j) for i, j in compounds.items()}
        self.educts, self.products = self.partition_reactants(reactions)
        self.cofactors = []
        self.cofactor_ids = {}

    @staticmethod
    def partition_reactants(reactions):
        educts = set()
        products = set()
        for reaction in reactions:
            educts.update(reaction['educts'])
            products.update(reaction['products'])
        return educts, products


class StandardOptimizer:
    def __init__(self, rule_test):
        self.rule_test = rule_test
        self.optimal_metric = inf
        self.optimal_size = inf
        self.optimal_states = []

    def evaluate_state(self, state):
        rules = [
            mod.ruleGMLString(sub_state.get_gml_rule())
            for sub_state in state
        ]
        metrics = self.rule_test.test_set_of_rules(rules)
        total_surplus = 0
        for individual_result in metrics['individual']:
            total_surplus += individual_result['educt_surplus']
            total_surplus += individual_result['product_surplus']

        state_size = len(state)
        expand = False
        if total_surplus < self.optimal_metric or (
                total_surplus == self.optimal_metric and state_size < self.optimal_size):
            self.optimal_states = [state]
            self.optimal_size = state_size
            self.optimal_metric = total_surplus
            expand = True
        elif total_surplus == self.optimal_metric and state_size == self.optimal_size:
            self.optimal_states.append(state)
            expand = True
        elif state_size < self.optimal_size:
            expand = True

        return expand

    def get_optimal_states(self):
        return self.optimal_states
