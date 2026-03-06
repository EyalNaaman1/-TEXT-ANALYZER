import json
from utils import get_processed_sentences, load_kseq_query  # type: ignore
from typing import Any, List, Dict, Tuple
from task1 import Task1  # type: ignore

class Task4:
    def __init__(self, args: Any) -> None:
        """Initialize Task4 and load processed sentences."""
        self._processed_sentences = get_processed_sentences(args)
        self._task1 = Task1(args) if not getattr(args, 'preprocessed', None) else None
        self._args = args

    def clean_kseq_keys(self, k_seq_keys: List[List[str]]) -> List[List[str]]:
        """Cleans K-seq keys using Task1's text processing."""
        if not self._task1:
            return k_seq_keys 

        return [
            self._task1.clean_text(" ".join(row)).split()
            for row in k_seq_keys
            if self._task1.clean_text(" ".join(row)).strip()
        ]

    def build_index(self, k_seq_keys: List[List[str]], sentences: List[List[str]]) -> List[Tuple[str, List[List[str]]]]:
        """Build a dictionary that maps each K-seq to the sentences that contain it"""
        sentence_dict = {idx: set(sentence) for idx, sentence in enumerate(sentences)}
        index = {}

        for k_seq_key in k_seq_keys:
            k_seq_str = " ".join(k_seq_key) 
            matching_sentences = []

            for idx, words in sentence_dict.items():
                if set(k_seq_key).issubset(words):
                    matching_sentences.append(sentences[idx])
            if matching_sentences:
                index[k_seq_str] = sorted(matching_sentences, key=lambda x: " ".join(x).lower())

        return sorted(index.items(), key=lambda item: item[0]) 

    def task_4(self) -> None:
        """run Task 4"""
        try:
            sentences = self._processed_sentences
            k_seq_keys = load_kseq_query(self._args.qsek_query_path) 
            k_seq_keys = self.clean_kseq_keys(k_seq_keys)

            k_seq_matches = self.build_index(k_seq_keys, sentences)

            output = {
                "Question 4": {
                    "K-Seq Matches": k_seq_matches
                }
            }

            json_output = json.dumps(output, indent=4, ensure_ascii=False)
            print(json_output)

        except Exception as e:
            print("Unexpected error:", e)
