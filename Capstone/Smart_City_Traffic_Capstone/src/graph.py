"""Weighted road-network graph with adjacency-list and adjacency-matrix views."""
from math import inf

class CityGraph:
    def __init__(self, directed=False):
        self.directed = directed
        self.adj_list = {}
        self.edges = []

    @property
    def nodes(self):
        return list(self.adj_list.keys())

    def add_node(self, node):
        if node not in self.adj_list:
            self.adj_list[node] = []

    def add_edge(self, u, v, weight):
        if weight < 0:
            # Negative weights are permitted for Bellman-Ford experiments.
            pass
        self.add_node(u); self.add_node(v)
        self.adj_list[u].append((v, float(weight)))
        self.edges.append((u, v, float(weight)))
        if not self.directed:
            self.adj_list[v].append((u, float(weight)))

    def adjacency_matrix(self):
        nodes = self.nodes
        index = {node: i for i, node in enumerate(nodes)}
        matrix = [[0 if i == j else inf for j in range(len(nodes))]
                  for i in range(len(nodes))]
        for u, neighbors in self.adj_list.items():
            for v, w in neighbors:
                matrix[index[u]][index[v]] = w
        return nodes, matrix

    def unique_edges(self):
        if self.directed:
            return list(self.edges)
        seen, result = set(), []
        for u, v, w in self.edges:
            key = frozenset((u, v))
            if key not in seen:
                seen.add(key); result.append((u, v, w))
        return result

    def copy(self):
        g = CityGraph(self.directed)
        for n in self.nodes: g.add_node(n)
        for u, v, w in self.edges: g.add_edge(u, v, w)
        return g

    @classmethod
    def from_edges(cls, edges, directed=False):
        g = cls(directed)
        for u, v, w in edges: g.add_edge(u, v, w)
        return g
