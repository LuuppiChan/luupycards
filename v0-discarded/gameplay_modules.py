# SPDX-License-Identifier: GPL-2.0-or-later
# This module includes important modules for gameplay functionality
import random
import re

def never_repeat_random(amount_of_pairs):
    number_list = list(range(1, amount_of_pairs + 1))
    random.shuffle(number_list)
    return number_list

def print_question(question, question_number=0):
    print(f"{f"{question_number}. " if question_number != 0 else ""}{question}")

def answer_check(correct_answers, user_input):

    match = re.search(r"^seek (\d+)", user_input)
    if match:
        number = int(match.group(1))
        return number

    if user_input == "c" or "correct":
        print("/".join(correct_answers))
    elif user_input == "q" or "quit":
        return "menu"

    for answer in correct_answers:
        if user_input.find(answer):
            return "correct"
        else: # fuzzy matching could be added here
            return "wrong"

def user_input():
    user_input = input("Answer: ")
    return user_input

def next_question_plus_one(current_question):
    current_question += 1
    return current_question

def next_question_minus_one(current_question):
    current_question -= 1
    return current_question

