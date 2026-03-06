import pytest
import json
import tempfile
import os
import csv
from collections import defaultdict
from unittest.mock import patch
from main import readargs, main # type: ignore
from task1 import Task1  # type: ignore
from task2 import Task2  # type: ignore
from task3 import Task3  # type: ignore
from task4 import Task4  # type: ignore
from task5 import Task5  # type: ignore
from task6 import Task6  # type: ignore
from task7 import Task7  # type: ignore
from task8 import Task8  # type: ignore
from task9 import Task9  # type: ignore
from utils import (get_processed_sentences, load_json, load_people_data,load_people_pairs, load_kseq_query, create_name_mapping,build_adjacency_list)  # type: ignore

@pytest.fixture
def temp_json_file():
    """Creates a temporary JSON file."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w", encoding="utf-8") as temp_file:
        yield temp_file.name
    os.remove(temp_file.name)

@pytest.fixture
def temp_json_with_data():
    """Creates a temporary JSON file with predefined data and closes it properly."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w", encoding="utf-8") as temp_file:
        data = {"keys": [["Harry Potter", "The Chosen One"], ["Hermione Granger", "Brilliant Witch"]]}
        json.dump(data, open(temp_file.name, "w", encoding="utf-8"))
    yield temp_file.name
    os.remove(temp_file.name)

@pytest.fixture
def temp_people_file():
    """Creates a temporary JSON file with people data."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w", encoding="utf-8") as temp_file:
        data = {
            "Question 1": {
                "Processed Sentences": [
                    ["harry", "potter", "wizard"],
                    ["hermione", "granger", "brilliant"],
                    ["ron", "weasley", "loyal"]
                ]
            }
        }
        json.dump(data, temp_file)
        temp_file.flush()

    yield temp_file.name

    os.remove(temp_file.name)


@pytest.fixture
def temp_removewords():
    """Creates a temporary file with words to remove."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w', encoding="utf-8") as temp_file:
        temp_file.write("is\n")
        temp_file.write("a\n")
        temp_file.write("very\n")
    yield temp_file.name
    try:
        os.remove(temp_file.name)
    except PermissionError:
        pass


@pytest.fixture
def temp_sentences_file():
    """Creates a temporary valid sentences CSV file."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='w', encoding="utf-8") as temp_file:
        temp_file.write("sentence\n")
        temp_file.write("Harry Potter is a wizard\n")
        temp_file.write("Hermione Granger is very smart\n")
    yield temp_file.name
    try:
        os.remove(temp_file.name)
    except PermissionError:
        pass


@pytest.fixture
def temp_names_file():
    """Creates a temporary valid names CSV file."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='w', encoding="utf-8") as temp_file:
        temp_file.write("Name,Other Names\n")
        temp_file.write("Harry Potter,The Boy Who Lived\n")
        temp_file.write("Hermione Granger,Brilliant Witch\n")
    yield temp_file.name
    try:
        os.remove(temp_file.name)
    except PermissionError:
        pass


@pytest.fixture
def sample_args(temp_sentences_file, temp_names_file, temp_removewords):
    """Creates mock arguments for testing Task1."""
    class Args:
        sentences = temp_sentences_file
        names = temp_names_file
        removewords = temp_removewords

    return Args()

@pytest.fixture
def empty_file():
    """Creates an empty temporary file."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='w', encoding="utf-8") as temp_file:
        pass
    yield temp_file.name
    try:
        os.remove(temp_file.name)
    except PermissionError:
        pass


@pytest.fixture
def invalid_sentences_file():
    """Creates a CSV file missing the 'sentence' column."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='w', encoding="utf-8") as temp_file:
        temp_file.write("wrong_column\n")
        temp_file.write("This should fail\n")
    yield temp_file.name
    try:
        os.remove(temp_file.name)
    except PermissionError:
        pass


