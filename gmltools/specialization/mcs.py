import itertools
import re
from collections import deque

import igraph as ig


def partition_edges(graph):
    start_edges = []
    # incident_edges = []
    other_edges = []
    for edge in graph.es:
        if edge.source_vertex['id_in_rule'] and edge.target_vertex['id_in_rule']:
            start_edges.append((edge.source_vertex['id_in_rule'], edge.source_vertex))
        # elif edge.source_vertex['id_in_rule'] or edge.target_vertex['id_in_rule']:
        #    incident_edges.append(edge)
        else:
            other_edges.append(edge)
    start_edges = [x[1] for x in sorted(start_edges, key=lambda x: x[0])]
    # return start_edges, incident_edges, other_edges
    return start_edges, other_edges


def get_edge_info(edges):
    edge_types = {}
    edge_incidences = {}
    for edge in edges:
        edge_type = (tuple(sorted([edge.source_vertex['label'], edge.target_vertex['label']])), edge['label'])
        if not edge_types[edge_type]:
            edge_types[edge_type] = []
        edge_types[edge_type].append(edge)
        edge_incidences[edge.index] = {}
        for node in edge.vertex_tuple:
            for inner_edge in node.all_edges:
                if inner_edge == edge:
                    continue
                edge_incidences[edge.index][inner_edge.index] = node['label']
    return edge_types, edge_incidences


def generate_compat_graph(graph_one, graph_two):
    compat_nodes = []
    compat_edges = []
    c_edges = []

    edges_one = partition_edges(graph_one)
    edges_two = partition_edges(graph_two)

    # starting graph
    edges = {}
    for i, (edge_one, edge_two) in enumerate(zip(edges_one[0], edges_two[0])):
        compat_nodes.append((edge_one, edge_two))
        for j, existing_node in enumerate(compat_nodes):
            compat_edges.append((i, j))
            c_edges.append(bool(set(edge_one.tuple) & set(existing_node[0].tuple)))
        edges[edge_one.index] = edge_one

    # rest of the edges
    edge_types_one, incident_edges_one = get_edge_info(edges_one[1])
    edge_types_two, incident_edges_two = get_edge_info(edges_two[1])
    for type in edge_types_one:
        if type not in edge_types_two:
            continue
        for edge_one in edge_types_one[type]:
            for edge_two in edge_types_two[type]:
                compat_nodes.append((edge_one, edge_two))
                i = len(compat_nodes)
                for j, existing_node in enumerate(compat_nodes):
                    incident_one = existing_node[0].index in incident_edges_one[edges_one.index]
                    incident_two = existing_node[1].index in incident_edges_two[edges_two.index]
                    if () and \
                            () and \
                            incident_edges_one[edge_one.index][existing_node[0].index] == \
                            incident_edges_two[edges_two.index][existing_node[1].index]:
                        compat_edges.append((i, j))
                        c_edges.append(True)
                    elif not incident_edges_one[edge_one.index][existing_node[0].index] \
                            and not incident_edges_two[edges_two.index][existing_node[1].index]:
                        compat_edges.append((i, j))
                        c_edges.append(False)

        compat_graph.add_vertices(1, attributes={'edges': [(i, j)]})
        for m, inner_edge_one in enumerate(graph_one.es):
            if m == i:
                break
            for n, inner_edge_two in enumerate(graph_two.es):
                if j == n or (m, n) not in compat_graph.vs['edges']:
                    continue
                common_node_one = set(edge_one.tuple) & set(inner_edge_one.tuple)
                common_node_two = set(edge_two.tuple) & set(inner_edge_two.tuple)
                if common_node_one and common_node_two and \
                        graph_one.vs[common_node_one.pop()]['label'] == graph_two.vs[common_node_two.pop()][
                    'label']:
                    compat_graph.add_edges(
                        [[compat_graph.vs(edges_eq=(i, j))[0].index,
                          compat_graph.vs(edges_eq=(m, n))[0].index]],
                        attributes={'is_c_edge': [True]}
                    )
                elif not common_node_one and not common_node_two:
                    compat_graph.add_edges(
                        [[compat_graph.vs(edges_eq=(i, j))[0].index,
                          compat_graph.vs(edges_eq=(m, n))[0].index]],
                        attributes={'is_c_edge': [False]}
                    )

    return None


