"""Compare algorithm runtimes on compact and expanded synthetic city graphs."""
import time, statistics, json
from src.sample_data import build_sample_city, build_large_city
from src.algorithms import dijkstra, bellman_ford, bfs, dfs, prim_mst, kruskal_mst
def measure(fn, repeats=25):
    samples=[]
    for _ in range(repeats):
        start=time.perf_counter(); fn(); samples.append((time.perf_counter()-start)*1000)
    return round(statistics.mean(samples), 4)
def run():
    results={}
    for label, graph in [("small_8_nodes",build_sample_city()),("large_100_nodes",build_large_city())]:
        source=graph.nodes[0]
        results[label]={"vertices":len(graph.nodes),"edges":len(graph.unique_edges())}
        calls={"Dijkstra":lambda:dijkstra(graph,source),"Bellman-Ford":lambda:bellman_ford(graph,source),
               "BFS":lambda:bfs(graph,source),"DFS":lambda:dfs(graph,source),
               "Prim":lambda:prim_mst(graph),"Kruskal":lambda:kruskal_mst(graph)}
        results[label]["mean_runtime_ms"]={name:measure(fn) for name,fn in calls.items()}
    print(json.dumps(results,indent=2)); return results
if __name__=="__main__": run()
