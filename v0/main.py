# SPDX-License-Identifier: GPL-2.0-or-later
import os
import argparse

import core_functions as core
import gameplay_modules as gameplay

# Create parser
parser = argparse.ArgumentParser(description="Simple flip card program.")

# Add arguments
parser.add_argument("-i", type=str, required=True, help="csv file location.")
args = parser.parse_args()

pairs = core.pair_import(args.i)

game_version = 0.2
modes = [
    ["normal", "n"],                    #0
    ["normal_random", "nr"],            #1
    ["reverse", "r"],                   #2
    ["reverse_random", "rr"],           #3
    ["multiple_choice", "mc"],          #4
    ["multiple_choice_random", "mcr"],  #5
    ["", ""],                           #6
    ["settings", "s"],                  #7
    ["quit", "q"],                      #8
]
locked_settings_values = ["all_time_streak"]
static_settings_values = ["reset_all_time_streak"]

while True:
    # setting up before gameplay loop
    print(os.path.exists("settings.json"))
    print(os.getcwd())
    selected_mode = core.main_menu(modes=modes, version=game_version)

    match selected_mode:
        case 0 | 1:
            pass
        case 2 | 3:
            pass
        case 4 | 5:
            pass
        case 7:
            options = core.get_options(mode="load")
            core.settings_menu(options, locked_values=locked_settings_values, static_values=static_settings_values)
        case 8:
            exit(0)

    # gameplay loop here

    while True:
        gameplay.normal(pairs)