def find_cliques(compat_graph, required_edges_one, required_edges_two):
    compat_nodes = {i: j for i, j in enumerate(compat_graph.vs)}
    compat_edges = {i: {
        (edge.target if edge.target != i else edge.source): edge for edge in node.incident()
    } for i, node in enumerate(compat_graph.vs)
    }
    compat_neighbors = {i: v.neighbors() for i, v in enumerate(compat_graph.vs)}

    def inner_find_cliques(start_node, addable, not_addable, excluded, used_initializers):
        cliques = []
        stack = deque()
        stack.append(({start_node}, addable, not_addable, excluded))
        while len(stack):
            clique, addable, not_addable, excluded = stack.pop()
            if not len(addable) and not len(excluded):
                cliques.append(list(clique))
                continue
            for node in list(addable):
                addable.remove(node)
                addable_copy = addable.copy()
                not_addable_copy = not_addable.copy()
                excluded_copy = excluded.copy()
                for candidate in list(not_addable_copy):
                    if candidate in used_initializers:
                        excluded_copy.add(candidate)
                        not_addable_copy.remove(candidate)
                    elif candidate in compat_neighbors[node.index] \
                            and compat_edges[node.index][candidate.index]['is_c_edge']:
                        addable_copy.add(candidate)
                        not_addable_copy.remove(candidate)
                neighbors = set(compat_neighbors[node.index])
                stack.append((clique | {node}, addable_copy & neighbors, not_addable_copy & neighbors,
                              excluded_copy & neighbors))
                excluded.add(node)

        return cliques

    cliques = []
    used_initializers = set()
    for node in compat_graph.vs:
        print("New start node.")
        addable = set()
        not_addable = set()
        excluded = set()
        for neighbor in compat_neighbors[node.index]:
            if compat_edges[node.index][neighbor.index]['is_c_edge']:
                if neighbor in used_initializers:
                    excluded.add(neighbor)
                else:
                    addable.add(neighbor)
            else:
                not_addable.add(neighbor)
        cliques += inner_find_cliques(node, addable, not_addable, excluded, used_initializers)
        used_initializers.add(node)
    print("Cliques found!")
    return cliques


def transform_cliques_to_edges(clique, compat_graph):
    edges_one = set()
    edges_two = set()
    for edge in clique:
        edges_one.add(edge['edges'][0])
        edges_two.add(edge['edges'][1])
    return edges_one, edges_two


def find_mcs(graph_one, required_nodes_one, graph_two, required_nodes_two):
    # TODO: consider in_rule_ids
    needed_edges_one = {edge.index for edge in graph_one.es(_within=required_nodes_one)}
    needed_edges_two = {edge.index for edge in graph_two.es(_within=required_nodes_two)}
    compat_graph = generate_compat_graph(graph_one, graph_two)
    compat_cliques = find_cliques(compat_graph, None, None)
    mcs = []
    largest = 0
    for clique in compat_cliques:
        edges_one, edges_two = transform_cliques_to_edges(clique, compat_graph)
        if not (needed_edges_one < edges_one and needed_edges_two < edges_two):
            continue
        mcs_graph = graph_one.subgraph_edges(list(edges_one))
        if not mcs_graph.is_connected():
            continue
        if len(mcs_graph.vs) > largest:
            largest = len(mcs_graph.vs)
            mcs = [mcs_graph]
        elif len(mcs_graph.vs) == largest:
            mcs.append(mcs_graph)
    return mcs[0]


