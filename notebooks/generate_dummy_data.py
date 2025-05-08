# %% [markdown]
# # Generate Dummy Data for Causal Graphs
# 
# This notebook contains code to generate synthetic data for testing the graph merging module.

# %% [markdown]
# ## Using the DataGenerator Class
# 
# The `DataGenerator` class uses Google's Gemini API to generate causal graphs based on natural language queries. Let's see how to use it:

# %%
# Import necessary libraries
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns

# Set random seed for reproducibility
np.random.seed(42)

# %%
# Import the DataGenerator class
import sys
sys.path.append('..')  # Add the parent directory to the Python path
from src.dummy_data import DataGenerator

# %%
# Initialize the DataGenerator with your Gemini API key
# Get your API key from: https://makersuite.google.com/app/apikey
api_key = "YOUR_API_KEY_HERE"  # Replace with your actual API key
generator = DataGenerator(api_key=api_key)

# %% [markdown]
# ### Example 1: Generate a Simple Causal Graph
# 
# Let's generate a causal graph for a simple relationship between exercise and health:

# %%
# Generate a graph with maximum depth of 3
exercise_health_graph = generator.generate_graph(
    query="Generate a causal graph showing how regular exercise affects physical and mental health",
    depth=3
)

# Display the generated graph
import json
print(json.dumps(exercise_health_graph, indent=2))

# %% [markdown]
# ### Example 2: Generate a More Complex Graph
# 
# Let's try a more complex example with a deeper graph:

# %%
# Generate a more complex graph
climate_graph = generator.generate_graph(
    query="Generate a causal graph showing the relationships between climate change, human activities, and environmental impacts",
    depth=5
)

# Display the generated graph
print(json.dumps(climate_graph, indent=2))

# %% [markdown]
# ### Saving Generated Graphs
# 
# We can save the generated graphs to JSON files for later use:

# %%
# Save the generated graphs
generator.save_graph(exercise_health_graph, path='../data/graphs', name='exercise_health')
generator.save_graph(climate_graph, path='../data/graphs', name='climate_change')

# %% [markdown]
# ### Visualizing the Generated Graphs
# 
# Let's create a function to visualize the generated graphs using NetworkX:

# %%
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

# %%
# Visualize the exercise and health graph
visualize_graph(exercise_health_graph)

# %%
# Visualize the climate change graph
visualize_graph(climate_graph) 