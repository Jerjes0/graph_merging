import json
import numpy as np
import os
from copy import deepcopy
from pathlib import Path
from typing import Dict, List, Any

class CausalGraph(object):
    def __init__(self, filename: Path):
        self.filename = filename
        self.graph = None
        # self.node_mapping = {}
        # self.adjacency = {
        #     "isChild": np.array([]),
        #     "isParent": np.array([]),
        #     "noRelation": np.array([]),
        # }
        self.load(self.filename)

    def load(self, filename: Path) -> None:
        with open(filename, 'r') as file:
            self.graph = json.load(file)

        # for i, node in enumerate(graph.keys()):
        #     self.node_mapping[node] = i
        # graph_size = len(self.node_mapping)
        # for r in self.adjacency.keys():
        #     self.adjacency[r] = np.zeros((graph_size, graph_size), dtype=np.int32)
        # for src_node, edge in graph.items():
        #     for dst_node, edge_type in edge.items():
        #         src_idx = self.node_mapping[src_node]
        #         dst_idx = self.node_mapping[dst_node]
        #         for r in edge_type.keys():
        #             self.adjacency[r][src_idx, dst_idx] = edge_type[r]

    def save(self, filename: Path = None) -> None:
        # if filename is None:
        #     filename = self.filename
        # graph = {}
        # for src_node, src_idx in self.node_mapping.items():
        #     graph[src_node] = {}
        #     for dst_node, dst_idx in self.node_mapping.items():
        #         graph[src_node][dst_node] = {}
        #         for r in self.adjacency.keys():
        #             graph[src_node][dst_node][r] = int(self.adjacency[r][src_idx, dst_idx])

        with open(filename, 'w') as file:
            json.dump(self.graph, file, indent=4)

    def parent(self, node: str) -> List[str]:
        if node not in self.graph:
            return []
        return [k for k, v in self.graph[node].items() if v.get("isChild", 0) > 0]

    def merge(self, rhs: 'CausalGraph') -> None:
        node_type = {}
        common_node = []
        for node in self.graph.keys():
            if node in rhs.graph.keys():
                node_type[node] = "common"
                common_node.append(node)
            else:
                node_type[node] = "left"
        for node in rhs.graph.keys():
            if node not in node_type:
                node_type[node] = "right"
        common_node = set(common_node)
        for node in node_type.keys():
            if node_type[node] == "common":
                node_type[node] = "external"
                self_parent = set(self.parent(node))
                rhs_parent = set(rhs.parent(node))
                if len(self_parent) > 0 and self_parent.issubset(common_node):
                    node_type[node] = "internal_left"
                if len(rhs_parent) > 0 and rhs_parent.issubset(common_node):
                    if node_type[node] == "internal_left":
                        node_type[node] = "internal_both"
                    else:
                        node_type[node] = "internal_right"

        merged_graph = {}

        # Retain noRelation relationships.
        for src_node in self.graph.keys():
            if src_node not in merged_graph:
                merged_graph[src_node] = {}
            for dst_node, edge_type in self.graph[src_node].items():
                if dst_node not in merged_graph[src_node]:
                    merged_graph[src_node][dst_node] = {}
                if edge_type["noRelation"] == 1:
                    merged_graph[src_node][dst_node] = {"isChild": 0, "isParent": 0, "noRelation": 1}
        for src_node in rhs.graph.keys():
            if src_node not in merged_graph:
                merged_graph[src_node] = {}
            for dst_node, edge_type in rhs.graph[src_node].items():
                if dst_node not in merged_graph[src_node]:
                    merged_graph[src_node][dst_node] = {}
                if edge_type["noRelation"] == 1:
                    merged_graph[src_node][dst_node] = {"isChild": 0, "isParent": 0, "noRelation": 1}

        # Merge isChild and isParent relationships.
        for node in node_type.keys():
            if node not in merged_graph:
                merged_graph[node] = {}
            if node_type[node] == "internal_both":
                node_type[node] = np.random.choice(["internal_left", "internal_right"])
            if node_type[node] in ["left", "internal_left", "external"]:
                for pa_node in self.parent(node):
                    merged_graph[node][pa_node] = {"isChild": 1, "isParent": 0, "noRelation": 0}
                    merged_graph[pa_node][node] = {"isChild": 0, "isParent": 1, "noRelation": 0}
            if node_type[node] in ["right", "internal_right", "external"]:
                for pa_node in rhs.parent(node):
                    merged_graph[node][pa_node] = {"isChild": 1, "isParent": 0, "noRelation": 0}
                    merged_graph[pa_node][node] = {"isChild": 0, "isParent": 1, "noRelation": 0}

        # Eliminate cycles by simulated annealing.
        temperature = 10
        decay = 0.9
        patience = 50

        def compute_energy(graph: Dict[str, Any], hierarchy: Dict[str, int]) -> float:
            energy = 0.0
            for src_node, edges in graph.items():
                for dst_node, edge_type in edges.items():
                    if edge_type["isChild"] == 1 and hierarchy[src_node] <= hierarchy[dst_node]:
                        energy += 1.0
            return energy

        hierarchy = {}
        for node in merged_graph.keys():
            hierarchy[node] = np.random.randint(0, len(merged_graph))
        best_hierarchy = hierarchy
        energy = compute_energy(merged_graph, hierarchy)
        best_energy = energy
        patience_count = 0
        while patience_count < patience:
            patience_count += 1
            new_hierarchy = deepcopy(hierarchy)
            node = np.random.choice(list(merged_graph.keys()))
            new_hierarchy[node] = np.random.randint(0, len(merged_graph))
            new_energy = compute_energy(merged_graph, new_hierarchy)
            if new_energy < energy or np.random.rand() < np.exp((energy - new_energy) / temperature):
                hierarchy = new_hierarchy
                energy = new_energy
                if energy < best_energy:
                    best_energy = energy
                    best_hierarchy = hierarchy
                    patience_count = 0
            temperature *= decay

        for src_node, edges in merged_graph.items():
            for dst_node, edge_type in edges.items():
                if edge_type["isChild"] == 1 and best_hierarchy[src_node] <= best_hierarchy[dst_node]:
                    merged_graph[src_node][dst_node] = {"isChild": 0, "isParent": 0, "noRelation": 1}
                    merged_graph[dst_node][src_node] = {"isChild": 0, "isParent": 0, "noRelation": 1}

        self.graph = merged_graph

if __name__ == "__main__":
    graph1 = CausalGraph(Path("graph1.json"))
    graph2 = CausalGraph(Path("graph2.json"))
    graph1.merge(graph2)
    graph1.save(Path("merged_graph.json"))