@pytest.fixture
def invalid_names_file():
    """Creates a CSV file missing the 'Name' and 'Other Names' columns."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='w', encoding="utf-8") as temp_file:
        temp_file.write("wrong_column\n")
        temp_file.write("John Doe\n")
    yield temp_file.name
    try:
        os.remove(temp_file.name)
    except PermissionError:
        pass
    
#======================= Tests =======================

def test_load_json_valid(temp_json_with_data):
    """Test successful loading of a JSON file."""
    data = load_json(temp_json_with_data)
    assert "keys" in data
    assert isinstance(data["keys"], list)

def test_load_json_invalid():
    """Test loading a missing JSON file."""
    with pytest.raises(FileNotFoundError):
        load_json("non_existent_file.json")

def test_load_people_pairs(temp_json_with_data):
    """Test loading people pairs from a valid JSON file."""
    pairs = load_people_pairs(temp_json_with_data)
    assert isinstance(pairs, list)
    assert len(pairs) == 2
    assert pairs[0] == ["Harry Potter", "The Chosen One"]

def test_load_people_pairs_invalid():
    """Test loading from a non-existent JSON file."""
    with pytest.raises(SystemExit):
        load_people_pairs("invalid_file.json")

def test_load_kseq_query(temp_json_with_data):
    """Test loading K-seq query keys."""
    queries = load_kseq_query(temp_json_with_data)
    assert isinstance(queries, list)
    assert len(queries) == 2

def test_create_name_mapping():
    """Test creating a name mapping from processed people data."""
    people_data = [
        [["harry", "potter"], [["the", "boy", "who", "lived"]]],
        [["hermione", "granger"], [["brilliant", "witch"]]]
    ]
    name_map = create_name_mapping(people_data)
    assert name_map["harry potter"] == "harry potter"
    assert name_map["hermione granger"] == "hermione granger"
    assert name_map["the boy who lived"] == "harry potter"
    assert name_map["brilliant witch"] == "hermione granger"

def test_build_adjacency_list():
    """Test building an adjacency list from pair matches."""
    pairs = [
    ("harry potter", "hermione granger"),
    ("harry potter", "ron weasley")
]
    graph = build_adjacency_list(pairs)
    assert isinstance(graph, defaultdict)
    assert "harry potter" in graph
    assert "hermione granger" in graph["harry potter"]
    assert "ron weasley" in graph["harry potter"]
    assert "harry potter" in graph["ron weasley"]
    assert "harry potter" in graph["hermione granger"]

def test_get_processed_sentences(temp_people_file):
    """Test retrieving processed sentences from a preprocessed file."""
    class Args:
        def __init__(self):
            self.preprocessed = [temp_people_file]

    args = Args()
    sentences = get_processed_sentences(args)
    assert isinstance(sentences, list)

def test_load_people_data_without_preprocessed(temp_sentences_file, temp_names_file, temp_removewords):
    """Test `load_people_data` when no preprocessed file is provided."""
    class Args:
        preprocessed = []
        sentences = temp_sentences_file
        names = temp_names_file
        removewords = temp_removewords

    people_data = load_people_data(Args())
    assert isinstance(people_data, list)
    assert len(people_data) > 0  

def test_load_json_file_not_found():
    """Test load_json when the file does not exist."""
    with pytest.raises(FileNotFoundError):
        load_json("non_existent_file.json")


def test_load_json_invalid_format():
    """Test load_json with an invalid JSON format."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w", encoding="utf-8") as temp_file:
        temp_file.write("{invalid_json: true")  
        temp_file_name = temp_file.name

    try:
        with pytest.raises(ValueError, match="Invalid JSON format"):
            load_json(temp_file_name)
    finally:
        os.remove(temp_file_name)

def test_get_processed_sentences_no_data():
    """Test get_processed_sentences when no preprocessed data is found."""
    class Args:
        preprocessed = ["non_existent_file.json"]

    with pytest.raises(ValueError, match="Invalid input"):
        get_processed_sentences(Args())

def test_load_people_data_no_data():
    """Test load_people_data when no processed names are found."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as temp_removewords:
        temp_removewords.write("is\n")
        temp_removewords.write("a\n")
        temp_removewords.write("very\n")
        temp_removewords_name = temp_removewords.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode="w", encoding="utf-8") as temp_names:
        temp_names.write("Name,Other Names\n") 
        temp_names.write(",\n")  
        temp_names_name = temp_names.name

    class Args:
        preprocessed = ["non_existent_file.json"]
        sentences = "valid_sentences.csv"
        names = temp_names_name
        removewords = temp_removewords_name

    try:
        with pytest.raises(SystemExit):
            load_people_data(Args())
    finally:
        os.remove(temp_removewords_name)
        os.remove(temp_names_name)


def test_load_kseq_query_invalid_json():
    """Test load_kseq_query with an invalid JSON file."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w", encoding="utf-8") as temp_file:
        temp_file.write("{invalid_json: true") 
        temp_file_name = temp_file.name

    try:
        with pytest.raises(SystemExit):
            load_kseq_query(temp_file_name) 
    finally:
        os.remove(temp_file_name)

#-------------------------------------------test for task 1------------------------------------------

def test_task1_json_output(sample_args, capfd):
    """Tests the final JSON output of Task1."""
    task1 = Task1(sample_args)
    task1.task_1()

    captured = capfd.readouterr().out.strip()

    try:
        output = json.loads(captured)
    except json.JSONDecodeError:
        pytest.fail("Invalid JSON output from Task1")

    if "error" in output:
        pytest.fail(f"Task1 returned an error: {output['error']}")

    expected_output = {
        "Question 1": {
            "Processed Sentences": [["harry", "potter", "wizard"], ["hermione", "granger", "smart"]],
            "Processed Names": [
                [["harry", "potter"], [["the", "boy", "who", "lived"]]],
                [["hermione", "granger"], [["brilliant", "witch"]]]
            ]
        }
    }

    assert output == expected_output


def test_missing_sentences_file(temp_removewords, capsys):
    """Test that missing sentences file raises SystemExit."""
    class Args:
        sentences = "non_existent_file.csv"
        names = "valid_names.csv"
        removewords = temp_removewords

    with pytest.raises(SystemExit) as exc_info:
        task_instance = Task1(Args())  
        task_instance.task_1()

    assert exc_info.value.code == 1  

    captured = capsys.readouterr()  
    assert "Invalid input" in captured.out  


def test_missing_names_file(temp_removewords, capsys):
    """Test that missing names file raises SystemExit."""
    class Args:
        sentences = "valid_sentences.csv"
        names = "non_existent_file.csv"
        removewords = temp_removewords

    with pytest.raises(SystemExit) as exc_info:
        task_instance = Task1(Args())  
        task_instance.task_1()

    assert exc_info.value.code == 1  

    captured = capsys.readouterr()  
    assert "Invalid input" in captured.out



