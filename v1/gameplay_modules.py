# SPDX-License-Identifier: GPL-2.0-or-later
import re
import os

import core_functions as core
import random
import string
import readline # for better input field


class MainGameplay:
    def __init__(self, pairs, reverse=False, current_question=1, streak_current=0, order="forward"):

        # These for easy reverse mode functionality
        self.question = "question"
        self.answer = "answer"
        if reverse:
            self.question = "answer"
            self.answer = "question"

        # chooses the order
        self.order = order
        if order == "reverse":
            self.order = "reverse"

        self.pairs = pairs
        self.current_question = current_question
        self.show_question_number = core.settings_value_manipulator("show current question number")
        self.streak_current = streak_current
        self.streak_all_time = core.settings_value_manipulator("all time streak")

    def update_class_variables(self, variable, new_input):
        match variable:
            case "streak_current":
                self.streak_current = new_input
            case "streak_all_time":
                self.streak_all_time = new_input
            case "current_question":
                self.current_question = new_input

    def print_question(self):
        print(f"Current streak: {self.streak_current}, All time streak: {self.streak_all_time}")
        print(f"{f"{self.current_question}. " if self.show_question_number else ""}{" / ".join(self.pairs[self.current_question][self.question])}")

    def answer_check(self, user_input):
        correct_answers = self.pairs[self.current_question][self.answer]

        # check for correct answer in user_input, iterates through all answer candidates
        for answer in correct_answers:
            answer = answer.lower()
            if answer == user_input or answer in user_input:
                print("Correct")
                return "correct"

        match = re.search(r"^seek (\d+)", user_input)
        if match:  # seeking
            question_number = int(match.group(1))
            self.update_class_variables("current_question", question_number)
            return "seek",

        elif user_input in ["c", "correct"]:  # show correct answer
            print(f"Correct answers: {" / ".join(correct_answers)}")
            return "show correct answer"

        elif user_input in ["q", "quit"]:  # quit to main menu
            print("Returning to main menu...")
            return "quit"

        elif not user_input or re.findall("^ *$", user_input):  # checks if user_input is empty
            print("Please type something...")
            return "empty field"

        return "wrong"  # if there's no match, the answer is incorrect

    def next_question_plus_one(self):
        self.current_question += 1

    def next_question_minus_one(self):
        self.current_question -= 1

    def next_question(self):
        # Check how the next question should be done and return it.
        if self.order == "forward":
            self.next_question_plus_one()
        elif self.order == "reverse":
            self.next_question_minus_one()
        else:
            raise Exception("Someone has set an invalid question order.")

    def generate_multiple_choice_answers(self, current_question, generate_new=True, correct_letter="", multiple_choice_options={}):

        if generate_new:
            options = core.get_options()
            max_options = options["multiple choice max options"]
            random_list = core.never_repeat_random_list(1, core.settings_value_manipulator("max question"))

            if len(random_list) < max_options:
                raise Exception(
                    f"Not enough unique pairs to generate {max_options} options from {len(random_list)} pairs.")

            if current_question in random_list:
                random_list.remove(current_question)

            random_list = random_list[:max_options]  # one less than max_options
            random_list.append(current_question)

            while len(random_list) != max_options:
                random_list.pop(0)

            random.shuffle(random_list)

            letters = string.ascii_lowercase

            for _, (letter, answer_number) in enumerate(zip(letters, random_list)):
                if answer_number == current_question:
                    correct_letter = letter

                multiple_choice_options[letter] = self.pairs[answer_number]["answer"][0]

            if not correct_letter:
                raise Exception("There's no correct answer for some reason. ¯\\(ツ)/¯")

        print()
        for _, (key, option) in enumerate(multiple_choice_options.items()):
            print(f"{key}. {option}")
        print()

        return correct_letter, current_question, multiple_choice_options

    @staticmethod
    def user_input_sanitized():
        user_input = input("Answer: ")
        return user_input.lower()

    @staticmethod
    def clear():
        os.system("clear")

    def play(self):
        playing = True
        user_input = ""
        answer_check = ""

        while playing:
            self.print_question()
            user_input = self.user_input_sanitized()
            answer_check = self.answer_check(user_input)
            self.clear()  # To get the screen clear for the next question print like done in the last functions
            match answer_check:
                case "correct":
                    self.update_class_variables("current_question", self.next_question())
                case "seek":  # updating question variable has already been done in the function, this is easier than having to pass the question number to the main loop
                    pass
                case "show correct answer":
                    self.update_class_variables("streak_current", 0)  # breaks the streak
                case "quit":
                    playing = False  # this quits the main loop
                case "empty field":
                    pass
                case "wrong":
                    self.update_class_variables("streak_current", 0)  # breaks the streak
                case _:
                    raise Exception("Answer check returned an invalid result. Did you write the possible results correctly?")


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
        elif result in ["wrong", "correct answer"]:
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
        elif result in ["wrong", "correct answer"]:
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
            correct_letter, correct_answer, multiple_choice_options = generate_multiple_choice_answers(pairs, current_question, generate_new=False, correct_letter=correct_letter, multiple_choice_options=multiple_choice_options)

        user_input = input("Answer: ")
        user_input = user_input.lower()

        if user_input == correct_letter or correct_letter in user_input.strip() and len(user_input) < 2:
            user_input = pairs[correct_answer]["answer"][0]
            user_input = user_input.lower()

        os.system("clear")
        result, current_question = answer_check(pairs[current_question]["answer"], user_input, current_question)

        if result not in ["wrong", "empty field", "correct answer"]:
            break
        elif result in ["wrong", "correct answer"]:
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
        case "wrong" | "correct answer":
            return True, current_question, streak_current, False, lives
        case _:
            raise Exception("Uhh... How...")
    

def answer_check(correct_answers, user_input, current_question):
    for answer in correct_answers:

        answer = answer.lower()
        
        if answer == user_input or answer in user_input:
            print("Correct")
            return "correct", current_question
        
        match = re.search(r"^seek (\d+)|^seek(\d+)", user_input)
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
