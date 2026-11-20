"""Deterministic sample road networks: compact test graph and expanded 100-node city."""
import csv
from pathlib import Path
from .graph import CityGraph
NODES = ["Central", "Museum", "University", "Hospital", "Airport", "Stadium", "Market", "Tech Park"]
EDGES = [
    ("Central","Museum",4), ("Central","University",3), ("Central","Market",6),
    ("Museum","University",2), ("Museum","Hospital",7), ("University","Hospital",4),
    ("University","Tech Park",5), ("Hospital","Airport",8), ("Hospital","Stadium",3),
    ("Market","Stadium",4), ("Stadium","Airport",6), ("Market","Tech Park",9),
    ("Tech Park","Airport",7), ("Museum","Market",5)
]
def build_sample_city():
    """Small 8-node graph used by focused unit tests and algorithm examples."""
    return CityGraph.from_edges(EDGES)
def build_large_city():
    """Load the 100-intersection, 250-road synthetic dataset from data/."""
    path = Path(__file__).resolve().parent.parent / "data" / "city_network_100_nodes_250_roads.csv"
    graph = CityGraph()
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            graph.add_edge(row["from"], row["to"], float(row["travel_time_minutes"]))
    return graph
