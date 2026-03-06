import json
from typing import Any, Dict, List, Set, Tuple, Union
from utils import get_processed_sentences, load_people_data  # type: ignore

class PersonContext:
    """Class to store person related K-seqs."""
    
    def __init__(self, name: str) -> None:
        self.name = name
        self.k_seqs: Set[Tuple[str, ...]] = set()

    def add_k_seqs(self, k_seqs: Set[Tuple[str, ...]]) -> None:
        """Add K-seqs to the person context."""
        self.k_seqs.update(k_seqs)

    def get_sorted_k_seqs(self) -> List[Tuple[str, ...]]:
        """Return sorted K-seqs."""
        return sorted(self.k_seqs)


class Task5:
    def __init__(self, args: Any) -> None:
        """Initialize Task5"""
        self.k_max: int = args.maxk  # Maximal K-seq length (N)
        self.sentences: List[List[str]] = get_processed_sentences(args)
        self.processed_names: List[Tuple[List[str], List[List[str]]]] = load_people_data(args)

    def find_person_contexts(self) -> List[Tuple[str, List[Tuple[str, ...]]]]:
        """Extract person contexts"""
        self.processed_names.sort(key=lambda x: " ".join(x[0]))  # Sort by full name alphabetically
        person_contexts: Dict[str, PersonContext] = {}

        for sentence in self.sentences:
            words_set: Set[str] = set(sentence)  # Convert sentence to a set of words

            for name, nicknames in self.processed_names:
                name_key: str = " ".join(name).lower()  

                if self.is_name_in_sentence(name, nicknames, words_set):
                    k_seqs_for_person: Set[Tuple[str, ...]] = self.collect_k_seqs(sentence)

                    if name_key not in person_contexts:
                        person_contexts[name_key] = PersonContext(name_key)

                    person_contexts[name_key].add_k_seqs(k_seqs_for_person)

        # Sort results lexicographically
        return [(name, context.get_sorted_k_seqs()) for name, context in sorted(person_contexts.items())]

    def is_name_in_sentence(self, names: List[str], nicknames: List[List[str]], words_set: Set[str]) -> bool:
        """Check if the person's name or any nickname appears in the sentence."""
        all_names: list[Union[list[str], str]] = names + nicknames  # Combine names and nicknames

        for name in all_names:
            name_words: Set[str] = set(name) if isinstance(name, list) else {name} 
            if name_words.issubset(words_set):  # Check if all words appear in the sentence
                return True

        return False

    def collect_k_seqs(self, sentence: List[str]) -> Set[Tuple[str, ...]]:
        """Generate all K-seqs up to N."""
        return {
            tuple(sentence[i:j]) 
            for i in range(len(sentence)) 
            for j in range(i + 1, min(i + self.k_max + 1, len(sentence) + 1))
        }

    def task_5(self) -> None:
        """run task 5"""
        try:
            person_contexts = self.find_person_contexts()

            output: Dict[str, Dict[str, List[Tuple[str, List[Tuple[str, ...]]]]]] = {
                "Question 5": {
                    "Person Contexts and K-Seqs": person_contexts
                }
            }

            json_output = json.dumps(output, indent=4, ensure_ascii=False)
            print(json_output)

        except Exception as e:
            print("Unexpected error:", e)