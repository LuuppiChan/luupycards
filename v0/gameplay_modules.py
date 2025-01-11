# SPDX-License-Identifier: GPL-2.0-or-later
import re

def normal(pairs, current_question=1, current_question_number_enabled=False, streak_current=0, streak_all_time=0):
    result = True
    while not result:
        print(f"Current streak: {streak_current}, All time streak: {streak_all_time}")
        print(f"{f"{current_question}." if current_question_number_enabled else ""} {pairs[current_question]["question"][0]}")
        user_input = input("Answer: ")
        result, current_question_switch = answer_check(pairs[current_question]["answers"], user_input)
        if current_question_switch:
            current_question = current_question_switch
    

def answer_check(correct_answers, user_input):
    for answer in correct_answers:
        match = re.search(r"^seek (\d+)", user_input)

        if answer == user_input:
            print("Correct")
            return True
        elif match:
            question_number = int(match.group(1))
            return True, question_number
        elif user_input == "c" or "correct":
            print("/".join(correct_answers))
            return False