def test_empty_sentences_file(empty_file, temp_removewords):
    """Test that an empty sentences file raises ValueError."""
    class Args:
        sentences = empty_file
        names = "valid_names.csv"
        removewords = temp_removewords

    with pytest.raises(ValueError, match="File is empty"):
        Task1(Args()).process_sentences()


def test_empty_names_file(empty_file, temp_removewords):
    """Test that an empty names file raises ValueError."""
    class Args:
        sentences = "valid_sentences.csv"
        names = empty_file
        removewords = temp_removewords

    with pytest.raises(ValueError, match="File is empty"):
        Task1(Args()).process_names()


def test_invalid_sentences_file(invalid_sentences_file, temp_removewords):
    """Test that a sentences file missing the 'sentence' column raises ValueError."""
    class Args:
        sentences = invalid_sentences_file
        names = "valid_names.csv"
        removewords = temp_removewords

    with pytest.raises(ValueError, match="Missing 'sentence' column"):
        Task1(Args()).process_sentences()


def test_invalid_names_file(invalid_names_file, temp_removewords):
    """Test that a names file missing required columns raises ValueError."""
    class Args:
        sentences = "valid_sentences.csv"
        names = invalid_names_file
        removewords = temp_removewords

    with pytest.raises(ValueError, match="Missing 'Name' or 'Other Names' column"):
        Task1(Args()).process_names()

def test_missing_remove_words_file():
    """Test that missing remove words file raises SystemExit."""
    class Args:
        sentences = "valid_sentences.csv"
        names = "valid_names.csv"
        removewords = "non_existent_file.txt"

    with pytest.raises(SystemExit) as exc_info:
        task_instance = Task1(Args())  
        task_instance.task_1()  

    assert exc_info.value.code == 1

def test_task1_with_exception(sample_args, capsys):
    """Test error handling in Task1 when an exception occurs."""
    
    class MockTask1(Task1):
        def process_sentences(self):
            raise ValueError("Test Error")

    with pytest.raises(SystemExit, match="1"):
        MockTask1(sample_args).task_1()

    assert "Unexpected error: Test Error" in capsys.readouterr().out

def test_task1_with_invalid_data(sample_args, capsys):
    """Test Task1 handling invalid input."""
    class Args:
        sentences = "invalid_file.csv" 
        names = "valid_names.csv"
        removewords = sample_args.removewords

    with pytest.raises(SystemExit) as exc_info:
        task1 = Task1(Args())
        task1.task_1()

    assert exc_info.value.code == 1

    captured = capsys.readouterr().out.strip()
    assert "Invalid input" in captured

def test_process_names_empty_name(temp_removewords):
    """Test process_names when a name field is empty."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='w', encoding="utf-8") as temp_file:
        writer = csv.writer(temp_file)
        writer.writerow(["Name", "Other Names"])  
        writer.writerow(["", "Alias1, Alias2"])  
        temp_file_name = temp_file.name

    class Args:
        sentences = "valid_sentences.csv"
        names = temp_file_name
        removewords = temp_removewords

    task1 = Task1(Args())
    result = task1.process_names()
    
    assert result == []  

    os.remove(temp_file_name)  
 

def test_process_names_duplicate_names(temp_removewords):
    """Test process_names when duplicate names exist."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='w', encoding="utf-8") as temp_file:
        writer = csv.writer(temp_file)
        writer.writerow(["Name", "Other Names"]) 
        writer.writerow(["John Doe", "JD"]) 
        writer.writerow(["John Doe", "Johnny"])  
        temp_file_name = temp_file.name

    class Args:
        sentences = "valid_sentences.csv"
        names = temp_file_name
        removewords = temp_removewords

    task1 = Task1(Args())
    result = task1.process_names()

    assert len(result) == 1  

    os.remove(temp_file_name) 

#-------------------------------------------test for task 2------------------------------------------

@pytest.fixture
def temp_removewords_2():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w', encoding="utf-8") as temp_file:
        temp_file.write("is\n")
        temp_file.write("a\n")
        temp_file.write("very\n")
    yield temp_file.name
    os.remove(temp_file.name)

@pytest.fixture
def temp_sentences_file_2():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='w', encoding="utf-8") as temp_file:
        temp_file.write("sentence\n")
        temp_file.write("Harry Potter is a wizard\n")
        temp_file.write("Hermione Granger is very smart\n")
    yield temp_file.name
    os.remove(temp_file.name)

@pytest.fixture
def temp_names_file_2():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='w', encoding="utf-8") as temp_file:
        temp_file.write("Name,Other Names\n")
        temp_file.write("Harry Potter,The Boy Who Lived\n")
        temp_file.write("Hermione Granger,Brilliant Witch\n")
    yield temp_file.name
    os.remove(temp_file.name)

@pytest.fixture
def sample_args_2(temp_sentences_file_2, temp_names_file_2, temp_removewords_2):
    class Args:
        maxk = 3
        sentences = temp_sentences_file_2
        names = temp_names_file_2
        removewords = temp_removewords_2
    return Args()

@pytest.fixture
def invalid_args_2(temp_sentences_file_2, temp_names_file_2, temp_removewords_2):
    class Args:
        maxk = -1  
        sentences = temp_sentences_file_2
        names = temp_names_file_2
        removewords = temp_removewords_2
    return Args()

