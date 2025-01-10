# SPDX-License-Identifier: GPL-2.0-or-later
import os
import core_functions as core

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

os.system("clear")
selected_mode = core.main_menu(modes=modes, version=version)
os.system("clear")

pairs = core.pair_import(csv_file_path=csv_path)
amount_of_pairs = len(pairs["questions"])

pairs["questions"].insert(0, ["Wait... question zero? What's the answer though..."])
pairs["answers"].insert(0, ["luupycards"])

import normal
normal.play(pairs, 1)


