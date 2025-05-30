import json
import sys
import os
import copy

def load_graph(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    else:
        return {}

def merge_graph(graph, main_graph):
    nodes = list(graph.keys())
    pairs = {}
    for node in nodes:
        pairs[node] = copy.deepcopy(nodes)
    for node1 in graph.keys():
        if not node1 in main_graph:
            main_graph[node1] = {}
        for node2 in graph[node1]["children"]:
            pairs[node1].remove(node2)
            pairs[node2].remove(node1)

            # add the relation to merged graph
            if not node2 in main_graph:
                main_graph[node2] = {}
            if not node2 in main_graph[node1].keys():
                main_graph[node1][node2] = {
                    "isChild": 1,
                    "isParent": 0,
                    "noRelation": 0
                }
            else:
                main_graph[node1][node2]["isChild"] += 1
            if not node1 in main_graph[node2].keys():
                main_graph[node2][node1] = {
                    "isChild": 0,
                    "isParent": 1,
                    "noRelation": 0
                }
            else:
                main_graph[node2][node1]["isParent"] += 1
    for node1 in pairs.keys():
        for node2 in pairs[node1]:
            if node1 == node2:
                continue
            if not node1 in main_graph:
                main_graph[node1] = {}
            if not node2 in main_graph[node1].keys():
                main_graph[node1][node2] = {
                    "isChild": 0,
                    "isParent": 0,
                    "noRelation": 1
                }
            else:
                main_graph[node1][node2]["noRelation"] += 1

def save_main_graph(filename, graph):
    with open(filename, 'w') as file:
        json.dump(graph, file, indent=4)

if __name__ == "__main__":
    # arguments: merged_filename, graph_filenames...
    if len(sys.argv) < 3:
        print("Usage: python basic_algorithm.py merged_filename graph_filenames...")
    else:
        merged_filename = sys.argv[1]
        main_graph = load_graph(merged_filename)

        for i in range(2,len(sys.argv)):
            graph_filename = sys.argv[i]
            graph = load_graph(graph_filename)
            merge_graph(graph, main_graph)

        save_main_graph(merged_filename, main_graph)
