import csv
import json
import os
import re
import random

from pathlib import Path
import logging
import shutil

corelog = logging.getLogger(__name__)

script_dir = os.path.dirname(os.path.abspath(__file__))
settings_path = os.path.join(script_dir, "settings.json")
pairs = list()

######################################
### This makes the code Linux only ###  I don't think it's anymore though.
######################################

# static settings path
home_dir = Path.home()
static_path = f"{home_dir}/.cache/luupycards"
settings_filename = "settings.json"
static_settings_path = os.path.join(static_path, settings_filename)

# creates the static dir if it doesn't exist
os.makedirs(static_path, exist_ok=True)  # for cross-platform compatibility

# If there's no settings file, it creates one.
if not os.path.isfile(static_settings_path):
    shutil.copy(settings_path, static_settings_path)  # for cross-platform compatibility

def get_data_dir() -> str:
    home_dir = Path.home()
    static_path = f"{home_dir}/.cache/luupycards"
    return static_path


class PairImport:
    def __init__(self):
        self.default_json = True
        self.jp_mode = False
        self.sentences = False
        self.automatic = False
        self.first_time = True

    pair0 = {
        "question": ["Wait... question zero? What's the answer though..."],
        "answer": ["Luupycards"],
        "question tooltip": "Congrats for finding an easter egg!",
        "answer tooltip": "I wonder what the game is called...",
        "regex": False,
    }
    tooltip_regex: str = r"\{\s*tooltip\s*=\s*[\"'](.*)[\"']\s*\}"
    regex_enabled_regex: str = r"\{\s*regex\s*=\s*[\"']?([Tt]rue|[Ff]alse|1|0|[Yy]es|[Nn]o)[\"']?\s*\}"

    def determine_pair_file(self, file_path, jp_mode=False, sentences=False) -> list[dict[str, list[str] | str | bool]]:
        self.automatic = True
        pairs = list()

        json_match = re.search(fr"^.*(\.json|\.csv)$", file_path)
        if json_match.group(1).lower() == ".json":
            corelog.info("Input file is json")
            self.jp_mode = jp_mode
            self.sentences = sentences
            pairs = self.pair_import_json(file_path)
            corelog.info("Imported")
        else:
            corelog.info("Input file is csv")
            pairs = self.pair_import(file_path)
            corelog.info("Imported")
        return pairs

    # csv
    def pair_import(self, csv_file_path) -> list[dict[str, list[str] | str | bool]]:

        pairs = list()

        if self.first_time:
            pairs.append(self.pair0)
            self.first_time = False
        else:
            pass

        current_pair_dict = dict()

        with open(csv_file_path, mode="r", encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            for row_number, row in enumerate(csv_reader, start=1):
                row = [x.strip() for x in row if x]  # removes empty slots and useless    whitespaces    .
                if row_number % 2 != 0:  # questions
                    current_pair_dict["question"] = row.copy()

                    for item in row:
                        result = re.search(self.tooltip_regex, item)
                        if result:
                            current_pair_dict["question tooltip"] = result.group(1)
                            current_pair_dict["question"].remove(item)

                else:  # answers
                    current_pair_dict["answer"] = row.copy()
                    for item in row:
                        result = re.search(self.tooltip_regex, item)
                        if result:
                            current_pair_dict["answer tooltip"] = result.group(1)
                            current_pair_dict["answer"].remove(item)

                        regex_match = re.search(self.regex_enabled_regex, item)
                        if regex_match:
                            if regex_match.group(1) in ["True", "true", "1", "Yes", "yes"]:
                                current_pair_dict["regex"] = True
                            elif regex_match.group(1) in ["False", "false", "0", "No", "no"]:
                                current_pair_dict["regex"] = False
                            current_pair_dict["answer"].remove(item)

                    pairs.append(current_pair_dict.copy())
                    current_pair_dict = dict()

        return pairs.copy()

    def pair_import_csv_alternative(self, csv_file_path) -> list[dict[str, list[str] | str | bool]]:

        pairs = list()
        if self.first_time:
            pairs.append(self.pair0)
            self.first_time = False
        else:
            pass

        with open(csv_file_path, mode="r", encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            for i, row in enumerate(csv_reader, start=1):
                row = [x.strip() for x in row if x]  # removes empty slots and useless    whitespaces    .
                # Row is like the following
                # question,answer,answerA,answerB

                question, *answers = row  # unpack
                regex: bool | None = None

                # check for regex flag
                for answer in answers:
                    match = re.search(self.tooltip_regex, answer)
                    if match:
                        regex = match.group(1)
                        answer.remove(answer)

                if regex:
                    pairs.append(
                        {
                            "question": [question],
                            "answer": answers,
                            "regex": regex
                        }
                    )
                else:
                    pairs.append(
                        {
                            "question": [question],
                            "answer": answers
                        }
                    )

        return pairs

    # json
    def pair_import_json(self, json_file_path) -> list[dict[str, list[str] | str | bool]]:
        corelog.info("Importing from json.")

        pairs = list()
        if self.first_time:
            pairs.append(self.pair0)
            self.first_time = False
        else:
            pass

        with open(json_file_path, mode="r", encoding="utf-8") as file:
            raw_pairs = json.loads(file.read())
            corelog.debug("File opened successfully.")
            for (key, content) in raw_pairs.items():  # goes through the keys' items
                corelog.debug(f'Going through key "{key}"')
                if self.default_json:
                    for i, pair in enumerate(content, start=1):  # goes through the keys' lists that should be dictionaries containing needed info
                        corelog.debug('Going through pair number "%s"', i)

                        ready_pair = {
                            "question": pair["question"].copy(),
                            "answer": pair["answer"].copy(),
                            "question tooltip": pair["question tooltip"] if "question tooltip" in pair else "",
                            "answer tooltip": pair["answer tooltip"] if "answer tooltip" in pair else "",
                        }
                        ready_pair.pop("question tooltip") if not ready_pair["question tooltip"] else None
                        ready_pair.pop("answer tooltip") if not ready_pair["answer tooltip"] else None

                        if "question tooltip" not in pair:
                            for item in pair["question"]:
                                result = re.search(self.tooltip_regex, item)
                                if result:
                                    ready_pair["question tooltip"] = result.group(1)
                                    ready_pair["question"].remove(item)

                        for item in pair["answer"]:
                            result = re.search(self.tooltip_regex, item)
                            if result:
                                ready_pair["answer tooltip"] = result.group(1)
                                ready_pair["answer"].remove(item)

                            regex_match = re.search(self.regex_enabled_regex, item)
                            if regex_match:
                                if regex_match.group(1) in ["True", "true", "1", "Yes", "yes"]:
                                    ready_pair["regex"] = True
                                elif regex_match.group(1) in ["False", "false", "0", "No", "no"]:
                                    ready_pair["regex"] = False
                                ready_pair["answer"].remove(item)

                        corelog.debug("Appending pair to list...")
                        pairs.append(ready_pair.copy())
                        corelog.debug("List has now %s item(s).", len(pairs))
                        corelog.debug("Pair contents: %s", pair)
                        if pairs[-1] != pair:
                            corelog.error("The pair wasn't added to the list correctly!")

                try:
                    # if this exists it's a jp file or if advanced is on
                    if "pronunciation" in content[0] and self.automatic or self.jp_mode:
                        corelog.debug("jp_mode is enabled.")
                        for i, jp_pair in enumerate(content, start=1):
                            jp_pair = dict(jp_pair)

                            corelog.debug('Going through pair number "%s"', i)

                            jp_pair["question"] = jp_pair["question"][:]  # Copy the list to avoid modifying the original
                            jp_pair["question"][0] = f"{jp_pair["question"][0]} pronunciation"
                            jp_pair["answer"] = jp_pair["pronunciation"][:]  # Copy the list

                            jp_pair.pop("question tooltip") if "question tooltip" in jp_pair else None
                            jp_pair.pop("answer tooltip") if "answer tooltip" in jp_pair else None

                            corelog.debug("Appending pair to list...")
                            pairs.append(jp_pair.copy())
                            corelog.debug("List has now %s item(s).", len(pairs))
                            corelog.debug("Pair contents: %s", jp_pair)
                            if pairs[-1] != jp_pair:
                                corelog.error("The pair wasn't added to the list correctly!")
                except IndexError:
                    corelog.critical("Index error while importing pairs!")

                if self.sentences:
                    corelog.debug("sentences are enabled")
                    for ii, pair in enumerate(content, start=1):
                        corelog.debug("Going through pair %s", ii)
                        for iii, sentence in enumerate(pair["sentences"], start=1):
                            corelog.debug("Going through sentence %s", iii)
                            new_pair = {
                                "question" : [sentence["sentence"]],
                                "answer" : [sentence["answer"]]
                            }
                            corelog.debug("Appending pair to list...")
                            pairs.append(new_pair.copy())
                            corelog.debug("List has now %s item(s).", len(pairs))

        corelog.debug("Returning the list")
        return pairs.copy()

    # nihongo quest
    def nq_import(self, csv_file_path, categories: list, pronunciation=False) -> list:
        pairs = list()

        pairs.append(self.pair0)

        with open(csv_file_path, mode="r") as file:
            csv_reader = csv.reader(file)
            for row_number, row in enumerate(csv_reader, start=1):
                if row[1] in categories:  # checks that the import is enabled

                    pairs.append(
                        {
                            "question" : [row[2]],
                            "answer" : row[3].split("; ")
                        }
                    )
                    if pronunciation:
                        if row[5] == "0":
                            # It's in kana so there's no point in having it
                            #answer_p = row[2]
                            pass
                        elif row[5] == "1":
                            # This category doesn't have pronunciations
                            pass
                        else:
                            pairs.append(
                                {
                                    "question" : [f"{row[2]} pronunciation"],
                                    "answer" : row[5].split("|")
                                }
                            )

        return pairs.copy()


def static_value_functions(user_input_subsetting, options, selected_setting) -> None:
    static_values = ["reset all time streak", "reset all time survival streak"]

    # other static value functions can be added here
    if selected_setting == static_values[0] and user_input_subsetting == True:
        options["all time streak"] = 0

    elif selected_setting == static_values[1] and user_input_subsetting == True:
        options["all time survival streak"] = 0

    get_options("dump", options)


def static_value_functions_gui():
    static_values = ["reset all time streak", "reset all time survival streak"]
    options = get_options()

    if options[static_values[0]]:
        settings_value_manipulator("all time streak", "dump", 0)

    if options[static_values[1]]:
        settings_value_manipulator("all time survival streak", "dump", 0)


def get_options(mode="load", settings_dict=None) -> dict[str, int | bool | dict[str, str | bool | int | list[str]] | list[list[str]]]:
    if settings_dict is None:
        settings_dict: dict[str, int | bool | dict[str, str | bool | int | list[str]] | list[list[str]]] = {}

    if mode == "load":
        with open(static_settings_path, "r") as file:  # Open in read mode
            settings_dict = json.load(file)  # Use json.load() to directly parse the file

            if "last game settings" not in settings_dict:
                settings_dict["last game settings"] = {
                    "pairs": ["example.csv"],
                    "reverse": False,
                    "current_question": 1,
                    "streak_current": 0,
                    "order": "Forward",
                    "mode": "Normal"
                }
            if "recent files" not in settings_dict:
                settings_dict["recent files"] = []
            if "big mode" not in settings_dict:
                settings_dict["big mode"] = False

    elif mode == "dump":
        with open(static_settings_path, "w") as file:  # Open in write mode
            json.dump(settings_dict, file, indent=4)  # Write the dictionary to the file

    else:
        raise Exception('available modes: "load", "dump"')
    return settings_dict


def never_repeat_random_list(min_pair_number, amount_of_pairs) -> list:
    if min_pair_number < 0:
        min_pair_number = 1
    number_list = list(range(min_pair_number, amount_of_pairs + 1))
    random.shuffle(number_list)
    return number_list


def settings_value_manipulator(option, mode="return", new_value: int | bool = 0) -> str | None | int:
    options = get_options()
    if mode in ["write", "dump"]:
        options[option] = new_value
        get_options("dump", options)
        return None
    elif mode == "return":
        return options[option]
    else:
        raise Exception("Incorrect mode")
