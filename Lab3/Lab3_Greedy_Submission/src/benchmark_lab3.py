"""Benchmark all three greedy algorithms. Run: python src/benchmark_lab3.py"""
import os, sys, csv
sys.path.insert(0, os.path.dirname(__file__))
from greedy_lab3 import benchmark
rows=benchmark()
out=os.path.join(os.getcwd(),"benchmark_results.csv")
with open(out,"w",newline="",encoding="utf-8") as f:
    writer=csv.DictWriter(f,fieldnames=rows[0].keys())
    writer.writeheader(); writer.writerows(rows)
print(f"Saved measured results to {out}")
for row in rows: print(row)
