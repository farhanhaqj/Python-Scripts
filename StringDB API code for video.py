#!/usr/bin/env python
# coding: utf-8

# In[2]:


#Step:1 Importing Libraries
import requests
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors

# Step:2 Fetch Gene Interactions
def fetch_interactions(genes, api_key=None):
    base_url = "https://string-db.org/api/json/network"
    params = {
        "identifiers": "%0d".join(genes),
        "species": 9606,  # Human species ID
        "required_score": 400,
    }
    if api_key:
        params["api_key"] = api_key

    response = requests.get(base_url, params=params)
    return response.json() if response.status_code == 200 else None

#Step:3 Visualizing the Network
def visualize_network(data):
    G = nx.Graph()

    # Add edges with weights based on the interaction score
    for interaction in data:
        protein1 = interaction["preferredName_A"]
        protein2 = interaction["preferredName_B"]
        score = interaction["score"]
        G.add_edge(protein1, protein2, weight=score)

    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 8))

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=500)

    # Get edge weights and normalize them for the colormap
    edge_weights = []
    for u, v, d in G.edges(data=True):
        edge_weights.append(d['weight'])
    norm = mcolors.Normalize(vmin=min(edge_weights), vmax=max(edge_weights))
    cmap = cm.get_cmap('coolwarm')

    # Draw edges with varying widths and colors based on the score
    for (u, v, d) in G.edges(data=True):
        weight = d['weight']
        edge_color = cmap(norm(weight))
        edge_width = 1 + 2 * (weight - min(edge_weights)) / (max(edge_weights) - min(edge_weights))
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], width=edge_width, edge_color=[edge_color])

    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=10)

    plt.title("Gene Interaction Network")
    plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), label='Interaction Score')
    plt.show()

    
#Step:4 Run the Code
genes = ["TP53", "BRCA1", "EGFR", "AKT1", "MYC", "PIK3CA", "CDK1", "MDM2", "BCL2", "KRAS", "PTEN", "ERBB2", "MAPK1", "SRC", "VEGFA", "STAT3", "RB1", "E2F1", "CCND1", "JUN"] # List of genes
api_key = "your_string_api_key_here"  # STRING API key (optional)
data = fetch_interactions(genes, api_key)

if data:
    print("Gene Interactions retrieved successfully.")
    visualize_network(data)
else:
    print("No interactions found or error occurred.")


# In[ ]:




