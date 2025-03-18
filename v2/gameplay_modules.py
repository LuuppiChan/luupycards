import re
import os

import core_functions as core
import random
import string
import time
import readline  # for better input field
import logging

gamelog = logging.getLogger(__name__)

# Check if fuzzy select is available
fuzzy_is_available = False
try:
    from thefuzz import fuzz, process
    fuzzy_is_available = True
except ModuleNotFoundError:
    fuzzy_is_available = False

def determine_gamemode(current_mode: str, current_order: str, pairs: list):
    modes = [
        ["Normal", "n"],
        ["Reverse", "r"],
        ["Multiple Choice", "m"],
        ["Survive!", "s!"],
    ]
    orders = [
        ["Forward", "r"],
        ["Reverse", "re"],
        ["Random", "ro"]
    ]
    reverse = False
    order = "forward"
    game_object = MainGameplay

    match current_mode:
        case "Normal":
            game_object = Normal
        case "Reverse":
            reverse = True
            game_object = Reverse
        case "Multiple Choice":
            game_object = MultipleChoice
        case "Survive!":
            game_object = Survive

    match current_order:
        case "Forward":
            pass
        case "Reverse":
            order = "reverse"
        case "Random":
            order = "random"

    return game_object(pairs, order=order)  # This returns a ready game object


