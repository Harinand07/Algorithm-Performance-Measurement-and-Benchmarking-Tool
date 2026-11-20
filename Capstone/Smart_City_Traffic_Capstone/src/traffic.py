"""Traffic scenario helpers."""
from .graph import CityGraph

def simulate_congestion(graph, congested_edges, multiplier=3.0):
    if multiplier < 1: raise ValueError("Congestion multiplier must be >= 1.")
    affected = {frozenset(e) for e in congested_edges}
    new_graph = CityGraph(graph.directed)
    for node in graph.nodes: new_graph.add_node(node)
    for u,v,w in graph.edges:
        factor = multiplier if frozenset((u,v)) in affected else 1.0
        new_graph.add_edge(u,v,w*factor)
    return new_graph

def route_summary(graph, source, target, algorithm):
    from .algorithms import dijkstra, bellman_ford, reconstruct_path
    if algorithm == "Dijkstra":
        dist,parent = dijkstra(graph, source, target)
        return reconstruct_path(parent,source,target), dist[target]
    dist,parent,negative = bellman_ford(graph,source)
    if negative: raise ValueError("Negative cycle detected; shortest route is undefined.")
    return reconstruct_path(parent,source,target), dist[target]
