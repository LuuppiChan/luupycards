# SPDX-License-Identifier: GPL-2.0-or-later
# This module includes important modules for gameplay functionality
import random


def never_repeat_random(amount_of_pairs):
    number_list = list(range(1, amount_of_pairs + 1))
    random.shuffle(number_list)
    return number_list

def print_question(question, question_number=0):
    print(f"{f"{question_number}. " if question_number == 0 else ""}{question}")

