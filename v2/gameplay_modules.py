import re

import core_functions as core
import random
import logging

gamelog = logging.getLogger(__name__)

# Check if fuzzy select is available
fuzzy_is_available = False
try:
    from thefuzz import fuzz, process
    fuzzy_is_available = True
except ModuleNotFoundError:
    fuzzy_is_available = False

def determine_gamemode(current_mode: str, current_order: str, pairs: list, reverse=False, current_question=0, current_streak=0, regex=False):
    modes = [
        ["Normal", "n"],
        ["Multiple Choice", "m"],
        ["Survive!", "s!"],
    ]
    orders = [
        ["Forward", "r"],
        ["Reverse", "re"],
        ["Random", "ro"]
    ]
    order = "forward"
    game_object = MainGameplay

    match current_mode:
        case "Normal":
            game_object = MainGameplay
        case "Multiple Choice":
            game_object = MultipleChoice
        case "Survive!":
            game_object = Survive

    match current_order:
        case "Forward":
            pass  # this is the default
        case "Reverse":
            order = "reverse"
        case "Random":
            order = "random"

    return game_object(pairs, order=order, reverse=reverse, current_question=current_question, streak_current=current_streak, regex=regex)  # This returns a ready game object


class MainGameplay:
    def __init__(self, pairs, reverse=False, current_question=1, streak_current=0, order="forward", regex=False):

        global fuzzy_is_available
        self.fuzzy_matching = fuzzy_is_available

        # These for easy reverse mode functionality
        self.question = "question"
        self.answer = "answer"
        if reverse:
            self.question = "answer"
            self.answer = "question"

        # Maybe like import the whole dictionary and then assign values from it to variables?
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
            self.current_question = self.max_question
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
            "regex" : regex,
        }
        self.show_correct_binds = ["c", "correct", "ｃ"]
        self.quit_binds = ["q", "quit"]

    def new_random_list(self):
        self.random_list = core.never_repeat_random_list(self.all_settings["min question"],
                                                         self.all_settings["max question"])
        return self.random_list

    def print_correct_answer(self):
        if self.enabled_prints["correct answer"]:
            return "Correct"

    def print_invalid_seek(self, question_number):
        if self.enabled_prints["invalid seek"]:
            return f'"{question_number}" is an invalid seek target. (Max: {len(self.pairs) - 1})'

    def print_valid_seek(self, question_number):
        if self.enabled_prints["valid seek"]:
            return f"Seeking from {self.current_question} to {question_number}..."

    def print_show_correct_answer(self, correct_answers):
        if self.enabled_prints["show correct answer"]:
            return f"Correct answers: {" / ".join(correct_answers)}"

    def print_return_to_main_menu(self):
        if self.enabled_prints["return to main menu"]:
            return "Returning to main menu..."

    def print_empty_field(self):
        if self.enabled_prints["empty field"]:
            return "Please type something..."

    def print_wrong_answer(self):
        if self.enabled_prints["wrong answer"]:
            return f'"{self.user_input.capitalize()}" is not a correct answer.'

    def print_fuzzy_correct(self, correct_answers):
        if self.enabled_prints["fuzzy correct"]:
            return f"Almost correct! {" / ".join(correct_answers)}"

    def print_question(self) -> tuple[str, list[str], str]:
        return f"{" / ".join(self.pairs[self.current_question][self.question])}", self.pairs[self.current_question][self.question], f"{self.current_question}. " if self.show_question_number else ""

    def fuzzy_check(self, correct_answers):
        for answer in correct_answers:
            if (fuzz.ratio(self.user_input.lower(), answer) >
                    self.all_settings["fuzzy select percent"] or
                    fuzz.ratio(self.user_input.lower(), " / ".join(correct_answers)) >
                    self.all_settings["fuzzy select percent"]):
                return True  # Match was found

        return False  # Match was not found

    def next_question_plus_one(self):
        if self.current_question >= self.max_question:
            self.current_question = self.all_settings["min question"]
        elif self.current_question < self.all_settings["min question"]:  # usually 1
            self.current_question = self.max_question
        else:
            self.current_question += 1

    def next_question_minus_one(self):
        if self.current_question <= self.all_settings["min question"]:  # usually 1
            self.current_question = self.max_question
        elif self.current_question > self.max_question:
            self.current_question = self.all_settings["min question"]
        else:
            self.current_question -= 1

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

    def generate_multiple_choice_answers_gui(self, generate_new=True, correct_index=-1, multiple_choice_options=None) -> tuple[int, list[list[str, str]]]:
        if multiple_choice_options is None:
            multiple_choice_options = []

        if correct_index != -1:
            self.mc_correct_index = correct_index

        if generate_new:

            mc_max_options = self.all_settings["multiple choice max options"]
            random_index_list = core.never_repeat_random_list(1, self.max_question)
            # list from 1 to max question

            # this chooses random pairs out of the pairs, but doesn't leave space for the correct one yet
            for i in range(mc_max_options +1):
                if random_index_list[i] == self.current_question:  # skips if it's the correct since it's already in
                    continue
                multiple_choice_options.append(self.pairs[random_index_list[i]])

            # this checks if the length is over the target and removes accordingly
            while len(multiple_choice_options) != mc_max_options -1:  # it should remove up to 2 incorrect pairs...
                multiple_choice_options.pop(0)

            multiple_choice_options.append(self.pairs[self.current_question].copy())  # appends the correct pair

            random.shuffle(multiple_choice_options)  # randomize!

            # converts the pairs into answer strings
            for i, option in enumerate(multiple_choice_options):
                # finds the correct index
                if self.pairs[self.current_question] == option:
                    self.mc_correct_index = i

                # change the same index to the answer
                # the first one is only the first question and the second one is the full question
                multiple_choice_options[i]: list[str, str] = [option[self.answer][0], " / ".join(option[self.answer])]

        return self.mc_correct_index, multiple_choice_options

    def check_max_streak(self):
        if self.streak_current > self.streak_all_time:
            core.settings_value_manipulator("all time streak", "dump", self.streak_current)
            self.streak_all_time = core.settings_value_manipulator("all time streak")

    def update_streaks(self):
        self.streak_all_time = core.settings_value_manipulator("all time streak")

    def settings_update(self, update_random_list=False):
        max_question = core.settings_value_manipulator("max question")
        pair_length = len(self.pairs)
        if pair_length -1 < max_question:
            max_question = len(self.pairs) - 1
            core.settings_value_manipulator("max question", "dump", max_question)
            update_random_list = True  # update needed since the settings number is invalid for some reason
        else:
            max_question = core.settings_value_manipulator("max question")

        min_question = core.settings_value_manipulator("min question")

        # updates only if there are changes to these 2 settings or force is on
        if max_question != self.max_question or min_question != self.all_settings["min question"] or update_random_list:
            self.random_list = core.never_repeat_random_list(min_question, max_question)

        self.show_question_number = core.settings_value_manipulator("show current question number")
        self.check_max_streak()
        self.update_streaks()
        self.max_question = max_question
        self.all_settings = core.get_options()

    def regex_check(self, correct_answers, user_input) -> tuple[str, str] | str | None:
        try:
            # check for correct answer in user_input, iterates through all answer candidates
            for answer in correct_answers:
                match = re.search(answer, user_input)
                if match:
                    self.next_question()
                    self.streak_current += 1
                    return "correct", self.print_correct_answer()

            if len(correct_answers) > 1:
                pattern = r"(?: ?[ /|;,]+ ?| ?or ?)"
                regex = f"^{pattern.join(f"(?:{ans})" for ans in correct_answers)}$"
                match = re.search(regex, user_input)

                if match:  # or the user has inputted all the options
                    self.next_question()
                    self.streak_current += 1
                    return "correct", self.print_correct_answer()
        except re.PatternError:
            return "wrong", "Invalid RegEx! (re.PatternError)"

        return None

    def answer_check_gui(self, user_input="") -> tuple[str, str] | str:
        # lowercase every check
        # Also strip trailing spaces
        correct_answers: list[str] = self.pairs[self.current_question][self.answer]
        when_showing_correct_answers = self.pairs[self.current_question][self.answer]
        for i, correct_answer in enumerate(correct_answers):
            correct_answers[i] = correct_answer.lower().strip()

        if not user_input:
            user_input = self.user_input.lower().strip()
        else:
            user_input = user_input.lower().strip()

        if "regex" in self.pairs[self.current_question]:
            flag_exists = True
            force_regex = self.pairs[self.current_question]["regex"]
        else:
            flag_exists = False

        if self.enabled_answer_checks["correct answer"]:
            # check for correct answer in user_input, iterates through all answer candidates
            for answer in correct_answers:
                if answer == user_input or answer in user_input:  # IDK if "answer in user_input" should be included. It makes it easier but has some side effects. Or just token matching in fuzzy?
                    self.next_question()
                    self.streak_current += 1
                    return "correct", self.print_correct_answer()

            try:
                if len(correct_answers) > 1:
                    pattern = r"(?: ?[ /|;,]+ ?| ?or ?)"
                    regex = f"^{pattern.join(re.escape(ans) for ans in correct_answers)}$"
                    match = re.search(regex, user_input)

                    if match:  # or the user has inputted all the options
                        self.next_question()
                        self.streak_current += 1
                        return "correct", self.print_correct_answer()
            except re.PatternError:
                pass

        # Regex checks
        if flag_exists:
            if force_regex:  # it's really not unbound here
                regex_result = self.regex_check(correct_answers, user_input)
                if regex_result:
                    return regex_result

        elif self.enabled_answer_checks["regex"]:
            regex_result = self.regex_check(correct_answers, user_input)
            if regex_result:
                return regex_result

        if self.enabled_answer_checks["fuzzy correct"]:
            if self.fuzzy_matching:  # checks if fuzzy matching is available
                if self.fuzzy_check(correct_answers):
                    self.next_question()
                    self.streak_current += 1
                    return "fuzzy correct", self.print_fuzzy_correct(correct_answers)

        if self.enabled_answer_checks["seek"]:
            # absolute seek (normal)
            match = re.search(r"^seek (\d+)", str(user_input))
            if match:  # seeking
                info_return = ""
                question_number = int(match.group(1))
                if 0 <= question_number < len(self.pairs):
                    info_return = self.print_valid_seek(question_number)
                    self.current_question = question_number
                else:
                    info_return = self.print_invalid_seek(question_number)
                return "seek", info_return

            # relative seek (new)
            match = re.search(r"^seek ([\+\-])(\d+)", str(user_input))
            if match:
                info_return = ""
                offset = int(match.group(1) + match.group(2))
                question_number = self.current_question + offset
                if 0 <= question_number < len(self.pairs):
                    info_return = self.print_valid_seek(question_number)
                    self.current_question = question_number
                else:
                    info_return = self.print_invalid_seek(question_number)
                return "seek", info_return


        if self.enabled_answer_checks["show correct answer"]:
            if user_input in self.show_correct_binds:  # show correct answer
                self.streak_current = 0  # breaks the streak
                return "show correct answer", self.print_show_correct_answer(when_showing_correct_answers)

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

    def play_gui(self) -> tuple[str, list[str], str]:
        self.settings_update()

        return self.print_question()


class MultipleChoice(MainGameplay):
    def __init__(self, pairs, reverse=False, current_question=1, streak_current=0, order="forward", regex=False):
        super().__init__(pairs, reverse, current_question, streak_current, order, regex)
        self.enabled_answer_checks["fuzzy correct"] = False


class Survive(MainGameplay):
    def __init__(self, pairs, reverse=False, current_question=1, streak_current=0, order="random", regex=False):
        super().__init__(pairs, reverse, current_question, streak_current, order, regex)
        self.streak_all_time = core.settings_value_manipulator("all time survival streak")
        self.lives = core.settings_value_manipulator("lives")
        self.enabled_prints["wrong answer"] = False  # It's a print, not the check!

    def check_max_streak(self):
        if self.streak_current > self.streak_all_time:
            core.settings_value_manipulator("all time survival streak", "dump", self.streak_current)
            self.streak_all_time = core.settings_value_manipulator("all time survival streak")

    def update_streaks(self):
        self.streak_all_time = core.settings_value_manipulator("all time survival streak")

    def return_correct_answers(self) -> str:
        return f"Correct answers: {" / ".join(self.pairs[self.current_question][self.answer])}"
