# Expanded synthetic city road network

File: `city_network_100_nodes_250_roads.csv`

- Intersections (vertices): 100
- Road segments (undirected edges): 250
- Layout: 10 × 10 junction grid
- Composition: 180 orthogonal arterial roads, 41 diagonal connections, 29 expressway links
- Weight: illustrative travel time in minutes (positive numeric weights)
- Reproducibility: generated deterministically using seed 2401201044
- Geography: fictional/synthetic; not real-world coordinates or municipal traffic measurements

Loaded by `src.sample_data.build_large_city()` and used by default in `app.py`.
The compact eight-node example remains available as `build_sample_city()` for focused tests.
