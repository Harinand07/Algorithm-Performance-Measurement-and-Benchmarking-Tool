"""Network plotting utilities. Saves PNG files for reports and demonstrations."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

def draw_network(graph, output_path, title="City road network", highlight_edges=None):
    G = nx.Graph()
    G.add_nodes_from(graph.nodes)
    for u,v,w in graph.unique_edges(): G.add_edge(u,v,weight=w)
    pos = nx.spring_layout(G, seed=17)
    plt.figure(figsize=(9,6))
    nx.draw_networkx_nodes(G,pos,node_color="#cfe8f3",node_size=1500,edgecolors="#24536b")
    nx.draw_networkx_labels(G,pos,font_size=9,font_weight="bold")
    nx.draw_networkx_edges(G,pos,width=1.8,edge_color="#718096")
    labels = {(u,v): f"{w:g}" for u,v,w in graph.unique_edges()}
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels,font_size=8)
    if highlight_edges:
        valid = [(u,v) for u,v in highlight_edges if G.has_edge(u,v) or G.has_edge(v,u)]
        nx.draw_networkx_edges(G,pos,edgelist=valid,width=3.5,edge_color="#e4572e")
    plt.title(title,fontsize=14); plt.axis("off"); plt.tight_layout()
    plt.savefig(output_path,dpi=170,bbox_inches="tight"); plt.close()

def draw_comparison(labels, values, output_path, title, ylabel):
    plt.figure(figsize=(7,4))
    plt.bar(labels,values)
    plt.title(title); plt.ylabel(ylabel); plt.grid(axis="y",alpha=.25)
    plt.tight_layout(); plt.savefig(output_path,dpi=170); plt.close()