def test_count_sequences():
    sentences = [
        ["harry", "potter", "is", "wizard"],
        ["hermione", "granger", "is", "smart"]
    ]
    max_k = 2
    result = Task2.count_sequences(sentences, max_k)
    
    assert isinstance(result, dict)
    assert "1_seq" in result
    assert "2_seq" in result
    assert ["harry", 1] in result["1_seq"]
    assert ["potter is", 1] in result["2_seq"]

def test_task2_output(sample_args_2, capfd):
    task2 = Task2(sample_args_2)
    task2.task_2()
    
    captured = capfd.readouterr().out.strip()
    
    try:
        output = json.loads(captured)
    except json.JSONDecodeError:
        pytest.fail("Invalid JSON output from Task2")
    
    assert "Question 2" in output
    assert isinstance(output["Question 2"], dict)
    assert f"{sample_args_2.maxk}-Seq Counts" in output["Question 2"]

def test_invalid_maxk(invalid_args_2):
    """Test Task2 handling invalid maxk values."""
    with pytest.raises(SystemExit) as exc_info:
        task2 = Task2(invalid_args_2)
        task2.task_2()

    assert exc_info.value.code == 1

def test_empty_sentences():
    sentences = []
    max_k = 3
    result = Task2.count_sequences(sentences, max_k)
    
    assert isinstance(result, dict)
    for k in range(1, max_k + 1):
        assert f"{k}_seq" in result
        assert result[f"{k}_seq"] == []

def test_format_output(temp_sentences_file_2, temp_names_file_2, temp_removewords_2):
    class MockArgs:
        maxk = 3
        sentences = temp_sentences_file_2
        names = temp_names_file_2
        removewords = temp_removewords_2
    
    task2 = Task2(MockArgs())
    k_seq_counts = {
        "1_seq": [["harry", 1], ["potter", 1]],
        "2_seq": [["harry potter", 1]]
    }
    result = task2._format_output(k_seq_counts, MockArgs().maxk)
    
    assert isinstance(result, dict)
    assert "Question 2" in result
    assert f"{MockArgs().maxk}-Seq Counts" in result["Question 2"]

#-------------------------------------------test for task 3------------------------------------------
@pytest.fixture
def temp_removewords_3():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w', encoding="utf-8") as temp_file:
        temp_file.write("is\n")
        temp_file.write("a\n")
        temp_file.write("very\n")
    yield temp_file.name
    try:
        os.remove(temp_file.name)
    except FileNotFoundError:
        pass

@pytest.fixture
def temp_sentences_file_3():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='w', encoding="utf-8") as temp_file:
        temp_file.write("sentence\n")
        temp_file.write("Harry Potter is a wizard\n")
        temp_file.write("Hermione Granger is very smart\n")
    yield temp_file.name
    try:
        os.remove(temp_file.name)
    except FileNotFoundError:
        pass

@pytest.fixture
def temp_names_file_3():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='w', encoding="utf-8") as temp_file:
        temp_file.write("Name,Other Names\n")
        temp_file.write("Harry Potter,The Boy Who Lived\n")
        temp_file.write("Hermione Granger,Brilliant Witch\n")
    yield temp_file.name
    try:
        os.remove(temp_file.name)
    except FileNotFoundError:
        pass

@pytest.fixture
def sample_args_3(temp_sentences_file_3, temp_names_file_3, temp_removewords_3):
    class Args:
        maxk = 3
        sentences = temp_sentences_file_3
        names = temp_names_file_3
        removewords = temp_removewords_3
    return Args()

def test_count_mentions():
    sentences = [
        ["harry", "potter", "is", "wizard"],
        ["hermione", "granger", "is", "smart"]
    ]
    people_data = [
        [["harry", "potter"], [["the", "boy", "who", "lived"]]],
        [["hermione", "granger"], [["brilliant", "witch"]]]
    ]
    result = Task3.count_mentions(Task3, sentences, people_data)
    
    assert isinstance(result, dict)
    assert "harry potter" in result
    assert "hermione granger" in result
    assert result["harry potter"] > 0
    assert result["hermione granger"] > 0

def test_task3_output(sample_args_3, capfd):
    task3 = Task3(sample_args_3)
    task3.task_3()
    
    captured = capfd.readouterr().out.strip()
    
    try:
        output = json.loads(captured)
    except json.JSONDecodeError:
        pytest.fail("Invalid JSON output from Task3")
    
    assert "Question 3" in output
    assert isinstance(output["Question 3"], dict)
    assert "Name Mentions" in output["Question 3"]

#-------------------------------------------test for task 4------------------------------------------
@pytest.fixture
def temp_kseq_query_file_4():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='w', encoding="utf-8") as temp_file:
        json.dump({"queries": [["harry", "potter"], ["hermione", "granger"]]}, temp_file)
    yield temp_file.name
    try:
        os.remove(temp_file.name)
    except FileNotFoundError:
        pass

@pytest.fixture
def temp_sentences_file_4():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='w', encoding="utf-8") as temp_file:
        temp_file.write("sentence\n")
        temp_file.write("Harry Potter is a wizard\n")
        temp_file.write("Hermione Granger is very smart\n")
    yield temp_file.name
    try:
        os.remove(temp_file.name)
    except FileNotFoundError:
        pass

