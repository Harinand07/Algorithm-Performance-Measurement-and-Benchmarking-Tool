"""Core graph algorithms for routing, connectivity and infrastructure planning."""
import heapq
from collections import deque
from math import inf

def dijkstra(graph, source, target=None):
    if source not in graph.adj_list: raise KeyError(f"Unknown source: {source}")
    if any(w < 0 for u in graph.adj_list for _, w in graph.adj_list[u]):
        raise ValueError("Dijkstra requires non-negative edge weights.")
    dist = {n: inf for n in graph.nodes}; parent = {n: None for n in graph.nodes}
    dist[source] = 0; pq = [(0, source)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]: continue
        if target is not None and u == target: break
        for v, w in graph.adj_list[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd; parent[v] = u
                heapq.heappush(pq, (nd, v))
    return dist, parent

def reconstruct_path(parent, source, target):
    if source == target: return [source]
    path, cur = [], target
    while cur is not None:
        path.append(cur)
        if cur == source: return path[::-1]
        cur = parent.get(cur)
    return []

def bellman_ford(graph, source):
    if source not in graph.adj_list: raise KeyError(f"Unknown source: {source}")
    dist = {n: inf for n in graph.nodes}; parent = {n: None for n in graph.nodes}
    dist[source] = 0
    edges = graph.edges if graph.directed else graph.unique_edges() + [(v,u,w) for u,v,w in graph.unique_edges()]
    for _ in range(max(0, len(graph.nodes)-1)):
        changed = False
        for u,v,w in edges:
            if dist[u] != inf and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w; parent[v] = u; changed = True
        if not changed: break
    negative_cycle = any(dist[u] != inf and dist[u] + w < dist[v] for u,v,w in edges)
    return dist, parent, negative_cycle

def bfs(graph, source):
    if source not in graph.adj_list: raise KeyError(source)
    seen, order, q = {source}, [], deque([source])
    while q:
        u = q.popleft(); order.append(u)
        for v, _ in graph.adj_list[u]:
            if v not in seen: seen.add(v); q.append(v)
    return order

def dfs(graph, source):
    if source not in graph.adj_list: raise KeyError(source)
    seen, order = set(), []
    def visit(u):
        seen.add(u); order.append(u)
        for v, _ in graph.adj_list[u]:
            if v not in seen: visit(v)
    visit(source)
    return order

class UnionFind:
    def __init__(self, nodes):
        self.parent = {n:n for n in nodes}; self.rank = {n:0 for n in nodes}
    def find(self, x):
        if self.parent[x] != x: self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    def union(self, a,b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb: return False
        if self.rank[ra] < self.rank[rb]: ra,rb = rb,ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]: self.rank[ra] += 1
        return True

def prim_mst(graph, start=None):
    if not graph.nodes: return [], 0
    start = start or graph.nodes[0]
    if start not in graph.adj_list: raise KeyError(start)
    visited = {start}; heap = [(w,start,v) for v,w in graph.adj_list[start]]
    heapq.heapify(heap); mst=[]; cost=0
    while heap and len(visited) < len(graph.nodes):
        w,u,v = heapq.heappop(heap)
        if v in visited: continue
        visited.add(v); mst.append((u,v,w)); cost += w
        for nxt,nw in graph.adj_list[v]:
            if nxt not in visited: heapq.heappush(heap,(nw,v,nxt))
    if len(visited) != len(graph.nodes): raise ValueError("Graph is disconnected; spanning tree does not exist.")
    return mst, cost

def kruskal_mst(graph):
    uf = UnionFind(graph.nodes); mst=[]; cost=0
    for u,v,w in sorted(graph.unique_edges(), key=lambda x:x[2]):
        if uf.union(u,v): mst.append((u,v,w)); cost += w
        if len(mst) == max(0,len(graph.nodes)-1): break
    if len(mst) != max(0,len(graph.nodes)-1):
        raise ValueError("Graph is disconnected; spanning tree does not exist.")
    return mst, cost
