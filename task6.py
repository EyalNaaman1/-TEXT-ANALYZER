import json
from collections import defaultdict
from typing import Any, Dict, List, Set, Tuple
from task1 import Task1  # type: ignore
from utils import get_processed_sentences, create_name_mapping  # type: ignore

class Task6:
    def __init__(self, args: Any) -> None:
        """Initialize Task6"""
        self.window_size: Any = getattr(args, "windowsize", None)
        self.threshold: Any = getattr(args, "threshold", None)
        self.sentences: List[List[str]] = get_processed_sentences(args)
        self.processed_names: List[Tuple[List[str], List[List[str]]]] = Task1(args).process_names() 

    def build_person_graph(self) -> List[List[List[str]]]:
        """Constructs a graph of people appearing together in sentence windows"""
        name_mapping: Dict[str, str] = create_name_mapping(self.processed_names)  
        connection_counts: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))

        if not isinstance(self.window_size, int) or self.window_size <= 0:
            raise ValueError("Invalid window size: must be a positive integer.")
        if not isinstance(self.threshold, int) or self.threshold < 0:
            raise ValueError("Invalid threshold: must be a non-negative integer.")

        for start in range(len(self.sentences) - self.window_size + 1):
            window: List[List[str]] = self.sentences[start:start + self.window_size]
            window_people: Set[str] = set()

            for sentence in window:
                sentence_words: Set[str] = set(sentence)
                for key, mapped_name in name_mapping.items():
                    if set(key.split()) & sentence_words:
                        window_people.add(mapped_name)

            sorted_people: List[str] = sorted(window_people)
            for i in range(len(sorted_people)):
                for j in range(i + 1, len(sorted_people)):
                    connection_counts[sorted_people[i]][sorted_people[j]] += 1

        edges: List[List[List[str]]] = [
            [p1.split(), p2.split()]
            for p1, connections in connection_counts.items()
            for p2, count in connections.items()
            if count >= self.threshold
        ]

        return sorted(edges)

    def task_6(self) -> None:
        """run task 6"""
        person_connections: List[List[List[str]]] = self.build_person_graph()
        
        json_output = json.dumps({"Question 6": {"Pair Matches": person_connections}}, indent=4)
        print(json_output)