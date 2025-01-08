# SPDX-License-Identifier: GPL-2.0-or-later
import os
import csv

# create question and answer list (this will be created elsewhere later)
questions = []
answers = []

example_file_name= "example_test.csv"
work_dir = os.getcwd()
parent_dir = os.path.abspath(os.path.join(work_dir, os.pardir))
example_file_path = os.path.abspath(os.path.join(parent_dir, example_file_name))

with open(example_file_path, mode="r") as file:
    csv_reader = csv.reader(file)

    for row_number, row in enumerate(csv_reader, start=1):
        row = [x for x in row if x]

        if row_number % 2 == 0:
            answers.append(row)
        else:
            questions.append(row)


print(questions)
print(answers)