# Suggested GitHub commit sequence

Run these commands from the project root after `git init`:

1. `git add README.md requirements.txt .gitignore` then commit: `chore: initialize project documentation and dependencies`
2. `git add src/graph.py src/sample_data.py data/road_network.csv` then commit: `feat: add weighted city road graph and sample dataset`
3. `git add src/algorithms.py` then commit: `feat: implement shortest paths traversals and MST algorithms`
4. `git add src/traffic.py` then commit: `feat: add traffic congestion simulation`
5. `git add src/visualization.py app.py` then commit: `feat: add interactive Streamlit dashboard and visualizations`
6. `git add tests logs` then commit: `test: add graph algorithm validation and sample logs`
7. `git add docs screenshots Smart_City_Traffic_Capstone_Report.pdf` then commit: `docs: add report screenshots and submission evidence`

Use your actual GitHub account to create the repository and push it. These are suggested commit messages, not commits already made.
