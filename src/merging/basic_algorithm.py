import json
import sys

def load_graph(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def load_main_graph(filename, new):
    return

def merge_graph(graph, main_graph):
    return

def save_main_graph(graph, is_new):
    return

if __name__ == "__main__":
    # arguments: merged_filename, new/existing, graph_filenames...
    if len(sys.argv) < 3:
        print("Usage: python basic_algorithm.py merged_filename new/existing graph_filenames...")
        return 0
    merged_filename = sys.argv[0]
    is_new = sys.argv[1] == "new"
    main_graph = load_main_graph(merged_filename, is_new)

    for i in range(2,len(sys.argv)):
        graph_filename = sys.argv[i]
        # graph = load_graph("../../data/graphs/cognitive_science_graphs/Attention.json")
        graph = load_graph(graph_filename)
        merge_graph(graph, main_graph)

    save_main_graph(main_graph, is_new)
