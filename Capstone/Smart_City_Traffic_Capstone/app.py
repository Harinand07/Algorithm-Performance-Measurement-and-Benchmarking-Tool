import streamlit as st
import pandas as pd
import sys, time
from pathlib import Path
ROOT = Path(__file__).parent
sys.path.insert(0,str(ROOT))
from src.sample_data import build_large_city
from src.algorithms import dijkstra, bellman_ford, bfs, dfs, prim_mst, kruskal_mst, reconstruct_path
from src.traffic import simulate_congestion
from src.visualization import draw_network

st.set_page_config(page_title="Smart City Traffic Optimizer",page_icon="🚦",layout="wide")
st.title("🚦 Smart City Traffic Management & Route Optimization")
st.caption("Graph-based decision support • Sample travel-time units • Educational simulation")
if "traffic_factor" not in st.session_state: st.session_state.traffic_factor = 3.0
city = build_large_city()
nodes = city.nodes
with st.sidebar:
    st.header("Control panel")
    source = st.selectbox("Source intersection",nodes,index=0)
    target = st.selectbox("Destination intersection",nodes,index=len(nodes)-1)
    factor = st.slider("Congestion multiplier",1.0,6.0,3.0,0.5)
    mapping = {f"{u} ↔ {v}": (u, v) for u, v, w in city.unique_edges()}
    road_labels = list(mapping.keys())
    congested = st.multiselect("Congested roads (choose one or more)", road_labels,
                               default=road_labels[:1])
    st.info("All road weights are illustrative travel-time units, not live traffic feeds.")
affected = [mapping[x] for x in congested]
busy = simulate_congestion(city,affected,factor)
c1,c2,c3,c4 = st.columns(4)
c1.metric("Intersections",len(nodes)); c2.metric("Road segments",len(city.unique_edges()))
c3.metric("Congested roads",len(affected)); c4.metric("Congestion factor",f"{factor:.1f}×")
tab1,tab2,tab3,tab4,tab5 = st.tabs(["Route planner","Connectivity","Infrastructure","Graph model","About"])
with tab1:
    st.subheader("Shortest route comparison")
    original_dist, original_parent = dijkstra(city,source,target)
    new_dist, new_parent = dijkstra(busy,source,target)
    old_path = reconstruct_path(original_parent,source,target)
    new_path = reconstruct_path(new_parent,source,target)
    a,b = st.columns(2)
    a.metric("Normal travel cost",f"{original_dist[target]:.1f}")
    b.metric("After congestion",f"{new_dist[target]:.1f}",delta=f"{new_dist[target]-original_dist[target]:+.1f}")
    st.write("**Normal route:** "+" → ".join(old_path))
    st.write("**Congestion-aware route:** "+" → ".join(new_path))
    if original_dist[target] > 0:
        st.write(f"**Travel-cost change:** {(new_dist[target]-original_dist[target])/original_dist[target]*100:.1f}%")
    st.caption("Dijkstra is used because this traffic scenario contains non-negative weights. Expanded dataset: 100 intersections / 250 roads.")
    p=ROOT/"screenshots"/"app_route_graph.png"
    draw_network(busy,p,"Congestion-aware road network",list(zip(new_path,new_path[1:])))
    st.image(str(p),caption="Congestion-aware route highlighted in orange",use_container_width=True)
with tab2:
    st.subheader("Reachability and traversal")
    start=st.selectbox("Traversal start",nodes,key="traversal_start")
    x,y=st.columns(2)
    x.write("**Breadth-first search (BFS)**"); x.code(" → ".join(bfs(city,start)))
    y.write("**Depth-first search (DFS)**"); y.code(" → ".join(dfs(city,start)))
    st.success(f"{len(bfs(city,start))} of {len(nodes)} intersections are reachable from {start}.")
with tab3:
    st.subheader("Minimum spanning tree — infrastructure planning")
    p_edges,p_cost=prim_mst(city)
    k_edges,k_cost=kruskal_mst(city)
    x,y=st.columns(2)
    x.metric("Prim total network cost",f"{p_cost:.1f}")
    y.metric("Kruskal total network cost",f"{k_cost:.1f}")
    st.write("Prim edges:",pd.DataFrame(p_edges,columns=["From","To","Cost"]))
    st.write("Kruskal edges:",pd.DataFrame(k_edges,columns=["From","To","Cost"]))
    st.info("The MST is a minimum-cost connected backbone, not a replacement for every road or a traffic route.")
with tab4:
    st.subheader("Graph representation")
    st.write("Adjacency list")
    st.json({n:[{"neighbor":v,"weight":w} for v,w in city.adj_list[n]] for n in nodes})
    labels,matrix=city.adjacency_matrix()
    st.write("Adjacency matrix (∞ means no direct road)")
    st.dataframe(pd.DataFrame([["∞" if v==float("inf") else v for v in row] for row in matrix],index=labels,columns=labels))
with tab5:
    st.markdown("""
    **Purpose:** Demonstrate graph algorithms for a synthetic 100-intersection, 250-road city network.

    **Implemented:** adjacency list/matrix, Dijkstra, Bellman-Ford, BFS, DFS, Prim, Kruskal,
    congestion simulation, route comparison and visual output.

    **Limitations:** sample data only; no GPS, live sensor feeds, map tiles, accident reports,
    signal-control integration or production deployment. Bellman-Ford is available in the code
    library for negative-edge demonstrations; negative travel times are not realistic.

    **Run:** `pip install -r requirements.txt` then `streamlit run app.py`.
    """)