class MainGameplay:
    def __init__(self, pairs, reverse=False, current_question=1, streak_current=0, order="forward"):

        global fuzzy_is_available
        self.fuzzy_matching = fuzzy_is_available

        # These for easy reverse mode functionality
        self.question = "question"
        self.answer = "answer"
        if reverse:
            self.question = "answer"
            self.answer = "question"

        self.pairs = pairs
        self.current_question = current_question
        self.show_question_number = core.settings_value_manipulator("show current question number")
        self.streak_current = streak_current
        self.streak_all_time = core.settings_value_manipulator("all time streak")
        self.max_question = core.settings_value_manipulator("max question")  # This is true inconsistency lol
        self.all_settings = core.get_options()
        self.user_input = ""
        self.random_list = core.never_repeat_random_list(self.all_settings["min question"], self.all_settings["max question"])
        self.list_index = 0
        self.mc_correct_index = -1

        # chooses the order
        self.order = order
        if order == "reverse":
            self.order = "reverse"
        elif order == "random":
            self.order = "random"
            self.current_question = self.random_list[0]

        self.enabled_prints = {
            "correct answer" : True,
            "invalid seek" : True,
            "valid seek" : True,
            "show correct answer" : True,
            "return to main menu" : True,
            "empty field" : True,
            "wrong answer" : True,
            "fuzzy correct" : True,
        }
        self.enabled_answer_checks = {
            "correct answer" : True,
            "fuzzy correct": True,
            "seek" : True,
            "show correct answer" : True,
            "quit" : True,
            "empty field" : True,
            "wrong answer" : True,
        }
        self.show_correct_binds = ["c", "correct", "ｃ"]
        self.quit_binds = ["q", "quit"]

    def new_random_list(self):
        self.random_list = core.never_repeat_random_list(self.all_settings["min question"],
                                                         self.all_settings["max question"])
        return self.random_list

    def print_correct_answer(self):
        if self.enabled_prints["correct answer"]:
            print("Correct")
            return "Correct"

    def print_invalid_seek(self, question_number):
        if self.enabled_prints["invalid seek"]:
            print(f'"{question_number}" is an invalid seek number. (Max: {self.max_question})')
            return f'"{question_number}" is an invalid seek number. (Max: {self.max_question})'

    def print_valid_seek(self, question_number):
        if self.enabled_prints["valid seek"]:
            print(f"Seeking from {self.current_question} to {question_number}...")
            return f"Seeking from {self.current_question} to {question_number}..."

    def print_show_correct_answer(self, correct_answers):
        if self.enabled_prints["show correct answer"]:
            print(f"Correct answers: {" / ".join(correct_answers)}")
            return f"Correct answers: {" / ".join(correct_answers)}"

    def print_return_to_main_menu(self):
        if self.enabled_prints["return to main menu"]:
            print("Returning to main menu...")
            return "Returning to main menu..."

    def print_empty_field(self):
        if self.enabled_prints["empty field"]:
            print("Please type something...")
            return "Please type something..."

    def print_wrong_answer(self):
        if self.enabled_prints["wrong answer"]:
            print(f'"{self.user_input.capitalize()}" is not a correct answer.')
            return f'"{self.user_input.capitalize()}" is not a correct answer.'

    def print_fuzzy_correct(self, correct_answers):
        if self.enabled_prints["fuzzy correct"]:
            print(f"Almost correct! {" / ".join(correct_answers)}")
            return f"Almost correct! {" / ".join(correct_answers)}"

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
        return f"{f"{self.current_question}. " if self.show_question_number else ""}{" / ".join(self.pairs[self.current_question][self.question])}"

    def fuzzy_check(self, correct_answers):
        processed = process.extract(self.user_input, correct_answers)
        for items in processed:
            if items[1] >= self.all_settings["fuzzy select percent"]:
                return True  # Match was found

        return False  # Match was not found

    def answer_check(self) -> str:
        correct_answers = self.pairs[self.current_question][self.answer]
        user_input = self.user_input

        if self.enabled_answer_checks["correct answer"]:
            # check for correct answer in user_input, iterates through all answer candidates
            for answer in correct_answers:
                answer = answer.lower()
                if answer == user_input:  # IDK if "answer in user_input" should be included. It makes it easier but has some side effects. Or just token matching in fuzzy?
                    self.next_question()
                    self.streak_current += 1
                    self.print_correct_answer()
                    return "correct"

        if self.enabled_answer_checks["fuzzy correct"]:
            if self.fuzzy_matching:  # checks if fuzzy matching is available
                if self.fuzzy_check(correct_answers):
                    self.next_question()
                    self.streak_current += 1
                    self.print_fuzzy_correct(correct_answers)
                    return "fuzzy correct"

        if self.enabled_answer_checks["seek"]:
            match = re.search(r"^seek (\d+)", user_input)
            if match:  # seeking
                question_number = int(match.group(1))
                if question_number > self.max_question:
                    self.print_invalid_seek(question_number)
                else:
                    self.print_valid_seek(question_number)
                    self.update_class_variables("current_question", question_number)
                return "seek"

        if self.enabled_answer_checks["show correct answer"]:
            if user_input in self.show_correct_binds:  # show correct answer
                self.update_class_variables("streak_current", 0)  # breaks the streak
                self.print_show_correct_answer(correct_answers)
                return "show correct answer"

        if self.enabled_answer_checks["quit"]:
            if user_input in self.quit_binds:  # quit to main menu
                self.print_return_to_main_menu()
                return "quit"

        if self.enabled_answer_checks["empty field"]:
            if not user_input or re.findall("^ *$", user_input):  # checks if user_input is empty
                self.print_empty_field()
                return "empty field"

        if self.enabled_answer_checks["wrong answer"]:
            self.update_class_variables("streak_current", 0)  # breaks the streak
            self.print_wrong_answer()
            return "wrong"  # if there's no match, the answer is incorrect

        raise Exception("Please enable wrong answer check.")

    def next_question_plus_one(self):
        self.current_question += 1
        try:
            self.pairs[self.current_question]
        except IndexError:
            self.current_question = self.all_settings["min question"]

    def next_question_minus_one(self):
        self.current_question -= 1
        try:
            self.pairs[self.current_question]
        except IndexError:
            self.current_question = self.max_question

    def next_question_random(self):
        self.list_index += 1
        try:
            self.current_question = self.random_list[self.list_index]
        except IndexError:  # Wrap around
            self.new_random_list()  # creates new list for more randomness with smaller pair sets
            self.list_index = 0
            self.current_question = self.random_list[self.list_index]

    def next_question(self):
        # Check how the next question should be done and return it.
        if self.order == "forward":
            self.next_question_plus_one()
        elif self.order == "reverse":
            self.next_question_minus_one()
        elif self.order == "random":
            self.next_question_random()
        else:
            raise Exception("Someone has set an invalid question order.")

    def generate_multiple_choice_answers(self, generate_new=True, correct_letter="", multiple_choice_options=None):

        if multiple_choice_options is None:
            multiple_choice_options = {}
        if generate_new:
            options = core.get_options()
            max_options = options["multiple choice max options"]
            random_list = core.never_repeat_random_list(1, core.settings_value_manipulator("max question"))

            if len(random_list) < max_options:
                raise Exception(
                    f"Not enough unique pairs to generate {max_options} options from {len(random_list)} pairs.")

            if self.current_question in random_list:
                random_list.remove(self.current_question)

            random_list = random_list[:max_options]  # one less than max_options
            random_list.append(self.current_question)

            while len(random_list) != max_options:
                random_list.pop(0)

            random.shuffle(random_list)

            letters = string.ascii_lowercase

            for _, (letter, answer_number) in enumerate(zip(letters, random_list)):
                if answer_number == self.current_question:
                    correct_letter = letter

                multiple_choice_options[letter] = self.pairs[answer_number]["answer"][0]

            if not correct_letter:
                raise Exception("There's no correct answer for some reason. ¯\\(ツ)/¯")

        print()
        for _, (key, option) in enumerate(multiple_choice_options.items()):
            print(f"{key}. {option}")
        print()

        return correct_letter, multiple_choice_options

    def generate_multiple_choice_answers_gui(self, generate_new=True, correct_index=-1, multiple_choice_options=None) -> (int, list):
        if multiple_choice_options is None:
            multiple_choice_options = []

        if correct_index != -1:
            self.mc_correct_index = correct_index

        if generate_new:
            gamelog.debug("New mc options")

            mc_max_options = core.settings_value_manipulator("multiple choice max options")
            gamelog.debug("max_options: %s", mc_max_options)
            random_index_list = core.never_repeat_random_list(1, core.settings_value_manipulator("max question"))
            gamelog.debug("random_index_list: %s", random_index_list)
            # list from 1 to max question

            multiple_choice_options.append(self.pairs[self.current_question].copy())  # appends the correct pair

            # this chooses random pairs out of the pairs, but leaves space for the correct one
            for i in range(mc_max_options - 1):
                if random_index_list[i] == self.current_question:  # skips if it's the correct since it's already in
                    continue
                multiple_choice_options.append(self.pairs[random_index_list[i]])

            random.shuffle(multiple_choice_options)  # randomize!

            # converts the pairs into answer strings
            for i, option in enumerate(multiple_choice_options):
                # finds the correct index
                if self.pairs[self.current_question] == option:
                    self.mc_correct_index = i

                # change the same index to the answer
                multiple_choice_options[i] = " / ".join(option["answer"])

        return self.mc_correct_index, multiple_choice_options

    def user_input_sanitized(self):
        self.user_input = input("Answer: ").lower()

    @staticmethod
    def clear():
        # This method is not needed in graphical interfaces
        pass
        #os.system("clear")

    def check_max_streak(self):
        if self.streak_current > self.streak_all_time:
            core.settings_value_manipulator("all time streak", "dump", self.streak_current)
            self.streak_all_time = core.settings_value_manipulator("all time streak")

    def streak_question_and_input(self):
        self.check_max_streak()
        self.print_question()
        self.user_input_sanitized()

    def play(self):
        playing = True
        answer_check = ""

        while playing:
            self.streak_question_and_input()
            self.clear()  # To get the screen clear for the next question print like done in the last functions
            answer_check = self.answer_check()
            # Other return values have already done their job in the answer_check()
            if answer_check == "quit":
                return self.streak_current

    def settings_update(self):
        self.show_question_number = core.settings_value_manipulator("show current question number")
        self.streak_all_time = core.settings_value_manipulator("all time streak")
        self.max_question = core.settings_value_manipulator("max question")  # This is true inconsistency lol
        self.all_settings = core.get_options()
        self.random_list = core.never_repeat_random_list(self.all_settings["min question"],
                                                         self.all_settings["max question"])

    def answer_check_gui(self, user_input="") -> tuple[str, str] | str:
        correct_answers = self.pairs[self.current_question][self.answer]
        if not user_input:
            user_input = self.user_input

        if self.enabled_answer_checks["correct answer"]:
            # check for correct answer in user_input, iterates through all answer candidates
            for answer in correct_answers:
                answer = answer.lower()
                if answer == user_input:  # IDK if "answer in user_input" should be included. It makes it easier but has some side effects. Or just token matching in fuzzy?
                    self.next_question()
                    self.streak_current += 1
                    return "correct", self.print_correct_answer()

        if self.enabled_answer_checks["fuzzy correct"]:
            if self.fuzzy_matching:  # checks if fuzzy matching is available
                if self.fuzzy_check(correct_answers):
                    self.next_question()
                    self.streak_current += 1
                    return "fuzzy correct", self.print_fuzzy_correct(correct_answers)

        if self.enabled_answer_checks["seek"]:
            match = re.search(r"^seek (\d+)", user_input)
            if match:  # seeking
                info_return = ""
                question_number = int(match.group(1))
                if question_number > self.max_question:
                    info_return = self.print_invalid_seek(question_number)
                else:
                    info_return = self.print_valid_seek(question_number)
                    self.current_question = question_number
                return "seek", info_return

        if self.enabled_answer_checks["show correct answer"]:
            if user_input in self.show_correct_binds:  # show correct answer
                self.streak_current = 0  # breaks the streak
                return "show correct answer", self.print_show_correct_answer(correct_answers)

        if self.enabled_answer_checks["quit"]:
            if user_input in self.quit_binds:  # quit to main menu
                return "quit", self.print_return_to_main_menu()

        if self.enabled_answer_checks["empty field"]:
            if not user_input or re.findall("^ *$", user_input):  # checks if user_input is empty
                return "empty field", self.print_empty_field()

        if self.enabled_answer_checks["wrong answer"]:
            self.streak_current = 0  # breaks the streak
            return "wrong", self.print_wrong_answer()  # if there's no match, the answer is incorrect

        raise Exception("Please enable wrong answer check.")

    def play_gui(self):
        # The line under will break never repeat random
        #self.settings_update()

        self.check_max_streak()

        return self.print_question()


class Normal(MainGameplay):
    pass


class Reverse(MainGameplay):
    def __init__(self, pairs, reverse=True, current_question=1, streak_current=0, order="forward"):
        super().__init__(pairs, reverse, current_question, streak_current, order)


class MultipleChoice(MainGameplay):
    def __init__(self, pairs, reverse=False, current_question=1, streak_current=0, order="forward"):
        super().__init__(pairs, reverse, current_question, streak_current, order)
        self.enabled_answer_checks["fuzzy correct"] = False

    def play(self):  # When seeking it keeps the old answers
        playing = True
        answer_check = ""
        # These are multiple choice specific
        multiple_choice_options = {}
        correct_letter = ""

        while playing:
            self.check_max_streak()
            self.print_question()

            # Multiple choice specific
            if not multiple_choice_options:
                correct_letter, multiple_choice_options = self.generate_multiple_choice_answers()

            else:
                correct_letter, multiple_choice_options = self.generate_multiple_choice_answers(generate_new=False, correct_letter=correct_letter, multiple_choice_options=multiple_choice_options)

            self.user_input_sanitized()

            # Multiple choice specific
            if self.user_input == correct_letter or correct_letter in self.user_input.strip() and len(self.user_input) <= 2:
                self.user_input = self.pairs[self.current_question][self.answer][0]
                self.user_input = self.user_input.lower()

            self.clear()

            answer_check = self.answer_check()
            # Other return values have already done their job in the answer_check()
            if answer_check == "quit":
                return self.streak_current
            elif answer_check == "correct":  # Multiple choice specific
                multiple_choice_options = {}  # This is to make it generate new options
            elif answer_check =="seek":
                multiple_choice_options = {}


