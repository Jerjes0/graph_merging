import os
import json
import difflib
from collections import defaultdict
from typing import Dict, Any, List, Tuple

class GraphMerger:
    def __init__(self,
                 graph_path: str,
                 synonym_threshold: float = 0.8):
        """
        Args:
            graph_path: path to directory of JSON graph files
            synonym_threshold: 0–1 string‐similarity threshold to merge synonyms
        """
        self.synonym_threshold = synonym_threshold
        self.graph: Dict[str, Dict[str, Any]] = {}
        self._read_graphs(graph_path)

        # placeholders, filled when you call clean_synonyms()
        self.updated_graph: Dict[str, Dict[str, Any]]
        self.synonym_map: Dict[str, List[str]]

    def _read_graphs(self, graph_path: str) -> None:
        """Read every .json in graph_path and append into self.graph."""
        for fname in sorted(os.listdir(graph_path)):
            if not fname.endswith('.json'):
                continue
            full = os.path.join(graph_path, fname)
            with open(full, 'r', encoding='utf-8') as f:
                g = json.load(f)
            # If keys collide, the later file wins
            self.graph.update(g)

    def clean_synonyms(self) -> Tuple[Dict[str, Dict[str, Any]],
                                     Dict[str, List[str]]]:
        """
        1) Finds clusters of “synonymous” node names via SequenceMatcher
        2) Picks the first name in each cluster as the canonical label
        3) Rewrites self.graph into self.updated_graph using only canonicals
        4) Builds self.synonym_map: canonical → [other names merged into it]
        
        Returns:
            (updated_graph, synonym_map)
        """
        # 1) collect all unique node names (keys + children)
        all_names = set(self.graph.keys())
        for data in self.graph.values():
            all_names.update(data.get('children', []))
        sorted_names = sorted(all_names)

        # 2) cluster via simple threshold-based grouping
        canonical: Dict[str, str] = {}
        for name in sorted_names:
            if name in canonical:
                continue
            canonical[name] = name
            for other in sorted_names:
                if other in canonical:
                    continue
                sim = difflib.SequenceMatcher(
                    None, name.lower(), other.lower()
                ).ratio()
                if sim >= self.synonym_threshold:
                    canonical[other] = name

        # build synonym_map (excluding the canonical itself)
        synonym_map: Dict[str, List[str]] = defaultdict(list)
        for nm, canon in canonical.items():
            if nm != canon:
                synonym_map[canon].append(nm)

        # 3) rewrite graph keys & children
        updated: Dict[str, Dict[str, Any]] = {}
        for raw, data in self.graph.items():
            canon = canonical[raw]
            # initialize the node if first time
            if canon not in updated:
                # take description from whichever raw maps here first
                desc = self.graph.get(canon, data).get('description', '')
                updated[canon] = {'children': [], 'description': desc}
            # map children through canonical
            for ch in data.get('children', []):
                chcanon = canonical[ch]
                updated[canon]['children'].append(chcanon)

        # de‐duplicate children lists
        for node, d in updated.items():
            # preserve order but remove dupes
            seen = set()
            uniq = []
            for c in d['children']:
                if c not in seen:
                    seen.add(c)
                    uniq.append(c)
            d['children'] = uniq

        # store on self 
        self.updated_graph = updated
        self.synonym_map = dict(synonym_map)
        return

    def index_updated_graph(self, base_index: int = 1001) -> Dict[int, Dict[str, Any]]:
        """
        Create an indexed version of self.updated_graph where each concept string
        is replaced by a unique integer ID starting at base_index.

        Also populates:
          - self.index_map: Dict[str, int] mapping concept → ID
          - self.rev_index_map: Dict[int, str] mapping ID → concept
          - self.indexed_graph: Dict[int, Dict[str, Any]] the resulting graph
        """
        # 1) collect every concept name (nodes + children)
        all_concepts = set(self.updated_graph.keys())
        for data in self.updated_graph.values():
            all_concepts.update(data['children'])

        # 2) sort for stable ordering and assign IDs
        concepts = sorted(all_concepts)
        self.index_map = {concept: idx + base_index
                          for idx, concept in enumerate(concepts)}
        self.rev_index_map = {v: k for k, v in self.index_map.items()}

        # 3) build the indexed graph
        indexed = {}
        for concept, data in self.updated_graph.items():
            cid = self.index_map[concept]
            child_ids = [self.index_map[ch] for ch in data['children']]
            indexed[cid] = {
                'children': child_ids,
                'description': data['description']
            }

        self.indexed_graph = indexed
        return 

    def save_indexed_graph(self, path: str):
        """
        Save indexed_graph and index_map as json files in the provided path.
        
        Args:
            path (str): The path to save the json files
        """
        import json
        with open(path + '/indexed_graph.json', 'w') as f:
            json.dump(self.indexed_graph, f)
        with open(path + '/index_map.json', 'w') as f:
            json.dump(self.index_map, f)

