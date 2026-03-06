import json
import sys
from collections import deque
from typing import Any, Dict, List, Set, Tuple
from task6 import Task6  # type: ignore
from utils import load_people_pairs, load_json, build_adjacency_list  # type: ignore

class Task7:
	def __init__(self, args: Any) -> None:
		"""Initialize Task7."""
		self.max_distance: int = args.maximal_distance
		self.people_connections_path: str = args.pairs
		self._args: Any = args
		self.graph: Dict[str, Set[str]] = self.load_graph()

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

	@staticmethod
	def bfs(graph: Dict[str, Set[str]], start: str, target: str, max_depth: int) -> bool:
		"""Performs BFS to check if a path exists between start and target within max_depth"""
		if start == target:
			return True

		queue: deque[Tuple[str, int]] = deque([(start, 0)])
		visited: Set[str] = {start}

		while queue:
			current, depth = queue.popleft()
			if depth >= max_depth:
				continue

			for neighbor in graph.get(current, set()):
				if neighbor == target:
					return True
				if neighbor not in visited:
					visited.add(neighbor)
					queue.append((neighbor, depth + 1))

		return False

	def task_7(self) -> None:
		"""Run Task 7"""
		try:
			people_pairs: list[list[str]] = load_people_pairs(self.people_connections_path)

			results: Dict[str, Dict[str, List[List[Any]]]] = {
				"Question 7": {
				"Pair Matches": sorted(
					[[*sorted([p1, p2]), self.bfs(self.graph, p1, p2, self.max_distance)] for p1, p2 in people_pairs],
					key=lambda x: (x[0].lower(), x[1].lower())
					)
				}
			}
		
			json_output = json.dumps(results, indent=4, ensure_ascii=False)
			print(json_output)

		except Exception as e:
			print(f"Error executing Task 7: {e}")
			sys.exit(1)