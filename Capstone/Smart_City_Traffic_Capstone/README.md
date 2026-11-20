# Smart City Traffic Management & Route Optimization System

A Python/Streamlit capstone demonstrating graph modeling, shortest paths, graph traversal,
traffic congestion simulation, minimum spanning trees, visualization and algorithm analysis.

## Features
- Weighted undirected road network using adjacency list and adjacency matrix
- Dijkstra shortest path and Bellman-Ford shortest path / negative-cycle detection
- BFS and DFS reachability analysis
- Prim and Kruskal minimum spanning trees with Union-Find
- Congestion simulation by multiplying selected road travel-time weights
- Interactive Streamlit interface and saved PNG visualizations
- Unit tests and sample data

## Requirements
- Python 3.10 or newer recommended

## Setup and run
```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
Open the local URL printed by Streamlit (usually http://localhost:8501).

## Run tests
From the project root:
```bash
python -m unittest discover -s tests -v
```

## Repository structure
```text
app.py                 Streamlit interface
src/graph.py           Graph representation
src/algorithms.py      Dijkstra, Bellman-Ford, BFS, DFS, Prim, Kruskal
src/traffic.py         Congestion and route comparison helpers
src/visualization.py   Network and benchmark plots
src/sample_data.py     Compact test graph and expanded CSV-backed city network
benchmark.py           Small-vs-large algorithm runtime comparison
data/                  Sample road network CSV
tests/                 Automated unit tests
screenshots/           Generated evidence images
logs/                  Sample test/run log
docs/                  Final report and supplementary notes
```

## Algorithms and complexity
| Algorithm | Time | Auxiliary space (typical) |
|---|---:|---:|
| Build adjacency list | O(V + E) | O(V + E) |
| Build adjacency matrix | O(V²) | O(V²) |
| Dijkstra (binary heap) | O((V + E) log V) | O(V + E) |
| Bellman-Ford | O(VE) | O(V) |
| BFS / DFS | O(V + E) | O(V) |
| Prim (binary heap) | O(E log V) | O(V + E) |
| Kruskal | O(E log E) | O(V + E) |

## Data and interpretation
The supplied city and travel times are synthetic demonstration data. They are not live traffic,
GPS or official municipal measurements. The interface labels weights as illustrative travel-time
units. Bellman-Ford is included to demonstrate negative-edge handling; negative travel times
should not be interpreted as physically meaningful roads.

## GitHub submission
1. Create a public GitHub repository (or a private one with faculty access).
2. Upload this folder's contents; do not upload the ZIP as the only repository content.
3. Commit in meaningful stages (setup, graph model, algorithms, UI, tests, documentation).
4. Add your repository URL to the ZOSIMA submission.
5. Run the app and capture your own machine's screenshots before final submission.

## Academic submission checklist
- [ ] Replace student/institution placeholders in the report.
- [ ] Run the app locally and verify it opens.
- [ ] Run tests and include your actual terminal output.
- [ ] Capture fresh screenshots of the running interface.
- [ ] Create GitHub repository and verify access.
- [ ] Upload final PDF and repository link to ZOSIMA.

## Expanded dataset and benchmarking
The default app loads 100 synthetic intersections and 250 roads from `data/city_network_100_nodes_250_roads.csv`. The compact graph remains for tests. Run `python benchmark.py` for a small-vs-large runtime comparison; results are saved in `logs/benchmark_results.json`.