@pytest.fixture
def temp_names_file_4():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='w', encoding="utf-8") as temp_file:
        temp_file.write("Name,Other Names\n")
        temp_file.write("Harry Potter,The Boy Who Lived\n")
        temp_file.write("Hermione Granger,Brilliant Witch\n")
    yield temp_file.name
    try:
        os.remove(temp_file.name)
    except FileNotFoundError:
        pass

@pytest.fixture
def temp_removewords_4():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w', encoding="utf-8") as temp_file:
        temp_file.write("is\n")
        temp_file.write("a\n")
        temp_file.write("very\n")
    yield temp_file.name
    try:
        os.remove(temp_file.name)
    except FileNotFoundError:
        pass

@pytest.fixture
def sample_args_4(temp_sentences_file_4, temp_kseq_query_file_4, temp_names_file_4, temp_removewords_4):
    class Args:
        qsek_query_path = temp_kseq_query_file_4
        sentences = temp_sentences_file_4
        names = temp_names_file_4
        removewords = temp_removewords_4
    return Args()

@pytest.fixture
def sample_args_4_pr(temp_people_file,temp_kseq_query_file_4):
    class Args:
        qsek_query_path = temp_kseq_query_file_4
        preprocessed = [temp_people_file]

    return Args()

def test_clean_kseq_keys(sample_args_4):
    task4 = Task4(sample_args_4)
    k_seq_keys = [["Harry", "Potter"], ["Hermione", "Granger"]]
    cleaned_keys = task4.clean_kseq_keys(k_seq_keys)
    assert isinstance(cleaned_keys, list)
    assert all(isinstance(seq, list) for seq in cleaned_keys)

def test_pr_clean_kseq_keys(sample_args_4_pr):
    task=Task4(sample_args_4_pr)
    assert task.clean_kseq_keys(sample_args_4_pr)

def test_build_index(sample_args_4):
    task4 = Task4(sample_args_4)
    k_seq_keys = [["harry", "potter"], ["hermione", "granger"]]
    sentences = [
        ["harry", "potter", "is", "wizard"],
        ["hermione", "granger", "is", "smart"]
    ]
    index = task4.build_index(k_seq_keys, sentences)
    assert isinstance(index, list)
    assert len(index) == 2

def test_task4_output(sample_args_4, capfd):
    task4 = Task4(sample_args_4)
    task4.task_4()
    captured = capfd.readouterr().out.strip()
    try:
        output = json.loads(captured)
    except json.JSONDecodeError:
        pytest.fail("Invalid JSON output from Task4")
    assert "Question 4" in output
    assert isinstance(output["Question 4"], dict)
    assert "K-Seq Matches" in output["Question 4"]

#-------------------------------------------test for task 5------------------------------------------
@pytest.fixture
def temp_people_data_file_5():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='w', encoding="utf-8") as temp_file:
        json.dump({"people": [[["harry", "potter"], [["the", "boy", "who", "lived"]]], [["hermione", "granger"], [["brilliant", "witch"]]]]}, temp_file)
    yield temp_file.name
    try:
        os.remove(temp_file.name)
    except FileNotFoundError:
        pass

@pytest.fixture
def temp_sentences_file_5():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='w', encoding="utf-8") as temp_file:
        temp_file.write("sentence\n")
        temp_file.write("Harry Potter is a wizard\n")
        temp_file.write("Hermione Granger is very smart\n")
    yield temp_file.name
    try:
        os.remove(temp_file.name)
    except FileNotFoundError:
        pass

@pytest.fixture
def temp_names_file_5():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='w', encoding="utf-8") as temp_file:
        temp_file.write("Name,Other Names\n")
        temp_file.write("Harry Potter,The Boy Who Lived\n")
        temp_file.write("Hermione Granger,Brilliant Witch\n")
    yield temp_file.name
    try:
        os.remove(temp_file.name)
    except FileNotFoundError:
        pass

@pytest.fixture
def temp_removewords_5():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w', encoding="utf-8") as temp_file:
        temp_file.write("is\n")
        temp_file.write("a\n")
        temp_file.write("very\n")
    yield temp_file.name
    try:
        os.remove(temp_file.name)
    except FileNotFoundError:
        pass

@pytest.fixture
def sample_args_5(temp_sentences_file_5, temp_people_data_file_5, temp_names_file_5, temp_removewords_5):
    class Args:
        maxk = 3
        sentences = temp_sentences_file_5
        people_data = temp_people_data_file_5
        names = temp_names_file_5
        removewords = temp_removewords_5
    return Args()

def test_find_person_contexts(sample_args_5):
    task5 = Task5(sample_args_5)
    contexts = task5.find_person_contexts()
    assert isinstance(contexts, list)
    assert len(contexts) > 0

def test_task5_output(sample_args_5, capfd):
    task5 = Task5(sample_args_5)
    task5.task_5()
    captured = capfd.readouterr().out.strip()
    try:
        output = json.loads(captured)
    except json.JSONDecodeError:
        pytest.fail("Invalid JSON output from Task5")
    assert "Question 5" in output
    assert isinstance(output["Question 5"], dict)
    assert "Person Contexts and K-Seqs" in output["Question 5"]

#-------------------------------------------test for task 6------------------------------------------

@pytest.fixture
def temp_people_data_file_6():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='w', encoding="utf-8") as temp_file:
        json.dump({"people": [[["harry", "potter"], [["the", "boy", "who", "lived"]]], [["hermione", "granger"], [["brilliant", "witch"]]]]}, temp_file)
    yield temp_file.name
    try:
        os.remove(temp_file.name)
    except FileNotFoundError:
        pass

