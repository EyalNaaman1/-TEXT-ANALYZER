import json
import os
import sys
from collections import defaultdict
from typing import Any, Dict, List, Set, Tuple, Union
from task1 import Task1  # type: ignore

### ======================= load func ======================= ###

def get_processed_sentences(args: Any) -> List[List[str]]:
    """Load preprocessed sentences if available, otherwise process them using Task1."""
    
    if not getattr(args, 'preprocessed', None):  
        if not getattr(args, 'names', None):
            args.names = []
        return Task1(args).process_sentences()

    processed_sentences: List[List[str]] = []

    for filepath in args.preprocessed:
        if not os.path.isfile(filepath):  
            raise ValueError("Invalid input - preprocessed ")  

        try:
            with open(filepath, 'r', encoding="utf-8") as file:
                data: Dict[str, Any] = json.load(file)
                processed_sentences = data.get("Question 1", {}).get("Processed Sentences", [])

                if not processed_sentences:  
                    raise ValueError(f"Invalid input: Preprocessed file is empty or missing data")  

                return processed_sentences  

        except json.JSONDecodeError:
            raise ValueError(f"Invalid input: Preprocessed file is not a valid JSON file")  

    raise ValueError("Invalid input: No valid preprocessed files found") 

def load_json(filepath: str) -> Dict[str, Any]:
    """Load a JSON file and return its content."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    if os.path.getsize(filepath) == 0:
        raise ValueError(f"File is empty: {filepath}")

    with open(filepath, 'r', encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format: {filepath}")

def load_people_data(args: Any) -> List[Tuple[List[str], List[List[str]]]]:
    """Load processed people names from Task1 or a preprocessed file."""
    if not getattr(args, 'preprocessed', None):
        if not getattr(args, 'sentences', None):
            args.sentences = []
        return Task1(args).process_names()

    if args.preprocessed:
        for filepath in args.preprocessed:
            try:
                data: Dict[str, Any] = load_json(filepath)
                processed_names: List[Tuple[List[str], List[List[str]]]] = data.get("Question 1", {}).get("Processed Names", [])
                if processed_names:
                    return processed_names
            except Exception as e:
                print(f"Error loading preprocessed names from {filepath}: {e}")
                sys.exit(1)

    return Task1(args).process_names()


def load_people_pairs(filepath: str) -> List[List[str]]:
    """Load people pairs from a JSON file."""
    try:
        data: Union[Dict[str, Any], List[Any]] = load_json(filepath)
        raw_pairs = data.get("keys", []) if isinstance(data, dict) else data
        return [list(pair) for pair in raw_pairs]  
    except Exception as e:
        print(f"Error loading people pairs from {filepath}: {e}")
        sys.exit(1)

def load_kseq_query(filepath: str) -> List[List[str]]:
    """Load K-seq query keys from a JSON file."""
    try:
        data: Dict[str, Any] = load_json(filepath)
        return data.get("keys", [])
    except Exception as e:
        print(f"Error loading K-seq query from {filepath}: {e}")
        sys.exit(1)


### ======================= help func ======================= ###

def create_name_mapping(people_data: List[Tuple[List[str], List[List[str]]]]) -> Dict[str, str]:
    """
    Creates a dictionary mapping names, nicknames, and parts of multi-word names to the full name.
    Ensures that standalone names are not mistakenly overridden while keeping Task 3 functional.
    """
    try:
        name_mapping: Dict[str, str] = {}
        standalone_counts: Dict[str, int] = defaultdict(int) 

        for person in people_data:
            full_name = " ".join(person[0])  # Convert full name to a single string
            name_mapping[full_name] = full_name  # Map full name to itself

            for part in person[0]:
                standalone_counts[part] += 1

        # Add mappings for nicknames and individual words
        for person in people_data:
            full_name = " ".join(person[0])
            nicknames = person[1]

            # Map nicknames to the full name
            for nickname in nicknames:
                nickname_str = " ".join(nickname)
                name_mapping[nickname_str] = full_name

            # Map each word in the full name
            for part in person[0]:
                if standalone_counts[part] == 1:  # Only map if it's unique
                    name_mapping[part] = full_name

        return name_mapping
    except Exception as e:
        print("Unexpected error:", e)
        sys.exit(1)


def build_adjacency_list(pair_matches: List[Tuple[str, str]]) -> Dict[str, Set[str]]:
    """Convert a list of pair matches into an adjacency list."""
    graph: Dict[str, Set[str]] = defaultdict(set)
    for p1, p2 in pair_matches:
        graph[p1].add(p2)
        graph[p2].add(p1)
    return graph