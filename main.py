import argparse
from typing import Any, Dict, Optional, Type
from task1 import Task1 # type: ignore
from task2 import Task2 # type: ignore
from task3 import Task3 # type: ignore
from task4 import Task4 # type: ignore
from task5 import Task5 # type: ignore
from task6 import Task6 # type: ignore
from task7 import Task7 # type: ignore
from task8 import Task8 # type: ignore
from task9 import Task9 # type: ignore

def readargs(args=None):
	parser = argparse.ArgumentParser(
		prog='Text Analyzer project',
	)
	# General arguments
	parser.add_argument('-t', '--task',
						help="task number",
						required=True
						)
	parser.add_argument('-s', '--sentences',
						help="Sentence file path",
						)
	parser.add_argument('-n', '--names',
						help="Names file path",
						)
	parser.add_argument('-r', '--removewords',
						help="Words to remove file path",
						)
	parser.add_argument('-p', '--preprocessed',
						action='append',
						help="json with preprocessed data",
						)
	# Task specific arguments
	parser.add_argument('--maxk',
						type=int,
						help="Max k",
						)
	parser.add_argument('--fixed_length',
						type=int,
						help="fixed length to find",
						)
	parser.add_argument('--windowsize',
						type=int,
						help="Window size",
						)
	parser.add_argument('--pairs',
						help="json file with list of pairs",
						)
	parser.add_argument('--threshold',
						type=int,
						help="graph connection threshold",
						)
	parser.add_argument('--maximal_distance',
						type=int,
						help="maximal distance between nodes in graph",
						)

	parser.add_argument('--qsek_query_path',
						help="json file with query path",
						)
	
	return parser.parse_args(args)

def main() -> None:
    """Main function to execute the selected task."""
    args: argparse.Namespace = readargs()

    task_mapping: Dict[str, Type[Any]] = {
        '1': Task1, '2': Task2, '3': Task3, '4': Task4,
        '5': Task5, '6': Task6, '7': Task7, '8': Task8, '9': Task9
    }

    task_class: Optional[Type[Any]] = task_mapping.get(args.task)

    if not task_class:
        print("Invalid task number!")
        return 

    try:
        task_instance: Any = task_class(args)
        task_method: str = f"task_{args.task}"

        if hasattr(task_instance, task_method):
            getattr(task_instance, task_method)()
        else:
            print(f"Error: Task {args.task} does not have a defined method!")
    except Exception as e:
        print(f"Error executing Task {args.task}: {e}") 

if __name__ == "__main__":
	main()