@pytest.fixture
def temp_sentences_file_6():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='w', encoding="utf-8") as temp_file:
        temp_file.write("sentence\n")
        temp_file.write("Harry Potter is a wizard\n")
        temp_file.write("Hermione Granger is very smart\n")
        temp_file.write("The boy who lived met the brilliant witch\n")
    yield temp_file.name
    try:
        os.remove(temp_file.name)
    except FileNotFoundError:
        pass

@pytest.fixture
def temp_names_file_6():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='w', encoding="utf-8") as temp_file:
        temp_file.write("Name,Other Names\n")
        temp_file.write("Harry Potter,The Boy Who Lived\n")
        temp_file.write("Hermione Granger,Brilliant Witch\n")
    yield temp_file.name
    try:
        os.remove(temp_file.name)
    except FileNotFoundError:
        pass

@pytest.fixture
def temp_removewords_6():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w', encoding="utf-8") as temp_file:
        temp_file.write("is\n")
        temp_file.write("a\n")
        temp_file.write("very\n")
    yield temp_file.name
    try:
        os.remove(temp_file.name)
    except FileNotFoundError:
        pass

@pytest.fixture
def sample_args_6(temp_sentences_file_6, temp_people_data_file_6, temp_names_file_6, temp_removewords_6):
    class Args:
        windowsize = 2
        threshold = 1
        sentences = temp_sentences_file_6
        people_data = temp_people_data_file_6
        names = temp_names_file_6
        removewords = temp_removewords_6
    return Args()

def test_build_person_graph(sample_args_6):
    task6 = Task6(sample_args_6)
    graph = task6.build_person_graph()
    assert isinstance(graph, list)
    assert len(graph) > 0
    assert all(isinstance(edge, list) and len(edge) == 2 for edge in graph)

def test_task6_output(sample_args_6, capfd):
    task6 = Task6(sample_args_6)
    task6.task_6()
    captured = capfd.readouterr().out.strip()
    try:
        output = json.loads(captured)
    except json.JSONDecodeError:
        pytest.fail("Invalid JSON output from Task6")
    assert "Question 6" in output
    assert isinstance(output["Question 6"], dict)
    assert "Pair Matches" in output["Question 6"]

#-------------------------------------------test for task 7------------------------------------------
@pytest.fixture
def temp_people_pairs_file_7():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='w', encoding="utf-8") as temp_file:
        json.dump([["harry potter", "hermione granger"]], temp_file)
    yield temp_file.name
    try:
        os.remove(temp_file.name)
    except FileNotFoundError:
        pass

@pytest.fixture
def temp_preprocessed_graph_7():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='w', encoding="utf-8") as temp_file:
        json.dump({"Question 6": {"Pair Matches": [["harry potter", "ron weasley"], ["hermione granger", "ron weasley"]]}}, temp_file)
    yield temp_file.name
    try:
        os.remove(temp_file.name)
    except FileNotFoundError:
        pass

@pytest.fixture
def temp_removewords_file_7():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w', encoding="utf-8") as temp_file:
        temp_file.write("is\n")
        temp_file.write("a\n")
        temp_file.write("very\n")
    yield temp_file.name
    try:
        os.remove(temp_file.name)
    except FileNotFoundError:
        pass

@pytest.fixture
def sample_args_7(temp_people_pairs_file_7, temp_preprocessed_graph_7, temp_removewords_file_7):
    class Args:
        maximal_distance = 2
        pairs = temp_people_pairs_file_7
        preprocessed = temp_preprocessed_graph_7
        windowsize = 2 
        threshold = 1 
        sentences = ["harry potter is a wizard", "hermione granger is very smart"] 
        names = [["harry", "potter"], ["hermione", "granger"]]  
        removewords = temp_removewords_file_7  
    return Args()

@pytest.fixture
def invalid_args_7(temp_removewords_file_7):
    class Args:
        maximal_distance = None
        pairs = None
        windowsize = None  
        threshold = None  
        sentences = []  
        names = []  
        removewords = temp_removewords_file_7 
    return Args()

def test_bfs():
    graph = {
        "harry potter": {"ron weasley"},
        "ron weasley": {"harry potter", "hermione granger"},
        "hermione granger": {"ron weasley"}
    }
    assert Task7.bfs(graph, "harry potter", "hermione granger", 2) is True
    assert Task7.bfs(graph, "harry potter", "hermione granger", 1) is False
    assert Task7.bfs(graph, "harry potter", "harry potter", 2) is True

def test_task7_output(sample_args_7, capfd):
    task7 = Task7(sample_args_7)
    task7.task_7()
    captured = capfd.readouterr().out.strip()
    try:
        output = json.loads(captured)
    except json.JSONDecodeError:
        pytest.fail("Invalid JSON output from Task7")
    assert "Question 7" in output
    assert isinstance(output["Question 7"], dict)
    assert "Pair Matches" in output["Question 7"]

def test_invalid_task7_args(invalid_args_7):
    """Test Task7 handling invalid input."""
    with pytest.raises(SystemExit) as exc_info:
        Task7(invalid_args_7)

    assert exc_info.value.code == 1 

