import csv
import re
import os
import sys
import json
from typing import Any, Dict, List, Optional, Set, Tuple

class Task1:
	def __init__(self, args: Any) -> None:
		"""Initialize Task1."""
		self._sentences_file: str = args.sentences
		self._names_file: str = args.names
		self._remove_words: Set[str] = self._load_remove_words(args.removewords)

	def _load_remove_words(self, filepath: Optional[str]) -> Set[str]:
		"""Load remove words from a JSON file."""
		if not filepath:
			print("Invalid remove words input")
			sys.exit(1)
		
		if not os.path.isfile(filepath):
			print("Invalid remove words input")
			sys.exit(1)

		with open(filepath, 'r', encoding="utf-8") as file:
			words: Set[str] = {line.strip().lower() for line in file if line.strip()}
	
		return words if words else set()

	def _load_file(self, file_path: Optional[str]) -> List[Dict[str, str]]:
		"""Load a JSON file."""
		if not file_path:
			print("Invalid input -sentences")
			sys.exit(1)
		
		if not os.path.isfile(file_path):
			print("Invalid input -sentences")
			sys.exit(1)
	
		with open(file_path, 'r', encoding="utf-8") as file:
			content: List[Dict[str, str]] = list(csv.DictReader(file))

		if not content:
			raise ValueError(f"File is empty: {file_path}")

		return content

	def clean_text(self, text: Optional[str]) -> str:
		"""clean text as requested"""
		if not text:
			return ""
		text = text.lower()
		text = re.sub(r'[^\w\s]', ' ', text)
		words: List[str] = text.split()
		words = [word for word in words if word not in self._remove_words]
		return " ".join(words).strip()

	def process_sentences(self) -> List[List[str]]:
		"""clean the sentences if everything is right"""
		sentences_data: List[Dict[str, str]] = self._load_file(self._sentences_file)
		if not sentences_data or 'sentence' not in sentences_data[0]:
			raise ValueError("Missing 'sentence' column in sentences file.")

		sentences: List[List[str]] = [
			self.clean_text(row['sentence'].strip()).split() for row in sentences_data
			if 'sentence' in row and self.clean_text(row['sentence'].strip())
		]
		return sentences  

	def process_names(self) -> List[Tuple[List[str], List[List[str]]]]:
		"""clean the names if everything is right"""
		people_data: List[Dict[str, str]] = self._load_file(self._names_file)
		if not people_data or 'Name' not in people_data[0] or 'Other Names' not in people_data[0]:
			raise ValueError("Missing 'Name' or 'Other Names' column in people file.")

		processed_people: List[Tuple[List[str], List[List[str]]]] = []
		seen_names: Set[Tuple[str, ...]] = set()

		for row in people_data:
			cleaned_name: Tuple[str, ...] = tuple(self.clean_text(row['Name'].strip()).split())

			if not cleaned_name or cleaned_name == ("",):
				continue  

			if cleaned_name in seen_names:
				continue

			nicknames: List[List[str]] = [
				self.clean_text(nickname.strip()).split() for nickname in row['Other Names'].split(',')
				if nickname.strip()
			]
			nicknames = [nick for nick in nicknames if nick]

			processed_people.append((list(cleaned_name), nicknames))
			seen_names.add(cleaned_name)

		return processed_people

	def task_1(self) -> None:
		"""run task 1"""
		try:
			self._processed_sentences: List[List[str]] = self.process_sentences()
			self._processed_names: List[Tuple[List[str], List[List[str]]]] = self.process_names()

			output: Dict[str, Dict[str, Any]] = {
				"Question 1": {
					"Processed Sentences": self._processed_sentences,
					"Processed Names": self._processed_names
				}
			}
			
			json_output = json.dumps(output, indent=4, ensure_ascii=False)
			print(json_output)

		except Exception as e:
			print("Unexpected error:", e)
			sys.exit(1)