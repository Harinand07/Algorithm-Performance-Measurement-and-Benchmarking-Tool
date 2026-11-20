import unittest
from src.sample_data import build_sample_city, build_large_city
from src.algorithms import dijkstra, bellman_ford, bfs, dfs, prim_mst, kruskal_mst, reconstruct_path
from src.traffic import simulate_congestion

class TestCityAlgorithms(unittest.TestCase):
    def setUp(self): self.g=build_sample_city()
    def test_dijkstra_and_path(self):
        d,p=dijkstra(self.g,"Central","Airport")
        self.assertEqual(d["Airport"],15)
        self.assertEqual(reconstruct_path(p,"Central","Airport"),["Central","University","Hospital","Airport"])
    def test_bellman_ford_matches_dijkstra(self):
        d,_,negative=bellman_ford(self.g,"Central")
        expected,_=dijkstra(self.g,"Central")
        self.assertFalse(negative); self.assertEqual(d,expected)
    def test_traversals_cover_connected_graph(self):
        self.assertEqual(set(bfs(self.g,"Central")),set(self.g.nodes))
        self.assertEqual(set(dfs(self.g,"Central")),set(self.g.nodes))
    def test_mst_algorithms_agree(self):
        _,a=prim_mst(self.g); _,b=kruskal_mst(self.g)
        self.assertEqual(a,b); self.assertEqual(len(self.g.nodes)-1, len(prim_mst(self.g)[0]))
    def test_congestion_does_not_improve_cost(self):
        congested=simulate_congestion(self.g,[("University","Tech Park")],4)
        before,_=dijkstra(self.g,"Central")
        after,_=dijkstra(congested,"Central")
        self.assertGreaterEqual(after["Airport"],before["Airport"])
    def test_large_dataset_size(self):
        large = build_large_city()
        self.assertEqual(len(large.nodes), 100)
        self.assertEqual(len(large.unique_edges()), 250)
        self.assertEqual(len(bfs(large, large.nodes[0])), 100)

    def test_negative_cycle_detection(self):
        from src.graph import CityGraph
        g=CityGraph(directed=True)
        g.add_edge("A","B",1); g.add_edge("B","C",-3); g.add_edge("C","A",1)
        _,_,negative=bellman_ford(g,"A")
        self.assertTrue(negative)

if __name__=="__main__": unittest.main()
