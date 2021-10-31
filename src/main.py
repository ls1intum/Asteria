#!/usr/bin/env python3
import argparse
import inspect
from pathlib import Path

from automaticAssessor import generate_feedback_for_all_submissions, generate_feedback_for_submission, \
    extract_information_from_sample_solution

BASE_PATH = "../src"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=inspect.getmodulename(__file__))

    parser.add_argument(
        "-txt", "--TextSolution", help="Path to the Text file containing the student's solution", action='store',
        type=Path
    )

    parser.add_argument(
        "-all", "--TextSolutions", help="Path to the folder containing text files of all students solutions",
        action='store',
        type=Path
    )

    parser.add_argument(
        "-uml", "--UMLModel", help="Path to the JSON file containing sample solution depicted in a UML class diagram",
        action='store', type=Path
    )
    parser.add_argument(
        "-d", "--dir", help="Directory to save the automated feedback ",
        action='store', type=Path
    )
    args = parser.parse_args()

    if args.UMLModel and args.TextSolution and args.dir:
        solution_graph = extract_information_from_sample_solution(args.UMLModel)
        generate_feedback_for_submission(args.TextSolution, solution_graph, args.dir)

    elif args.UMLModel and args.TextSolutions and args.dir:
        generate_feedback_for_all_submissions(args.TextSolution, args.UMLModel, args.dir)

    else:
        parser.print_help()
