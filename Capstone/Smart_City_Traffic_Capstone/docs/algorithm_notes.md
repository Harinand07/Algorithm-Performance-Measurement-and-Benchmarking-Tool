# Algorithm and design notes

## Model
Intersections are vertices; roads are weighted edges. The sample graph is undirected because roads
are assumed to be bidirectional. Weights represent illustrative travel-time minutes.

## Shortest paths
Dijkstra uses a min-heap and requires non-negative weights. Bellman-Ford relaxes all edges up to
V−1 times and checks for a reachable negative-weight cycle. Parent maps reconstruct a route.

## Traversal
BFS uses a queue and explores by hop distance. DFS recursively explores each branch before
backtracking. Both report vertices reachable from a selected source.

## Infrastructure planning
Prim grows an MST from a start vertex using a heap of frontier edges. Kruskal sorts edges and
uses Disjoint Set Union with path compression and union by rank. For a connected undirected graph,
both should return V−1 edges and equal total weight.

## Congestion
A selected road's weight is multiplied by a user-controlled factor. The shortest path is recalculated
to show how changed travel costs can influence route selection.

## Limitations and ethical use
This prototype is a classroom simulation. It does not ingest live sensors, model road capacity,
predict queue lengths, or control traffic signals. Real deployment would require validated data,
privacy safeguards, accessibility review, cybersecurity controls and transport-engineer oversight.
