import json
import sys

def load_graph(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def load_main_graph(filename):
    return

def merge_graph(graph, main_graph):
    return

def save_main_graph(filename, graph):
    return

if __name__ == "__main__":
    # arguments: merged_filename, graph_filenames...
    if len(sys.argv) < 2:
        print("Usage: python basic_algorithm.py merged_filename graph_filenames...")
        return 0
    merged_filename = sys.argv[0]
    main_graph = load_main_graph(merged_filename)

    for i in range(2,len(sys.argv)):
        graph_filename = sys.argv[i]
        # graph = load_graph("../../data/graphs/cognitive_science_graphs/Attention.json")
        graph = load_graph(graph_filename)
        merge_graph(graph, main_graph)

    save_main_graph(merged_filename, main_graph)
