# SPDX-License-Identifier: GPL-2.0-or-later
import csv
import json
import os
import time

script_dir = os.path.dirname(os.path.abspath(__file__))
settings_path = os.path.join(script_dir, "settings.json")

def pair_import(csv_file_path):
    pair0 = {
        "question": ["Wait... question zero? What's the answer though..."],
        "answer": ["luupycards"],
    }
    pairs = [pair0]
    current_pair_dict = dict()

    with open(csv_file_path, mode="r") as file:
        csv_reader = csv.reader(file)
        for row_number, row in enumerate(csv_reader, start=1):
            row = [x for x in row if x]  # removes empty slots
            if row_number % 2 != 0:  # questions
                current_pair_dict["question"] = row
            else:  # answers
                current_pair_dict["answer"] = row
                pairs.append(current_pair_dict.copy())
    return pairs


def main_menu(modes, version):
    os.system("clear")

    while True:

        print(f"Welcome to Luupycards! {version}")
        for i, mode in enumerate(modes, start=1):  # Prints all modes and their numbers
            if mode[0]:  # Checks if there's anything in the mode
                print(f"{i} or {mode[1]:<3} for {mode[0]}")
            else:
                print(i)

        selected_input = input("Type number or the full name: ")

        if selected_input.isdigit():
            selected_input = int(selected_input)
            if 0 <= selected_input - 1 < len(modes):  # Checks if input is correct
                selected_mode = selected_input - 1
                break

        elif selected_input:  # If user input is alphabetical
            found = False
            for i, sublist in enumerate(modes):
                if selected_input.lower() == sublist[0] or selected_input.lower() == sublist[1]:
                    selected_mode = i # Finds the specific mode
                    found = True
                    break

            if found:
                break

        os.system("clear")
        print(f'Invalid selection "{selected_input}", please try again.')

    return selected_mode # It isn't unbound


def settings_menu(options={"example option" : "No options available"}, locked_values=[], static_values=[]):
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
                subsetting_menu(selected_setting, user_input, options, static_values, locked_values)

        elif user_input in options and user_input:  # If user input is alphabetical
            selected_setting = user_input  # Finds the specific mode
            subsetting_menu(selected_setting, user_input, options, static_values, locked_values)

        elif user_input == "quit" or user_input == "q":
            break

        else:
            os.system("clear")
            print(f'Invalid selection "{user_input}", please try again.')            
        

def subsetting_menu(selected_setting, user_input_main, options, static_values, locked_values):
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
        options["all_time_streak"] = 0
        get_options("dump", options)


def get_options(mode="load", settings_dict={}):

    if mode == "load":
        with open(settings_path, "r") as file:  # Open in read mode
            settings_dict = json.load(file)  # Use json.load() to directly parse the file
            print("Settings loaded:", settings_dict)

    elif mode == "dump":
        with open(settings_path, "w") as file:  # Open in write mode
            json.dump(settings_dict, file, indent=4)  # Write the dictionary to the file
            print("Settings dumped successfully.")

    else:
        raise ValueError('available modes: "load", "dump"')
    return settings_dict
    



