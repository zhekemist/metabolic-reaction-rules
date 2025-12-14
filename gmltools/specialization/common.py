import igraph as ig
import matplotlib.pyplot as plt

from gmltools.modimport import mod


# --- PLOTTING ---

def plot_ig_graphs(*graphs, size=(5, 5)):
    for graph in graphs:
        fig, ax = plt.subplots(figsize=size)
        ig.plot(graph, target=ax, edge_label=graph.es['label'])
    plt.show()


def print_ig_graphs(*graphs):
    p = mod.GraphPrinter()
    p.setMolDefault()
    p.withIndex = True
    for graph in graphs:
        graph = convert_ig_graph_to_modgraph(graph)
        graph.print(p)


# --- CONVERSION FUNCTIONS ---

def convert_modgraph_to_ig_graph(mod_graph):
    vertex_map = {}
    vertex_labels = []
    for new_vertex_id, vertex in enumerate(mod_graph.vertices):
        vertex_map[vertex.id] = new_vertex_id
        vertex_labels.append(vertex.stringLabel)

    edges = []
    edge_labels = []
    for edge in mod_graph.edges:
        edges.append([
            vertex_map[edge.source.id], vertex_map[edge.target.id]
        ])
        edge_labels.append(edge.stringLabel)

    ig_graph = ig.Graph(n=len(vertex_map), edges=edges,
                        vertex_attrs={'label': vertex_labels, 'old_id': list(vertex_map)},
                        edge_attrs={'label': edge_labels})
    if hasattr(mod_graph, 'id'):
        ig_graph['id'] = mod_graph.id
    return ig_graph


def convert_ig_graph_to_modgraph(ig_graph):
    gml = 'graph ['
    for vertex in ig_graph.vs:
        gml += f'node [ id {vertex.index} label "{vertex["label"]}" ]'
    for edge in ig_graph.es:
        gml += f'edge [ source {edge.source} target {edge.target} label "{edge["label"]}" ]'
    gml += ']'
    return mod.graphGMLString(gml)
