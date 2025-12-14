import itertools

from common import *


def labels_to_colors(graph_one, graph_two):
    # TODO: consider removing
    vertex_color_map = {}
    vertex_counter = itertools.count(0)
    edge_color_map = {}
    edge_counter = itertools.count(0)
    for graph in [graph_one, graph_two]:
        for label in graph.vs['label']:
            if label not in vertex_color_map:
                vertex_color_map[label] = next(vertex_counter)
        for label in graph.es['label']:
            if label not in edge_color_map:
                edge_color_map[label] = next(edge_counter)
    vertex_colors = []
    edge_colors = []
    for graph in [graph_one, graph_two]:
        vertex_colors.append([
            vertex_color_map[i] for i in graph.vs['label']
        ])
        edge_colors.append([
            edge_color_map[i] for i in graph.es['label']
        ])
    return {'color1': vertex_colors[0], 'color2': vertex_colors[1],
            'edge_color1': edge_colors[0], 'edge_color2': edge_colors[1]}


def extract_components(rule_object, right=False):
    total_graph = convert_modgraph_to_ig_graph(rule_object.left if not right else rule_object.right)
    total_graph.vs['is_variable'] = [label.startswith("_") for label in total_graph.vs['label']]
    educt_graphs = [
        educt for educt in total_graph.connected_components().subgraphs()
    ]
    return educt_graphs


def node_compat(large_graph, small_graph, large_vertex, small_vertex):
    big_label = large_graph.vs[large_vertex]['label']
    small_label = small_graph.vs[small_vertex]['label']
    return small_label.startswith('_') or (big_label == small_label)


def edge_compat(large_graph, small_graph, large_edge, small_edge):
    return large_graph.es[large_edge]['label'] == small_graph.es[small_edge]['label']


# --- MATCHING ---

class ReactionMatcher:
    # TODO: *-Variables support
    def __init__(self, gml_rule, compounds):
        rule_object = mod.ruleGMLString(gml_rule)
        self.compounds = compounds
        self.components = {
            'educts': extract_components(rule_object),
            'products': extract_components(rule_object, right=True)
        }
        self.free_name = self.name_products()

    def name_products(self):
        # -- NAMING ---
        next_free = itertools.count(0)
        for graph in self.components['products']:
            graph.vs['name'] = [
                str(next(next_free)) if not vertex['is_variable'] else vertex['label']
                for vertex in graph.vs
            ]
        return next(next_free)

    def match(self, reaction):
        # -- EDUCT MATCH --
        matches = []
        for educt_pattern in self.components['educts']:
            pattern_matches = []
            for educt_id in reaction['educts']:
                educt = self.compounds[educt_id]
                pattern_matches += [(educt_id, match) for match in educt.get_subisomorphisms_vf2(
                    educt_pattern,
                    node_compat_fn=node_compat, edge_compat_fn=edge_compat)]
            matches.append(pattern_matches)
        possible_bindings = list(itertools.product(*matches))

        # -- GLUING AND CHECKING --
        next_id = itertools.count(0)
        products = []
        for product in reaction['products']:
            product = self.compounds[product].copy()
            product.vs['name'] = [next(next_id) for _ in range(0, len(product.vs))]
            products.append(product)
        target_product_graph = ig.union(products, byname=True)
        fitting_bindings = []
        for binding in possible_bindings:
            generated_product_graph = self.glue_graphs(binding)
            if target_product_graph.isomorphic_vf2(generated_product_graph,
                                                   **labels_to_colors(target_product_graph, generated_product_graph)):
                fitting_bindings.append(binding)
        return fitting_bindings

    def glue_graphs(self, binding):
        next_free = itertools.count(self.free_name)
        graphs_to_glue = []
        for educt_pattern, (educt, match) in zip(self.components['educts'], binding):
            educt = self.compounds[educt].copy()
            variables = {match[vertex.index]: vertex['label'] for vertex in educt_pattern.vs(is_variable=True)}
            educt.vs['name'] = [
                str(next(next_free)) if vertex.index not in variables else variables[vertex.index]
                for vertex in educt.vs
            ]
            educt.delete_vertices([index for index in match if index not in variables])
            graphs_to_glue.append(educt)
        graphs_to_glue += list(self.components['products'])
        glued_graph = ig.union(graphs_to_glue, byname=True)
        new_labels = []
        for x in zip(*(glued_graph.vs['label_' + str(x)] for x in range(1, len(graphs_to_glue) + 1))):
            new_labels.append(next(label for label in x if label is not None and not label.startswith('_')))
        glued_graph.vs['label'] = new_labels
        return glued_graph

    def bind_graphs(self, binding):
        bound_graphs = []
        for educt_pattern, (educt, match) in zip(self.components['educts'], binding):
            educt = educt.copy()
            for pattern_node, educt_node in enumerate(match):
                pattern_node = educt_pattern.vs[pattern_node]
                educt_node = educt.vs[educt_node]
                educt_node['id_in_rule'] = pattern_node['old_id']
                educt_node['is_variable'] = pattern_node['is_variable']
            bound_graphs.append(educt)
        return bound_graphs