#-------------------------------------------test for task 8------------------------------------------
@pytest.fixture
def temp_people_pairs_file_8():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='w', encoding="utf-8") as temp_file:
        json.dump([
            ["harry potter", "hermione granger"],
            ["harry potter", "draco malfoy"]
        ], temp_file)
    yield temp_file.name
    try:
        os.remove(temp_file.name)
    except FileNotFoundError:
        pass

@pytest.fixture
def temp_preprocessed_graph_8():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='w', encoding="utf-8") as temp_file:
        json.dump({
            "Question 6": {
                "Pair Matches": [
                    ["harry potter", "ron weasley"],
                    ["ron weasley", "hermione granger"],
                    ["draco malfoy", "lucius malfoy"]
                ]
            }
        }, temp_file)
    yield temp_file.name
    try:
        os.remove(temp_file.name)
    except FileNotFoundError:
        pass

@pytest.fixture
def sample_args_8(temp_people_pairs_file_8, temp_preprocessed_graph_8):
    class Args:
        fixed_length = 2
        pairs = temp_people_pairs_file_8
        preprocessed = temp_preprocessed_graph_8
        windowsize = 2
        threshold = 1
    return Args()

@pytest.fixture
def invalid_args_8(temp_sentences_file_6,temp_people_pairs_file_8,temp_names_file_6):
    class Args:
        fixed_length = None
        pairs = temp_people_pairs_file_8
        names = temp_names_file_6
        sentences = temp_sentences_file_6
        removewords = None
        windowsize = None
        threshold = None
        
    return Args()

@pytest.fixture
def missing_args_8(temp_preprocessed_graph_8):
    class Args:
        fixed_length = 2
        pairs = None
        preprocessed = temp_preprocessed_graph_8
        windowsize = 2
        threshold = 1
        
    return Args()

@pytest.fixture
def missing_pre_args_8(temp_people_pairs_file_8,temp_names_file_6,temp_sentences_file_6,temp_removewords_file_7):
    class Args:
        fixed_length = 1
        pairs = temp_people_pairs_file_8
        names = temp_names_file_6
        sentences = temp_sentences_file_6
        removewords = temp_removewords_file_7 
        preprocessed = None
        windowsize = 2
        threshold = 1
        
    return Args()

def test_task8_missing_pairs(missing_args_8):
    with pytest.raises(ValueError, match="Missing --pairs"):
        Task8(missing_args_8)

def test_task8_none_pre(missing_pre_args_8):
    Task8(missing_pre_args_8)

def test_bfs_exact_k(sample_args_8):
    task8 = Task8(sample_args_8)

    assert task8.bfs_exact_k("harry potter", "hermione granger") is True  
    assert task8.bfs_exact_k("harry potter", "draco malfoy") is False  
    assert task8.bfs_exact_k("harry potter", "harry potter") is False  
    assert task8.bfs_exact_k("harry potter", "ron weasley") is False

    task8.k = 1
    assert task8.bfs_exact_k("harry potter", "ron weasley") is True

def test_task8_output(sample_args_8, capfd):
    task8 = Task8(sample_args_8)
    task8.task_8()
    
    captured = capfd.readouterr().out.strip()
    try:
        output = json.loads(captured)
    except json.JSONDecodeError:
        pytest.fail("Invalid JSON output from Task8")

    assert "Question 8" in output
    assert isinstance(output["Question 8"], dict)
    assert "Pair Matches" in output["Question 8"]

    expected_results = [
        ["harry potter", "hermione granger", True],
        ["draco malfoy", "harry potter", False]
    ]
    assert sorted(output["Question 8"]["Pair Matches"]) == sorted(expected_results)

def test_invalid_task8_args(invalid_args_8, capsys):
    """Test Task8 handling invalid input properly."""
    with pytest.raises(SystemExit) as exc_info:
        Task8(invalid_args_8)

    assert exc_info.value.code == 1

    captured = capsys.readouterr().out.strip()
    assert "Invalid remove words input" in captured

def test_bfs_exact_k_edge_cases(sample_args_8):
    task8 = Task8(sample_args_8)

    assert task8.bfs_exact_k("nonexistent", "hermione granger") is False
    task8.k = 10
    assert task8.bfs_exact_k("harry potter", "hermione granger") is False
    task8.k = 2
    assert task8.bfs_exact_k("harry potter", "hermione granger") is True

def test_invalid_k_values(sample_args_8):
    task8 = Task8(sample_args_8)

    task8.k = 0
    assert task8.bfs_exact_k("harry potter", "harry potter") is True  

    task8.k = -1
    with pytest.raises(ValueError, match="Invalid input"):
        task8.bfs_exact_k("harry potter", "hermione granger")

    task8.k = None
    with pytest.raises(ValueError, match="K must be specified for fixed-length path search."):
        task8.bfs_exact_k("harry potter", "ron weasley")


#-------------------------------------------test for task 9------------------------------------------
def write_and_flush(temp_file, data):
    temp_file.write(data)
    temp_file.flush()
    temp_file.close()

@pytest.fixture
def temp_sentences_file_9():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='w', encoding="utf-8", newline='') as temp_file:
        try:
            writer = csv.DictWriter(temp_file, fieldnames=["sentence"])
            writer.writeheader()
            writer.writerows([
                {"sentence": "harry potter is a wizard"},
                {"sentence": "ron weasley is loyal"},
                {"sentence": "hermione granger is very smart"},
                {"sentence": "draco malfoy is cunning"}
            ])
            temp_file.flush()
        finally:
            temp_file.close()

    yield temp_file.name

    try:
        os.remove(temp_file.name)
    except FileNotFoundError:
        pass


