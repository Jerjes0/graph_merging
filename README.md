# Graph Merging Module - Causal Inference Agent

This repository contains the graph merging module implementation for the Causal Inference Agent project, developed as part of DSC291 at UC San Diego.

## Project Overview

The graph merging module is a key component of the Causal Inference Agent project, focusing on the integration and merging of causal graphs to enable more comprehensive causal analysis.

## Collaborators

- Jerjes Aguirre-Chavez
- Zida Jin
- Samyak Karnavat
- Peng Wang

## Course Information

- Course: DSC291
- Institution: UC San Diego

# Causal Inference Agent

This project is part of the DSC 291 - Topics in Causal Inference course at UC San Diego, taught by Professor Biwei Huang.

## Project Overview

The Causal Inference Agent is designed to generate and merge causal graphs using natural language processing. It leverages Google's Gemini API to create causal graphs based on user queries and provides functionality to merge multiple graphs into a unified representation.

## Collaborators

- Jerjes Aguirre Chavez
- [Add other collaborators here]

## Setup Instructions

### 1. Create and Activate Conda Environment

```bash
# Create a new conda environment
conda create -n graph_merging python=3.10 -y

# Activate the environment
conda activate graph_merging
```

### 2. Install Required Packages

```bash
# Install packages from requirements.txt
conda install --file requirements.txt -y

# Install additional required packages
conda install jupyter notebook ipykernel -y
```

### 3. Set Up Jupyter Kernel

```bash
# Register the environment as a Jupyter kernel
python -m ipykernel install --user --name=graph_merging --display-name="Python (graph_merging)"
```

### 4. Get Google Gemini API Key

1. Go to https://makersuite.google.com/app/apikey
2. Create a new API key
3. Copy the API key for use in the notebook

### 5. Run the Notebook

```bash
# Start Jupyter Notebook
jupyter notebook notebooks/generate_dummy_data.ipynb
```

In the notebook:
1. Select the "Python (graph_merging)" kernel from the kernel menu
2. Replace `"YOUR_API_KEY_HERE"` with your actual Gemini API key
3. Run the cells in sequence

## Project Structure

```
graph_merging/
├── data/
│   └── graphs/          # Directory for saved causal graphs
├── notebooks/
│   └── generate_dummy_data.ipynb  # Jupyter notebook for generating graphs
├── src/
│   └── dummy_data/
│       ├── __init__.py
│       └── data_generator.py  # DataGenerator class implementation
└── requirements.txt     # Project dependencies
```

## Usage

The project provides a `DataGenerator` class that can:
1. Generate causal graphs from natural language queries
2. Save graphs to JSON files
3. Visualize graphs using NetworkX

Example usage in Python:
```python
from src.dummy_data import DataGenerator

# Initialize the generator with your API key
generator = DataGenerator(api_key="your-api-key")

# Generate a causal graph
graph = generator.generate_graph(
    query="Generate a causal graph showing how regular exercise affects health",
    depth=3
)

# Save the graph
generator.save_graph(graph, path='data/graphs', name='exercise_health')
```

## Dependencies

The project requires the following main packages:
- google-generativeai
- numpy
- pandas
- networkx
- matplotlib
- seaborn
- jupyter
- notebook
- ipykernel

All dependencies are listed in `requirements.txt` and will be installed automatically when following the setup instructions. 
