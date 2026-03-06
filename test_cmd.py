import pytest
import subprocess
import json
import os
from deepdiff import DeepDiff  # type: ignore


def run_command_and_compare(command, expected_file):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"❌ Command failed: {command}\nError: {e.stderr}")
        return False, None

    try:
        output_json = json.loads(result.stdout.strip())
    except json.JSONDecodeError:
        pytest.fail(f"❌ Failed to parse JSON output from command: {command}\nOutput:\n{result.stdout}")
        return False, None

    if not os.path.exists(expected_file):
        pytest.fail(f"❌ Expected JSON file not found: {expected_file}")
        return False, None

    try:
        with open(expected_file, "r", encoding="utf-8") as file:
            expected_json = json.load(file)
    except json.JSONDecodeError:
        pytest.fail(f"❌ Failed to parse expected JSON file: {expected_file}")
        return False, None

    diff = DeepDiff(expected_json, output_json, ignore_order=True)

    if not diff:
        return True, None
    else:
        return False, diff


@pytest.mark.parametrize("command,expected_file", [
    # Task 1
    ("python main.py -t 1 -s Q1_examples/example_1/sentences_small_1.csv -n Q1_examples/example_1/people_small_1.csv -r REMOVEWORDS.csv",
     "Q1_examples/example_1/Q1_result1.json"),
    
    # Task 2
    ("python main.py -t 2 --maxk 3 -s Q2_examples/example_1/sentences_small_1.csv -r REMOVEWORDS.csv",
     "Q2_examples/example_1/Q2_result1.json"),
    
    # Task 3
    ("python main.py -t 3 -s Q3_examples/example_1/sentences_small_1.csv -n Q3_examples/example_1/people_small_1.csv -r REMOVEWORDS.csv",
     "Q3_examples/example_1/Q3_result1.json"),

    # Task 4
    ("python main.py -t 4 -s Q4_examples/example_1/sentences_small_1.csv --qsek_query_path Q4_examples/example_1/kseq_query_keys_1.json -r REMOVEWORDS.csv",
     "Q4_examples/example_1/Q4_result1.json"),

    # Task 5
    ("python main.py -t 5 -s Q5_examples/example_1/sentences_small_1.csv -n Q5_examples/example_1/people_small_1.csv -r REMOVEWORDS.csv --maxk 3",
     "Q5_examples/example_1/Q5_result1.json"),

    # Task 6
    ("python main.py -t 6 -s Q6_examples/example_1/sentences_small_1.csv -n Q6_examples/example_1/people_small_1.csv -r REMOVEWORDS.csv --windowsize 4 --threshold 4",
     "Q6_examples/example_1/Q6_result1_w4_t4.json"),

    # Task 7
    ("python main.py -t 7 -s Q7_examples/example_1/sentences_small_1.csv -n Q7_examples/example_1/people_small_1.csv --pairs Q7_examples/example_1/people_connections_1.json -r REMOVEWORDS.csv --windowsize 5 --threshold 2 --maximal_distance 1000",
     "Q7_examples/example_1/Q7_result1_w5_t2.json"),

    # Task 8
    ("python main.py -t 8 -s Q8_examples/example_1/sentences_small_1.csv -n Q8_examples/example_1/people_small_1.csv -r REMOVEWORDS.csv --windowsize 3 --threshold 2 --fixed_length 2 --pairs Q8_examples/example_1/people_connections_1.json",
     "Q8_examples/example_1/Q8_example_1_w_3_threshold_2_fixed_length_2.json"),

    # Task 9
    ("python main.py -t 9 -s Q9_examples/example_1/sentences_small_1.csv -r REMOVEWORDS.csv --threshold 1",
     "Q9_examples/example_1/Q9_result1.json"),
])
def test_tasks(command, expected_file):
    """
    Runs command-line tests for multiple tasks, comparing the JSON output with the expected results.

    Args:
        command (str): The shell command to execute.
        expected_file (str): Path to the JSON file containing the expected output.
    """
    passed, diff = run_command_and_compare(command, expected_file)

    if not passed:
        pytest.fail(f"❌ Test failed for command: {command}\nDifferences:\n{diff}")