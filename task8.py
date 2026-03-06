import json
from collections import deque
from typing import Any, Dict, List, Set, Tuple
from task6 import Task6  # type: ignore
from utils import load_people_pairs, load_json, build_adjacency_list  # type: ignore

class Task8:
    def __init__(self, args: Any) -> None:
        """Initialize Task8."""
        
        self.k: int = args.fixed_length
        self.people_connections_path: str = args.pairs
        self._args: Any = args

        self.graph: Dict[str, Set[str]] = self.load_graph()

        if not self.people_connections_path:
            raise ValueError("Missing --pairs")

    def load_graph(self) -> Dict[str, Set[str]]:
        """Loads a preprocessed graph if available, otherwise constructs it from Task6."""
        pair_matches: List[Tuple[str, str]] = []
        if getattr(self._args, 'preprocessed', None):
            if self._args.preprocessed:
                raw_data = load_json(self._args.preprocessed).get("Question 6", {}).get("Pair Matches", [])
                pair_matches = [(str(p1), str(p2)) for p1, p2 in raw_data]
            else:
                raw_data = Task6(self._args).build_person_graph()
                pair_matches = [(" ".join(p1), " ".join(p2)) for p1, p2 in raw_data]  # Convert lists to strings
        else:
            raw_data = Task6(self._args).build_person_graph()
            pair_matches = [(" ".join(p1), " ".join(p2)) for p1, p2 in raw_data]  # Convert lists to strings

        return build_adjacency_list(pair_matches) 

    def bfs_exact_k(self, start: str, target: str) -> bool:
        """Checks if a path of exactly K exists between two nodes using BFS."""
        if self.k is None:
            raise ValueError("K must be specified for fixed-length path search.")
        if self.k == 0:
            return start == target
        if self.k == 1:
            return target in self.graph.get(start, set())
        
        if self.k < 0:
            raise ValueError("Invalid input")
        
        queue: deque[Tuple[str, int, Set[str]]] = deque([(start, 0, {start})])  

        while queue:
            current, depth, visited = queue.popleft()
            if depth == self.k:
                if current == target:
                    return True
                continue 

            for neighbor in self.graph.get(current, set()):
                if neighbor not in visited:
                    queue.append((neighbor, depth + 1, visited | {neighbor}))

        return False

    def task_8(self) -> None:
        """run task 8"""
        people_pairs: list[list[str]] = load_people_pairs(self.people_connections_path)

        results: Dict[str, Dict[str, List[List[Any]]]] = {
        "Question 8": {
            "Pair Matches": sorted(
                [[*sorted([p1, p2]), self.bfs_exact_k(p1, p2)] for p1, p2 in people_pairs],
                key=lambda x: (x[0].lower(), x[1].lower())
            )
        }
    }

        json_output = json.dumps(results, indent=4, ensure_ascii=False)
        print(json_output)
