import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from src.dp_algorithms import lcs, knapsack_01, matrix_chain_order, optimal_parenthesization

st.set_page_config(page_title="Smart Optimization Assistant", page_icon="🧠", layout="wide")
st.title("🧠 Smart Optimization Assistant")
st.caption("Lab 4 | Dynamic Programming: sequence analysis, resource allocation and computation optimization")
tab1, tab2, tab3, tab4 = st.tabs(["LCS", "0/1 Knapsack", "Matrix Chain", "Complexity"])

def show_table(data, title, cmap="Blues"):
    st.subheader(title)
    fig, ax = plt.subplots(figsize=(max(5, len(data[0])*.55), max(2.5, len(data)*.42)))
    im = ax.imshow(data, cmap=cmap, aspect="auto")
    for i in range(len(data)):
        for j in range(len(data[i])):
            ax.text(j, i, str(data[i][j]), ha="center", va="center", fontsize=8)
    fig.colorbar(im, ax=ax, fraction=.025)
    ax.set_xlabel("Column"); ax.set_ylabel("Row")
    st.pyplot(fig); plt.close(fig)

with tab1:
    st.subheader("Sequence Analysis — Longest Common Subsequence")
    c1, c2 = st.columns(2)
    x = c1.text_input("Sequence X", "ABCBDAB")
    y = c2.text_input("Sequence Y", "BDCABA")
    if st.button("Compute LCS", key="lcs"):
        length, seq, table = lcs(x, y)
        st.success(f"LCS: {seq} | Length: {length}")
        show_table(table, "LCS Dynamic Programming Table")

with tab2:
    st.subheader("Resource Allocation — 0/1 Knapsack")
    weights_text = st.text_input("Weights (comma-separated)", "2,3,4,5")
    values_text = st.text_input("Values / profits (comma-separated)", "3,4,5,6")
    capacity = st.number_input("Capacity", min_value=0, value=5, step=1)
    if st.button("Optimize knapsack", key="knap"):
        try:
            weights = [int(v.strip()) for v in weights_text.split(",")]
            values = [int(v.strip()) for v in values_text.split(",")]
            profit, chosen, table = knapsack_01(weights, values, int(capacity))
            st.success(f"Maximum profit: {profit} | Selected item numbers: {[i+1 for i in chosen]}")
            show_table(table, "Knapsack DP Table")
        except Exception as e: st.error(str(e))

with tab3:
    st.subheader("Computation Optimization — Matrix Chain Multiplication")
    dims_text = st.text_input("Dimensions (comma-separated)", "10,30,5,60")
    if st.button("Find optimal order", key="mcm"):
        try:
            dims = [int(v.strip()) for v in dims_text.split(",")]
            cost, table, split = matrix_chain_order(dims)
            n = len(dims)-1
            st.success(f"Minimum scalar multiplications: {cost:,}")
            st.write("Optimal parenthesization:", optimal_parenthesization(split, 1, n))
            show_table([row[1:] for row in table[1:]], "MCM Cost Table")
            show_table([row[1:] for row in split[1:]], "MCM Split Table", "YlGn")
        except Exception as e: st.error(str(e))

with tab4:
    st.subheader("Theoretical Complexity Comparison")
    df = pd.DataFrame([
        ["LCS", "O(m × n)", "O(m × n)", "m × n"],
        ["0/1 Knapsack", "O(n × W)", "O(n × W)", "n × W"],
        ["Matrix Chain Multiplication", "O(n³)", "O(n²)", "O(n²) table states; O(n³) split evaluations"]
    ], columns=["Algorithm","Time","Space","Subproblems / states"])
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.info("Measured runtime and memory depend on hardware, Python version and input values. See results/ for reproducible benchmark output.")
