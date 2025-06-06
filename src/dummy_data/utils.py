# Import necessary libraries
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
import scipy

from src.dummy_data import DataGenerator, GraphMerger

def visualize_graph(graph_dict):
    # Create a directed graph
    G = nx.DiGraph()
    
    # Add nodes and edges
    for node, data in graph_dict.items():
        G.add_node(node, description=data['description'])
        for child in data['children']:
            G.add_edge(node, child)
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, k=1, iterations=50)
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                          node_size=2000, alpha=0.6)
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, edge_color='gray', 
                          arrows=True, arrowsize=20)
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=10)
    
    plt.title("Causal Graph Visualization")
    plt.axis('off')
    plt.show()

def convert_graph_to_relation_matrix(graph):
    nodes = list(graph.keys())
    relation_matrix = {}

    for i in nodes:
        relation_matrix[i] = {}
        for j in nodes:
            if i == j:
                continue
            if j in graph[i]["children"]:
                relation_matrix[i][j] = {
                    "isChild": 1,
                    "isParent": 0,
                    "noRelation": 0
                }
            elif i in graph[j]["children"]:
                relation_matrix[i][j] = {
                    "isChild": 0,
                    "isParent": 1,
                    "noRelation": 0
                }
            else:
                relation_matrix[i][j] = {
                    "isChild": 0,
                    "isParent": 0,
                    "noRelation": 1
                }

    return relation_matrix