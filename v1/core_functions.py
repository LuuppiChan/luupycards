# SPDX-License-Identifier: GPL-2.0-or-later
import csv
import json
import os
import re
import time
import random
import readline # for better input field

pairs = [1,1]
pairs.clear()

script_dir = os.path.dirname(os.path.abspath(__file__))
settings_path = os.path.join(script_dir, "settings.json")


class Menu:
    def __init__(self, main_modes, special_modes, sub_modes, title="Title", sub_title="N/A"):
        self.main_modes = main_modes
        self.special_modes = special_modes
        self.sub_modes = sub_modes
        self.sub_title = sub_title
        self.option_number = 1
        self.title = title
        self.user_input = ""  # Initialize variable
        self.selected_mode = ""  # Initialize it for later use
        self.selected_sub_mode = ""

        # Make a list with all the modes. This might be the easiest way to compare the user_input.
        self.all_modes = ["mode zero"]
        self.all_modes.append(main_modes)
        self.all_modes.append(special_modes)


    def print_titles(self):
        if self.title: print(self.title)
        if self.sub_title: print(self.sub_title)

    def print_main_modes(self):
        for i, mode in enumerate(self.main_modes, start=1):  # Prints all modes and their numbers
            if mode[0]:  # Checks if there's anything in the mode
                print(f"{i:<2} or {mode[1]:<3} for {mode[0]}")
            else:
                print(i)
            self.option_number = i + 1  # puts the next option number to global variable

    def print_special_modes(self):
        for i, mode in enumerate(self.special_modes, start=self.option_number):  # Prints all modes and their numbers
            if mode[0]:  # Checks if there's anything in the mode
                print(f"{i:<2} or {mode[1]:<3} for {mode[0]}")
            else:
                print(i)

    def user_input_check(self):
        self.user_input = self.user_input.lower()
        for i, mode in enumerate(self.all_modes):
            if not i:
                continue

            for sub_i, sub_mode in enumerate(self.sub_modes):
                full_combination = mode[0], sub_mode[0]
                alias_combination = mode[1] + sub_mode[1]
                if self.user_input in [full_combination, alias_combination]:
                    self.selected_sub_mode = self.user_input.find(sub_mode[0]) if self.user_input.find(sub_mode[0]) != -1 else self.user_input.find(sub_mode[1])

            if self.user_input in [i, mode[0], mode[1]]:
                self.selected_mode = i

    def run(self):
        menu_is_open = True
        while menu_is_open:
            self.print_titles()
            self.print_main_modes()
            print()
            self.print_special_modes()
            self.user_input = input("Name, alias or number: ")


def pair_import(csv_file_path):
    global pairs
    pair0 = {
        "question": ["Wait... question zero? What's the answer though..."],
        "answer": ["luupycards"],
    }
    pairs = [pair0]
    current_pair_dict = dict()

    with open(csv_file_path, mode="r") as file:
        csv_reader = csv.reader(file)
        for row_number, row in enumerate(csv_reader, start=1):
            row = [x.strip() for x in row if x]  # removes empty slots and useless    whitespaces    .
            if row_number % 2 != 0:  # questions
                current_pair_dict["question"] = row
            else:  # answers
                current_pair_dict["answer"] = row
                pairs.append(current_pair_dict.copy())
    return pairs


def main_menu(modes, version, title=""):

    if not title:
        title = f"Welcome to Luupycards! {version}"
    os.system("clear")
    print(f'Loaded {settings_value_manipulator("max question")} pairs.')

    while True:

        print(title)
        for i, mode in enumerate(modes, start=1):  # Prints all modes and their numbers
            if mode[0]:  # Checks if there's anything in the mode
                print(f"{i:<2} or {mode[1]:<3} for {mode[0]}")
            else:
                print(i)

        selected_input = input("Type number, alias or the full name: ")
        selected_input = selected_input.strip()

        if selected_input.isdigit():
            selected_input = int(selected_input)
            if 0 <= selected_input - 1 < len(modes):  # Checks if input is correct
                selected_mode = selected_input - 1
                break

        elif selected_input:  # If user input is alphabetical
            found = False
            for i, sublist in enumerate(modes):
                if selected_input.lower() == sublist[0].lower() or selected_input.lower() == sublist[1].lower():
                    selected_mode = i # Finds the specific mode
                    found = True
                    break

            if found:
                break

        os.system("clear")
        print(f'Invalid selection "{selected_input}", please try again.')

    return selected_mode # It isn't unbound


