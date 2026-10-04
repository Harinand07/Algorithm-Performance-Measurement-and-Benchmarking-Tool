# Algorithm Performance Measurement and Benchmarking Tool

Lab 2 implementation covering Linear Search, Binary Search, Single Loop, Nested Loop, Recursive Factorial, Iterative Factorial, automated benchmarking, visualization and complexity analysis.

## Setup
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Run
```bash
python benchmark_engine.py
streamlit run app.py
```

## Files
`app.py`, `search_analysis.py`, `code_benchmark.py`, `benchmark_engine.py`, `project_notebook.ipynb`, `requirements.txt`, `README.md`, `data/`, `graphs/`, `screenshots/`, `Lab2_Report.docx`, `Lab2_Report.pdf`.

## Complexity
Linear Search O(n)/O(1); Binary Search O(log n)/O(1); Single Loop O(n)/O(1); Nested Loop O(n²)/O(1); Recursive Factorial O(n)/O(n); Iterative Factorial O(n)/O(1).

## Benchmark note
The assignment lists 50,000 for loop programs. A literal 50,000×50,000 nested loop requires 2.5 billion inner iterations and is therefore retained in the configuration but skipped in the executable benchmark. The report explicitly labels this case instead of inventing a timing.
