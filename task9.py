import json
from collections import defaultdict, deque
from typing import Any, Dict, List, Set
from utils import get_processed_sentences  # type: ignore

class Task9:
    def __init__(self, args: Any) -> None:
        """Initializes Task9 with the provided arguments."""
        self._processed_sentences: List[List[str]] = get_processed_sentences(args) 
        self.threshold: Any = getattr(args, 'threshold', None)

    def build_sentence_graph(self, sentences: List[List[str]]) -> Dict[int, Set[int]]:
        """Creates a graph efficiently using a dictionary"""
        graph: Dict[int, Set[int]] = defaultdict(set)
        word_to_sentences: Dict[str, Set[int]] = defaultdict(set)

        for idx, sentence in enumerate(sentences):
            for word in sentence:
                word_to_sentences[word].add(idx)

        for idx, words in enumerate(sentences):
            candidate_sentences = set()
            for word in words:
                candidate_sentences.update(word_to_sentences[word])
            for j in candidate_sentences:
                if j != idx and len(set(words) & set(sentences[j])) >= self.threshold:
                    graph[idx].add(j)
                    graph[j].add(idx)

        return graph


    def find_sentence_groups(self, graph: Dict[int, Set[int]]) -> List[Set[int]]:
        """Finds connected components in the sentence graph using BFS."""
        visited: Set[int] = set()
        groups: List[Set[int]] = []

        def bfs(start: int) -> Set[int]:
            queue: deque[int] = deque([start])
            group: Set[int] = set()
            while queue:
                node = queue.popleft()
                if node in visited:
                    continue
                visited.add(node)
                group.add(node)
                queue.extend(graph[node] - visited)
            return group

        for node in range(len(self._processed_sentences)):
            if node not in visited:
                groups.append(bfs(node))

        return groups

    def task_9(self) -> None:
        """run task 9"""
        sentences = self._processed_sentences

        if not isinstance(self.threshold, int) or self.threshold < 0:
            raise ValueError("Threshold must be a non-negative number.")

        graph = self.build_sentence_graph(sentences)
        groups = self.find_sentence_groups(graph)

        sorted_groups = sorted(groups, key=lambda g: (len(g), sorted(sentences[i] for i in g)))

        results: Dict[str, Dict[str, List[Any]]] = {
            "Question 9": {
                "group Matches": [
                    [f"Group {i+1}", sorted([sentences[j] for j in group])]
                    for i, group in enumerate(sorted_groups)
                ]
            }
        }

        json_output = json.dumps(results, indent=4, ensure_ascii=False)
        print(json_output)