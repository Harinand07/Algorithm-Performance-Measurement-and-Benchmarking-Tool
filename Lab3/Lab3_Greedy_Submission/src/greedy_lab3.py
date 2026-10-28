"""
Lab 3: Smart Resource Allocation and Scheduling System using Greedy Algorithms
Student: Kushagra Verma | Roll No.: 2401201044
Specialisation: BCA (AI & Data Science) | Section: __________
Run: python greedy_lab3.py
"""
from collections import Counter
from dataclasses import dataclass
import heapq
import time
import tracemalloc
import random
import statistics
import matplotlib.pyplot as plt

def fractional_knapsack(items, capacity):
    """Return (maximum value, [(name, fraction_taken), ...])."""
    if capacity < 0:
        raise ValueError("Capacity must be non-negative.")
    if any(x["weight"] <= 0 for x in items):
        raise ValueError("Every item weight must be positive.")
    ordered = sorted(items, key=lambda x: x["value"] / x["weight"], reverse=True)
    total, chosen, remaining = 0.0, [], capacity
    for item in ordered:
        if remaining <= 0:
            break
        take = min(1.0, remaining / item["weight"])
        total += item["value"] * take
        remaining -= item["weight"] * take
        if take > 0:
            chosen.append((item["name"], take))
    return total, chosen

def activity_selection(activities):
    """Return maximum-size compatible activity set, sorted by finish time."""
    if not activities:
        return []
    ordered = sorted(activities, key=lambda a: a["finish"])
    chosen = [ordered[0]]
    last_finish = ordered[0]["finish"]
    for act in ordered[1:]:
        if act["start"] >= last_finish:
            chosen.append(act)
            last_finish = act["finish"]
    return chosen

