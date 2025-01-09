# SPDX-License-Identifier: GPL-2.0-or-later
import os
import core_functions as core
import gameplay_modules as gameplay

# use parameters to import the csv path
csv_path = "/home/luuppi/Documents/coding/practice games/jp/new/items.csv"

# modes will be imported from elsewhere later
modes = [
    "normal",
    "reverse",
    "random",
    "random reverse",
    "multiple choice",
    "random multiple choice",
]
memory = core.open_memory("memory.json")
version = memory["version"]
all_time_max_streak = memory["all_time_streak"]

selected_mode = core.main_menu(modes=modes, version=version)
os.system('clear')

questions, answers = core.pair_import(csv_file_path=csv_path)
amount_of_pairs = len(questions)
gameplay.never_repeat_random(amount_of_pairs=amount_of_pairs) # Maybe import later?
questions.insert(0, "Wait... question zero? What's the answer though...")
answers.insert(0, "luupycards")
print(questions)