class Survive(MainGameplay):
    def __init__(self, pairs, reverse=False, current_question=1, streak_current=0, order="random"):
        super().__init__(pairs, reverse, current_question, streak_current, order)
        self.streak_all_time = core.settings_value_manipulator("all time survival streak")
        self.lives = core.settings_value_manipulator("lives")
        self.enabled_prints["wrong answer"] = False
        self.enabled_prints["show correct answer"] = False

    def check_max_streak(self):
        if self.streak_current > self.streak_all_time:
            core.settings_value_manipulator("all time survival streak", "dump", self.streak_current)
            self.streak_all_time = core.settings_value_manipulator("all time survival streak")

    def print_question(self):
        print(f"Current survival streak: {self.streak_current}, All time survival streak: {self.streak_all_time}")
        print(f"{f"{self.current_question}. " if self.show_question_number else ""}{" / ".join(self.pairs[self.current_question][self.question])}")
        return f"{f"{self.current_question}. " if self.show_question_number else ""}{" / ".join(self.pairs[self.current_question][self.question])}"

    def return_correct_answers(self):
        return f"Correct answers: {" / ".join(self.pairs[self.current_question][self.answer])}"

    def print_lives(self):
        print("Lives left: ", end="")
        for _ in range(self.lives):
            print(" ", end="")
        else:
            print()

    def play(self):
        playing = True
        answer_check = ""

        while playing:
            self.print_lives()
            self.streak_question_and_input()
            self.clear()  # To get the screen clear for the next question print like done in the last functions
            answer_check = self.answer_check()
            # Other return values have already done their job in the answer_check()
            match answer_check:
                case "quit":
                    return self.streak_current
                case "wrong":
                    print(f"Wrong, correct answer: {self.return_correct_answers()}")
                    # self.current_question += 1  # removing this might make learning easier
                    self.lives -= 1
                case "show correct answer":
                    print(f"The correct answer was: {self.return_correct_answers()}")
                    # self.current_question += 1  # removing this might make learning easier
                    self.lives -= 1

            if self.lives <= 0:
                self.clear()
                print(f"The correct answer was: {self.return_correct_answers()}")
                print("Game over!")
                time.sleep(5)
                return 0


# In this one the questions are images that are executed based on what's in the first question cell.
# This could be used by making a .csv and then on that directory a subdirectory with the images.
class Images(MainGameplay):
    def __init__(self, pairs, reverse=False, current_question=1, streak_current=0, order="normal"):
        super().__init__(pairs, reverse, current_question, streak_current, order)
