# SPDX-License-Identifier: GPL-2.0-or-later
import os
import csv
import json

def open_memory(memory_path):
    with open(memory_path, "rt") as file:
        contents_json = file.read()
        contents_python = json.loads(contents_json)
        print(contents_python)
    return contents_python

def main_menu(modes, version):
    while True:
        print(f"Welcome to Luupycards! {version}")
        for i, mode in enumerate(modes, start=1):  # Prints all modes and their numbers
            print(f"{i} for {mode}")
        selected_input = input("Type number or the full name: ")
        if selected_input.isdigit():
            selected_input = int(selected_input)
            if 0 <= selected_input - 1 < len(modes):  # Checks if input is correct
                selected_mode = selected_input - 1
                break
        elif selected_input in modes:  # If user input is alphabetical
            selected_mode = modes.index(selected_input)  # Finds the specific mode
            break
        print(f"Invalid selection \"{selected_input}\", please try again.")
    return selected_mode


def pair_import(csv_file_path):
    # create question and answer list (this will be created elsewhere later)
    questions = []
    answers = []
    pairs = {
        "questions" : questions,
        "answers" : answers
    }

    with open(csv_file_path, mode="r") as file:
        csv_reader = csv.reader(file)

        for row_number, row in enumerate(csv_reader, start=1):
            row = [x for x in row if x]

            if row_number % 2 == 0:
                answers.append(row)
            else:
                questions.append(row)

    return questions, answers