@dataclass
class HuffmanNode:
    char: str | None
    freq: int
    left: object = None
    right: object = None
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    if not text:
        return None
    freq = Counter(text)
    heap = [HuffmanNode(ch, count) for ch, count in freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        heapq.heappush(heap, HuffmanNode(None, left.freq + right.freq, left, right))
    return heap[0]

def generate_codes(node, prefix="", codes=None):
    if codes is None:
        codes = {}
    if node is None:
        return codes
    if node.char is not None:
        codes[node.char] = prefix or "0"
    else:
        generate_codes(node.left, prefix + "0", codes)
        generate_codes(node.right, prefix + "1", codes)
    return codes

def huffman_encode(text):
    root = build_huffman_tree(text)
    codes = generate_codes(root)
    encoded = "".join(codes[ch] for ch in text)
    return encoded, codes, root

def plot_knapsack(selection, output="knapsack_allocation.png"):
    names = [name for name, _ in selection]
    vals = [fraction * 100 for _, fraction in selection]
    plt.figure(figsize=(7.5, 4.4))
    plt.bar(names, vals)
    plt.ylabel("Item taken (%)")
    plt.ylim(0, 110)
    plt.title("Fractional Knapsack — Resource Allocation")
    plt.grid(axis="y", alpha=.25)
    plt.tight_layout(); plt.savefig(output, dpi=160); plt.close()

def plot_activity_timeline(selected, output="activity_timeline.png"):
    plt.figure(figsize=(8, 4.5))
    for i, a in enumerate(selected):
        plt.barh(i, a["finish"]-a["start"], left=a["start"], height=.55)
        plt.text(a["start"]+.05, i, a["name"], va="center", ha="left", fontsize=9)
    plt.yticks(range(len(selected)), [a["name"] for a in selected])
    plt.xlabel("Time")
    plt.title("Activity Selection — Scheduled Timeline")
    plt.grid(axis="x", alpha=.25)
    plt.tight_layout(); plt.savefig(output, dpi=160); plt.close()

def plot_huffman_tree(node, output="huffman_tree.png"):
    fig, ax = plt.subplots(figsize=(9, 5.4))
    ax.axis("off")
    def layout(n, depth=0, x0=0, x1=1):
        if n is None: return
        x=(x0+x1)/2; y=1-depth*.19
        label = f"{n.char!r}\\n{n.freq}" if n.char is not None else f"Σ\\n{n.freq}"
        ax.text(x,y,label,ha="center",va="center",fontsize=9,
                bbox=dict(boxstyle="round,pad=.35",fc="white",ec="#333333"))
        if n.left:
            lx,ly=layout(n.left,depth+1,x0,x)
            ax.plot([x,lx],[y-.035,ly+.035],color="#4472C4",lw=1.4)
            ax.text((x+lx)/2,(y+ly)/2,"0",fontsize=9)
        if n.right:
            rx,ry=layout(n.right,depth+1,x,x1)
            ax.plot([x,rx],[y-.035,ry+.035],color="#70AD47",lw=1.4)
            ax.text((x+rx)/2,(y+ry)/2,"1",fontsize=9)
        return x,y
    layout(node)
    ax.set_xlim(-.02,1.02); ax.set_ylim(-.03,1.08)
    ax.set_title("Huffman Tree (left edge = 0, right edge = 1)")
    plt.tight_layout(); plt.savefig(output,dpi=160); plt.close()

def benchmark_once(fn):
    tracemalloc.start()
    start = time.perf_counter()
    fn()
    elapsed = time.perf_counter() - start
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return elapsed * 1000, peak / 1024

def benchmark():
    """Median of 5 measured runs; timings vary by machine and Python version."""
    rows=[]
    for n in [100, 500, 1000, 2500, 5000]:
        items=[{"name":f"I{i}","weight":random.randint(1,100)+.1,
                "value":random.randint(1,300)} for i in range(n)]
        acts=[]
        t=0
        for i in range(n):
            start=random.randint(0, n*2)
            acts.append({"name":f"A{i}","start":start,"finish":start+random.randint(1,20)})
        text="".join(random.choice("abcdefghijklmnopqrstuvwxyz ") for _ in range(n))
        cases=[
            ("Fractional Knapsack", lambda items=items: fractional_knapsack(items, n*20)),
            ("Activity Selection", lambda acts=acts: activity_selection(acts)),
            ("Huffman Coding", lambda text=text: huffman_encode(text)),
        ]
        for name, fn in cases:
            results=[benchmark_once(fn) for _ in range(5)]
            rows.append({"Algorithm":name,"Input size":n,
                         "Time (ms)":statistics.median(x[0] for x in results),
                         "Peak memory (KiB)":statistics.median(x[1] for x in results)})
    return rows

def main():
    items=[{"name":"Gold","weight":10,"value":60},
           {"name":"Silver","weight":20,"value":100},
           {"name":"Bronze","weight":30,"value":120}]
    value, selection=fractional_knapsack(items,50)
    activities=[{"name":"A1","start":1,"finish":4},{"name":"A2","start":3,"finish":5},
                {"name":"A3","start":0,"finish":6},{"name":"A4","start":5,"finish":7},
                {"name":"A5","start":3,"finish":9},{"name":"A6","start":5,"finish":9},
                {"name":"A7","start":6,"finish":10},{"name":"A8","start":8,"finish":11}]
    selected=activity_selection(activities)
    encoded,codes,root=huffman_encode("abracadabra")
    print("LAB 3: SMART RESOURCE ALLOCATION AND SCHEDULING")
    print("="*54)
    print(f"Knapsack maximum value: {value:.2f}")
    print("Allocation:", ", ".join(f"{n}={f*100:.1f}%" for n,f in selection))
    print("Selected activities:", ", ".join(f"{a['name']}[{a['start']},{a['finish']}]" for a in selected))
    print("Huffman codes:", dict(sorted(codes.items())))
    print("Encoded bits:", encoded)
    print(f"Original size: {len('abracadabra')*8} bits; encoded size: {len(encoded)} bits")
    print(f"Encoded/original ratio: {len(encoded)/(len('abracadabra')*8):.2%}")
    plot_knapsack(selection, "knapsack_allocation.png")
    plot_activity_timeline(selected, "activity_timeline.png")
    plot_huffman_tree(root, "huffman_tree.png")
    print("Charts saved: knapsack_allocation.png, activity_timeline.png, huffman_tree.png")

if __name__ == "__main__":
    main()