def settings_menu(options=None, locked_values=None, static_values=None):
    if options is None:
        options = {}
    if locked_values is None:
        locked_values = []
    if static_values is None:
        static_values = []

    os.system("clear")
    while True:

        print("Settings menu")
        for number, (key, value) in enumerate(options.items(), start=1):
            print(f'{number}. for "{key}"')
            print(f'Current value: "{value}"')
            print()
        else:
            print("q for quit")
            print()

        user_input = input("Setting: ")

        if user_input.isdigit():
            user_input = int(user_input)
            if 0 <= user_input - 1 < len(options):  # Checks if input is correct
                key_list = list(options.keys())
                selected_setting = key_list[user_input - 1]
                subsetting_menu(selected_setting, options, static_values, locked_values)

        elif user_input in options and user_input:  # If user input is alphabetical
            selected_setting = user_input  # Finds the specific mode
            subsetting_menu(selected_setting, options, static_values, locked_values)

        elif user_input == "quit" or user_input == "q":
            check_for_invalid_setting_values()
            break

        else:
            os.system("clear")
            print(f'Invalid selection "{user_input}", please try again.')


def subsetting_menu(selected_setting, options, static_values, locked_values):
    user_input_subsetting = input("Insert a new value: ")

    if selected_setting in static_values:
        static_value_functions(user_input_subsetting, options, static_values, selected_setting)
        return

    elif selected_setting in locked_values:
        os.system("clear")
        print("This value is locked and cannot be changed from here.")
        time.sleep(2)

    else:
        if user_input_subsetting.lower() == "true":
            selected_value = True
        elif user_input_subsetting.lower() == "false":
            selected_value = False
        elif user_input_subsetting.isdigit():
            selected_value = int(user_input_subsetting)
        else:
            selected_value = 0

        os.system("clear")
        options[selected_setting] = selected_value
        get_options("dump", options)


def static_value_functions(user_input_subsetting, options, static_values, selected_setting):

    os.system("clear")

    # other static value functions can be added here
    if selected_setting == static_values[0] and user_input_subsetting.lower() == "true":
        options["all time streak"] = 0
        get_options("dump", options)

    elif selected_setting == static_values[1] and user_input_subsetting.lower() == "true":
        options["all time survival streak"] = 0
        get_options("dump", options)


def get_options(mode="load", settings_dict=None):
    if settings_dict is None:
        settings_dict = {}

    if mode == "load":
        with open(settings_path, "r") as file:  # Open in read mode
            settings_dict = json.load(file)  # Use json.load() to directly parse the file
            #print("Settings loaded:", settings_dict)

    elif mode == "dump":
        with open(settings_path, "w") as file:  # Open in write mode
            json.dump(settings_dict, file, indent=4)  # Write the dictionary to the file
            #print("Settings dumped successfully.")

    else:
        raise Exception('available modes: "load", "dump"')
    return settings_dict


def never_repeat_random_list(min_pair_number, amount_of_pairs):
    if min_pair_number < 0:
        min_pair_number = 1
    number_list = list(range(min_pair_number, amount_of_pairs + 1))
    random.shuffle(number_list)
    return number_list


def fancy_line_print(string):
    collect_the_string = ""
    time.sleep(.5)
    for x in string:
        collect_the_string = collect_the_string + x
        time.sleep(0.5) if x == " " else None
        time.sleep(0.5) if x == "." else None

        print(f"\r{collect_the_string}", end='')
        time.sleep(.05)
    time.sleep(3)


def settings_value_manipulator(option, mode="return", new_value: int | bool = 0):
    options = get_options()
    if mode in ["write", "dump"]:
        options[option] = new_value
        get_options("dump", options)
        return None
    elif mode == "return":
        return options[option]

def check_for_invalid_setting_values():
    global pairs
    options = get_options()
    options_orig = options.copy()

    if options["all time streak"] < -1:
        options["all time streak"] = 0
    if options["reset all time streak"]:
        options["reset all time streak"] = False
    if options["min question"] > options["max question"] or options["min question"] < 0:
        options["min question"] = 1
    if options["max question"] < options["min question"]:
        options["max question"] = options["min question"] + 1
    if options["max question"] > len(pairs) - 1:
        options["max question"] = len(pairs) - 1
    if options["multiple choice max options"] > 26:
        options["multiple choice max options"] = 5
    if options["lives"] < 1:
        options["lives"] = 5
    if options["fuzzy select percent"] >= 100 or 1 > options["fuzzy select percent"]:
        options["fuzzy select percent"] = 90

    if options_orig != options:
        print("One or more of your setting values is illegal, fixing it in 5 seconds...")
        fancy_line_print("5. 4. 3. 2. 1. 0.")
        get_options("dump", options)

# Most useful function ever!
def print_empty_lines(amount):
    for x in range(amount):
        print()