@pytest.fixture
def temp_removewords_file_9():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w', encoding="utf-8") as temp_file:
        write_and_flush(temp_file, "is\na\nvery\n")
    yield temp_file.name
    try:
        os.remove(temp_file.name)
    except FileNotFoundError:
        pass

@pytest.fixture
def sample_args_9(temp_sentences_file_9, temp_removewords_file_9):
    class Args:
        threshold = 0
        sentences = temp_sentences_file_9
        removewords = temp_removewords_file_9
    return Args()

@pytest.fixture
def invalid_args_9(temp_removewords_file_9,temp_sentences_file_9):
    class Args:
        threshold = None
        sentences = temp_sentences_file_9
        removewords = temp_removewords_file_9
    return Args()

def test_build_sentence_graph(sample_args_9):
    task9 = Task9(sample_args_9)
    graph = task9.build_sentence_graph(task9._processed_sentences)
    
    assert isinstance(graph, dict)
    assert len(graph) >= 0
    assert all(isinstance(k, int) and isinstance(v, set) for k, v in graph.items())

def test_find_sentence_groups(sample_args_9):
    task9 = Task9(sample_args_9)
    graph = task9.build_sentence_graph(task9._processed_sentences)
    groups = task9.find_sentence_groups(graph)
    
    assert isinstance(groups, list)
    assert all(isinstance(group, set) for group in groups)
    assert sum(len(group) for group in groups) == len(task9._processed_sentences)

def test_task9_output(sample_args_9, capfd):
    task9 = Task9(sample_args_9)
    task9.task_9()
    captured = capfd.readouterr().out.strip()
    
    try:
        output = json.loads(captured)
    except json.JSONDecodeError:
        pytest.fail("Invalid JSON output from Task9")
    
    assert "Question 9" in output
    assert isinstance(output["Question 9"], dict)
    assert "group Matches" in output["Question 9"]

def test_invalid_task9_args(invalid_args_9):
    task=Task9(invalid_args_9)
    with pytest.raises(ValueError, match="Threshold must be a non-negative number."):
        task.task_9()

#-------------------------------------------test for main------------------------------------------
@pytest.fixture
def mock_args():
    """Creates a mock object for argument parsing"""
    class Args:
        task = "1"
        sentences = "test_sentences.csv"
        names = "test_names.csv"
        removewords = "test_removewords.txt"
        preprocessed = None
        maxk = 5
        fixed_length = 3
        windowsize = 2
        pairs = "test_pairs.json"
        threshold = 2
        maximal_distance = 4
        qsek_query_path = "test_query.json"
    
    return Args()

def test_readargs():
    """Tests parsing command line arguments"""
    test_args = ['-t', '1', '-s', 'sentences.csv', '-n', 'names.csv', '-r', 'remove.txt']
    parsed_args = readargs(test_args)

    assert parsed_args.task == "1"
    assert parsed_args.sentences == "sentences.csv"
    assert parsed_args.names == "names.csv"
    assert parsed_args.removewords == "remove.txt"
    assert parsed_args.preprocessed is None

def test_readargs_with_optional_args():
    """Tests parsing command line arguments with optional parameters"""
    test_args = ['-t', '2', '--maxk', '10', '--threshold', '3']
    parsed_args = readargs(test_args)

    assert parsed_args.task == "2"
    assert parsed_args.maxk == 10
    assert parsed_args.threshold == 3

def test_main_invalid_task(capfd):
    """Tests main function with an invalid task number"""
    test_args = ['-t', '99']
    with patch('sys.argv', ['main.py'] + test_args):
        main()
    captured = capfd.readouterr()
    assert "Invalid task number!" in captured.out

@pytest.mark.parametrize("task_number, task_class", [
    ("1", Task1), ("2", Task2), ("3", Task3), ("4", Task4),
    ("5", Task5), ("6", Task6), ("7", Task7), ("8", Task8), ("9", Task9)
])
def test_main_valid_tasks(task_number, task_class):
    """Tests main function with valid task numbers"""
    test_args = ['-t', task_number]
    with patch('sys.argv', ['main.py'] + test_args), \
         patch.object(task_class, '__init__', return_value=None), \
         patch.object(task_class, f'task_{task_number}', return_value=None) as mock_task:
        
        main()
        mock_task.assert_called_once()

def test_main_task_without_method(capfd):
    """Tests main function when a task class does not have the expected method"""
    class MockTask:
        def __init__(self, args):
            pass

    test_args = ['-t', '1']
    with patch('sys.argv', ['main.py'] + test_args), \
         patch('main.Task1', MockTask):
        
        main()
    
    captured = capfd.readouterr()
    assert "Error: Task 1 does not have a defined method!" in captured.out

def test_main_task_execution_failure(capfd):
    """Tests main function when a task execution raises an exception"""
    class MockTask:
        def __init__(self, args):
            pass
        def task_1(self):
            raise ValueError("Test error")

    test_args = ['-t', '1']
    with patch('sys.argv', ['main.py'] + test_args), \
         patch('main.Task1', MockTask):
        
        main()
    
    captured = capfd.readouterr()
    assert "Error executing Task 1: Test error" in captured.out