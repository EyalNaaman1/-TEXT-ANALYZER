import json
import sys
from typing import Any, Dict, List, Tuple
from task1 import Task1  # type: ignore
from task2 import Task2  # type: ignore
from utils import get_processed_sentences, create_name_mapping  # type: ignore

class Task3:
    def __init__(self, args: Any) -> None:
        """Initialize Task3 and load processed sentences."""
        self._processed_sentences: List[List[str]] = get_processed_sentences(args)
        self._args: Any = args
        
    def count_mentions(self, sentences: List[List[str]], people_data: List[Tuple[List[str], List[List[str]]]]) -> Dict[str, int]:
        """Count the number of times each person's name (or nickname) appears in sentences."""
        mention_counts: Dict[str, int] = {}

        name_mapping = create_name_mapping(people_data)
        
        k_seq_counts = Task2.count_sequences(sentences, 1)

        for sentence in k_seq_counts.values():
            for s in sentence:
                word, count = s[0], s[1]  
                if word in name_mapping:  # Check if word exists in our mapping
                    mention = name_mapping[word]
                    if mention not in mention_counts:
                        mention_counts[mention] = 0
                    mention_counts[mention] += count

        mention_counts = {mention: count for mention, count in sorted(mention_counts.items(), key=lambda x: x[0])}
        return mention_counts

    def task_3(self) -> None:
        """Run Task 3"""
        if any(getattr(self._args, attr, None) is None for attr in ['sentences', 'names', 'removewords']):
            print("Invalid input: missing required arguments.")
            sys.exit(1)

        sentences: List[List[str]] = self._processed_sentences

        task1 = Task1(self._args)
        people_data: List[Tuple[List[str], List[List[str]]]] = task1.process_names()  

        mention_counts = self.count_mentions(sentences, people_data)

        output: Dict[str, Dict[str, List[List[Any]]]] = {
            "Question 3": {
                "Name Mentions": [[name, count] for name, count in mention_counts.items()]
            }
        }

        json_output = json.dumps(output, indent=4, ensure_ascii=False)
        print(json_output)