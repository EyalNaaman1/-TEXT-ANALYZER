import json
import sys
from collections import defaultdict
from typing import Dict, List, Tuple, Any
from utils import get_processed_sentences  # type: ignore

class Task2:
    def __init__(self, args: Any) -> None:
        """Initialize Task2 and load processed sentences."""
        self._max_k: int = args.maxk
        self._processed_sentences: List[List[str]] = get_processed_sentences(args)

    @staticmethod
    def count_sequences(sentences: List[List[str]], max_k: int) -> Dict[str, List[List[Any]]]:
        """Counts k-sequences in processed sentences"""
        k_seq_counts: Dict[int, Dict[Tuple[str, ...], int]] = {k: defaultdict(int) for k in range(1, max_k + 1)}

        for sentence in sentences:
            for k in range(1, max_k + 1):
                for i in range(len(sentence) - k + 1):
                    k_seq = tuple(sentence[i:i + k])  
                    k_seq_counts[k][k_seq] += 1

        sorted_k_seq_counts: Dict[str, List[List[Any]]] = {
            f"{k}_seq": [
                [' '.join(key), value] for key, value in sorted(counts.items(), key=lambda x: ' '.join(x[0]))
            ]
            for k, counts in k_seq_counts.items()
        }

        return sorted_k_seq_counts

    def _format_output(self, k_seq_counts: Dict[str, List[List[Any]]], max_k: int) -> Dict[str, Dict[str, List[Any]]]:
        """Formats the output in the expected structure."""
        output: Dict[str, Dict[str, List[Any]]] = {
            f"Question {2}": {
                f"{max_k}-Seq Counts": [
                    [
                        f"{k}_seq",
                        [
                            ["".join(seq), count]
                            for seq, count in k_seq_counts.get(f"{k}_seq", [])
                        ]
                    ]
                    for k in range(1, max_k + 1)
                ]
            }
        }
        return output
    
    def task_2(self) -> None:
        """run task 2"""
        try:
            if not isinstance(self._max_k, int) or self._max_k < 1:
                raise ValueError(f"Invalid _max_k: {self._max_k}. Must be a positive integer.")
            k_seq_counts = self.count_sequences(self._processed_sentences, self._max_k)
            output = self._format_output(k_seq_counts, self._max_k)
            
            json_output = json.dumps(output, indent=4, ensure_ascii=False)
            print(json_output)

        except Exception as e:
            print("Unexpected error:", e)
            sys.exit(1)