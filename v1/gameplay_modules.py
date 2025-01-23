# SPDX-License-Identifier: GPL-2.0-or-later
import re
import os
import core_functions as core
import random
import string
import readline # for better input field

def normal(pairs, current_question=1, current_question_number_enabled=True, streak_current=0, streak_all_time=0):

    result = True
    while result:

        print(f"Current streak: {streak_current}, All time streak: {streak_all_time}")
        print_question(current_question, current_question_number_enabled, pairs[current_question]["question"])
        user_input = input("Answer: ")
        user_input = user_input.lower()
        os.system("clear")
        result, current_question = answer_check(pairs[current_question]["answer"], user_input, current_question)

        if result not in ["wrong", "empty field", "correct answer"]:
            break
        elif result == "wrong":
            streak_current = streak_functions(mode="break")

    match result:
        case "correct":
            return True, current_question, streak_functions(streak_current, mode="add"), False
        case "seek":
            return True, current_question, streak_current, True
        case "quit":
            return False, current_question, streak_current, False
        case "wrong":
            pass
        case _:
            raise Exception("Uhh... How...")
    

# This is almost a copypaste of normal mode, just switched places with questions and answers
def reverse(pairs, current_question=1, current_question_number_enabled=True, streak_current=0, streak_all_time=0):

    result = True
    while result:

        print(f"Current streak: {streak_current}, All time streak: {streak_all_time}")
        print_question(current_question, current_question_number_enabled, pairs[current_question]["answer"])
        user_input = input("Question: ")
        user_input = user_input.lower()
        os.system("clear")
        result, current_question = answer_check(pairs[current_question]["question"], user_input, current_question)

        if result not in ["wrong", "empty field", "correct answer"]:
            break
        elif result == "wrong":
            streak_current = streak_functions(mode="break")

    match result:
        case "correct":
            return True, current_question, streak_functions(streak_current, mode="add"), False
        case "seek":
            return True, current_question, streak_current, True
        case "quit":
            return False, current_question, streak_current, False
        case "wrong":
            pass
        case _:
            raise Exception("Uhh... How...")

def multiple_choice(pairs, current_question=1, current_question_number_enabled=True, streak_current=0, streak_all_time=0):
    
    multiple_choice_options = {}
    correct_letter = ""
    result = True
    while result:

        print(f"Current streak: {streak_current}, All time streak: {streak_all_time}")
        print_question(current_question, current_question_number_enabled, pairs[current_question]["question"])

        if not multiple_choice_options:
            correct_letter, correct_answer, multiple_choice_options = generate_multiple_choice_answers(pairs, current_question)
        
        else:
            correct_letter, correct_answer, multiple_choice_options = generate_multiple_choice_answers(pairs, current_question, generate_new=False, correct_letter=correct_letter, multiple_choice_options=multiple_choice_options, lives=1)

        user_input = input("Answer: ")
        user_input = user_input.lower()

        if user_input == correct_letter or correct_letter in user_input.strip() and len(user_input) < 2:
            user_input = pairs[correct_answer]["answer"][0]
            user_input = user_input.lower()

        os.system("clear")
        result, current_question = answer_check(pairs[current_question]["answer"], user_input, current_question)

        if result not in ["wrong", "empty field", "correct answer"]:
            break
        elif result == "wrong":
            streak_current = streak_functions(mode="break")

    match result:
        case "correct":
            return True, current_question, streak_functions(streak_current, mode="add"), False
        case "seek":
            return True, current_question, streak_current, True
        case "quit":
            return False, current_question, streak_current, False
        case "wrong":
            pass
        case _:
            raise Exception("Uhh... How...")


# This hasn't yet been customized for survive, it's just normal gamemode right now.
def survive(pairs, current_question=1, current_question_number_enabled=True, streak_current=0, streak_all_time=0, lives=1):

    result = True
    while result:
        print(f"lives left: {lives}")
        print(f"Current survival streak: {streak_current}, All time survival streak: {streak_all_time}")
        print_question(current_question, current_question_number_enabled, pairs[current_question]["question"])
        user_input = input("Answer: ")
        user_input = user_input.lower()
        os.system("clear")
        result, current_question = answer_check(pairs[current_question]["answer"], user_input, current_question)

        if result not in ["wrong", "empty field"]:
            break
        elif result in ["wrong", "correct answer"]:
            os.system("clear")
            print(f"Wrong, correct answer: {" / ".join(pairs[current_question]["answer"])}")
            lives -= 1
            break

    match result:
        case "correct":
            return True, current_question, streak_functions(streak_current, mode="add"), False, lives
        case "seek":
            return True, current_question, streak_current, True, lives
        case "quit":
            return False, current_question, streak_current, False, lives
        case "wrong":
            return True, current_question, streak_current, False, lives
        case _:
            raise Exception("Uhh... How...")
    



def answer_check(correct_answers, user_input, current_question):
    for answer in correct_answers:

        answer = answer.lower()
        
        if answer == user_input:
            print("Correct")
            return "correct", current_question
        elif answer in user_input:
            print("Correct")
            return "correct", current_question
        
        match = re.search(r"^seek (\d+)", user_input)
        if match:
            question_number = int(match.group(1))
            return "seek", question_number

    if user_input in ["c", "correct"]:
        print(f"Correct answers: {" / ".join(correct_answers)}")
        return "correct answer", current_question

    elif user_input in ["q", "quit"]:
        print("Returning to main menu...")
        return "quit", current_question
    
    elif not user_input or re.findall("^ *$", user_input):
        print("Please type something...")
        return "empty field", current_question

    else:
        print("Wrong")
        return "wrong", current_question


def next_question_plus_one(current_question):
    current_question += 1
    return current_question


def next_question_minus_one(current_question):
    current_question -= 1
    return current_question

def streak_functions(current_streak=0, mode="add"):
    if mode == "add":
        return current_streak + 1
    elif mode == "break":
        return 0
    else:
        raise Exception("Invalid selection")

def generate_multiple_choice_answers(pairs, current_question, generate_new=True, correct_letter="", multiple_choice_options={}):

    if generate_new:
        options = core.get_options()
        max_options = options["multiple choice max options"]
        random_list = core.never_repeat_random_list(1, core.settings_value_manipulator("max question"))

        if len(random_list) < max_options:
            raise Exception(f"Not enough unique pairs to generate {max_options} options from {len(random_list)} pairs.")
        
        if current_question in random_list:
            random_list.remove(current_question)

        random_list = random_list[:max_options] # one less than max_options
        random_list.append(current_question)

        while len(random_list) != max_options:
            random_list.pop(0)

        random.shuffle(random_list)

        letters = string.ascii_lowercase

        for index, (letter, answer_number) in enumerate(zip(letters, random_list)):
            if answer_number == current_question:
                correct_letter = letter
                
            multiple_choice_options[letter] = pairs[answer_number]["answer"][0]

        if not correct_letter:
            raise Exception("There's no correct answer for some reason. ¯\\(ツ)/¯")

    print()
    for index, (key, option) in enumerate(multiple_choice_options.items()):
        print(f"{key}. {option}")
    print()
    
    return correct_letter, current_question, multiple_choice_options


def print_question(current_question, current_question_number_enabled, questions):
    print(f"{f"{current_question}. " if current_question_number_enabled else ""}{" / ".join(questions)}")