def find_mcs_of_set(graphs):
    current_mcs = graphs[0]
    for graph in graphs[1:]:
        required_nodes_one = [node.index for node in current_mcs.vs if node['id_in_rule'] is not None]
        required_nodes_two = [node.index for node in graph.vs if node['id_in_rule'] is not None]
        current_mcs = find_mcs(current_mcs, required_nodes_one, graph, required_nodes_two)
    return current_mcs


def merge_mcs_with_rule(rule_gml, mcs):
    free_id = max(int(x) for x in re.findall(rf'node \[ id (\d+) label ".+?" ]', rule_gml))
    free_id = itertools.count(free_id + 1)

    # replace variables
    for var_node in mcs.vs(is_variable=True):
        rule_gml = re.sub(rf'node \[ id {var_node["id_in_rule"]} label ".*?" ]',
                          f'node [ id {var_node["id_in_rule"]} label "{var_node["label"]}" ]',
                          rule_gml)
    # insert not yet existing nodes
    new_nodes = {}
    insert_point = rule_gml.find('context [') + 9
    for node in mcs.vs(id_in_rule=None):
        new_id = next(free_id)
        new_nodes[node.index] = new_id
        node_gml = f'node [ id {new_id} label "{node["label"]}" ]'
        rule_gml = rule_gml[:insert_point] + node_gml + rule_gml[insert_point:]

    for edge in mcs.es:
        if not (edge.source in new_nodes or edge.target in new_nodes):
            continue
        source_id = new_nodes[edge.source] if edge.source in new_nodes else edge.source_vertex['id_in_rule']
        target_id = new_nodes[edge.target] if edge.target in new_nodes else edge.target_vertex['id_in_rule']
        edge_gml = f'edge [ source {source_id} target {target_id} label "{edge["label"]}" ]'
        rule_gml = rule_gml[:insert_point] + edge_gml + rule_gml[insert_point:]

    return rule_gml


def get_environment_matches(mcs, bound_graph):
    def node_compat(large_graph, small_graph, large_vertex, small_vertex):
        small_vertex = small_graph.vs[small_vertex]
        large_vertex = large_graph.vs[large_vertex]
        return (small_vertex['id_in_rule'] == large_vertex['id_in_rule']) \
               and (small_vertex['label'] == large_vertex['label'])

    def edge_compat(large_graph, small_graph, large_edge, small_edge):
        return large_graph.es[large_edge]['label'] == small_graph.es[small_edge]['label']

    matches = bound_graph.get_subisomorphisms_vf2(
        mcs,
        node_compat_fn=node_compat, edge_compat_fn=edge_compat
    )
    return matches


def get_environments(mcs, bound_graph):
    matches = get_environment_matches(mcs, bound_graph)
    all_environments = set()
    for match in matches:
        per_node_environments = []
        matched_nodes = set(match)  # faster membership
        for mcs_node, bg_node in enumerate(match):
            bg_node = bound_graph.vs[bg_node]
            environment = []
            for edge in bg_node.incident():
                other = edge.source_vertex if edge.source_vertex != bg_node else edge.target_vertex
                if other.index in matched_nodes:
                    continue
                environment.append((edge['label'], other['label']))
            per_node_environments.append(tuple(sorted(environment)))
        all_environments.add(tuple(per_node_environments))
    return all_environments


def partition_environments(environments):
    environment_maps = [{} for _ in range(0, len(environments[0][0]))]
    for graph_idx, per_graph_envs in enumerate(environments):
        for per_graph_env in per_graph_envs:
            for node_idx, per_node_env in enumerate(per_graph_env):
                for env_el in per_node_env:
                    if env_el not in environment_maps[node_idx]:
                        environment_maps[node_idx][env_el] = set()
                    environment_maps[node_idx][env_el].add(graph_idx)
    print(environment_maps)
    groups = set()
    for per_node_dict in environment_maps:
        for group in per_node_dict.values():
            groups.add(tuple(sorted(group)))
    return groups
