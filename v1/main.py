import argparse
import os
import logging
from pathlib import Path

import core_functions as core
import gameplay_modules as gameplay

# Create parser
parser = argparse.ArgumentParser(description="Simple flip card program.")

# Add arguments
parser.add_argument("-i", type=str, required=False, help="Input csv file")
parser.add_argument("-j", type=str, required=False, help="Input json file (W.I.P.)")
parser.add_argument("-jp", type=bool, default=False, required=False, help="Use my jp importing with json")
parser.add_argument("-nq", "--nihongo-quest", type=str, required=False, help="Use an import method for Nihongo Quest's CSV format (REALLY EXPERIMENTAL)")
parser.add_argument("-debug", type=str, default="critical", required=False, help="Choose logging level (debug, info, error etc. critical is default)")

args = parser.parse_args()

# Create logging configuration
match args.debug:
    case "debug":
        log_level = logging.DEBUG
    case "info":
        log_level = logging.INFO
    case "error":
        log_level = logging.ERROR
    case "critical" | _:  # the wild card is so that it won't warn me.
        log_level = logging.CRITICAL

mainlog = logging.getLogger(__name__)
home_dir = Path.home()
log_path = os.path.join(home_dir, ".cache/luupycards", "luupy.log")
logging.basicConfig(filename=log_path, encoding="utf-8", level=log_level, filemode="w")

if os.name == "nt":
    mainlog.critical("Warning! This program is intended for Linux, using Windows WILL have unexpected behaviour!")

# make pair list
if args.i:
    pairs = core.pair_import(args.i)
elif args.j:
    pairs = core.pair_import_json(args.j, args.jp)
elif args.nihongo_quest:
    pairs = core.pair_import_nq(args.nihongo_quest)
else:
    pairs = []  # if no input method is specified

game_version = "v1.3"
modes = [
    ["Normal", "n"],                            #0
    ["Normal Random", "nr"],                    #1
    ["Normal Reverse order", "nro"],            #2
    ["Reverse", "r"],                           #3
    ["Reverse Random", "rr"],                   #4
    ["Reverse Reverse order", "rro"],           #5
    ["Multiple Choice", "m"],                   #6
    ["Multiple Choice Random", "mr"],           #7
    ["Multiple Choice Reverse Order", "mro"],   #8
    ["Survive!", "s!"],                         #9
    ["", ""],                                   #10
    ["Settings", "s"],                          #11
    ["Quit", "q"],                              #12
]

# Make a new main menu with these
main_modes = [
    ["Normal", "n"],
    ["Multiple Choice", "m"],
    ["Survive!", "s!"],
]
special_modes = [
    ["Settings", "s"],
    ["Quit", "q"]
]
sub_modes = [
    ["Random", "r"],
    ["Reverse", "re"],
    ["Reverse order", "ro"]
]
core.pass_pairs(pairs)
locked_settings_values = ["all time streak", "all time survival streak"]
static_settings_values = ["reset all time streak", "reset all time survival streak"]
playing = True
current_question = 1
shuffled_questions = [1, 2, 3]
core.settings_value_manipulator("max question", "dump", len(pairs) - 1)
max_question = core.settings_value_manipulator("max question")
# min_question = core.settings_value_manipulator("min question")  # Hmm, kinda bad thing, I'll just override for now
min_question = 1
core.settings_value_manipulator("min question", "dump", min_question)
show_current_question_number = core.settings_value_manipulator("show current question number")
current_streak = 0
all_time_streak = core.settings_value_manipulator("all time streak")
lives_left = core.settings_value_manipulator("lives")
all_time_streak_survival = core.settings_value_manipulator("all time survival streak")

# Initialize game variable
game = gameplay.Normal(pairs)

# New gameplay loop here
while not False:  # I know this is cursed
    # Main menu
    selected_mode = core.main_menu(modes=modes, version=game_version)

    game.clear()  # stupid way to clear
    print("Now playing:", modes[selected_mode][0]) if selected_mode < 10 else None

    # Matches the main mode. Aka. Normal, Reverse, Multiple Choice and Survive!
    # Then in a sub condition does the setting for the sub game mode.
    match selected_mode:
        case 0:  # Normals
            game = gameplay.Normal(pairs, streak_current=current_streak)

            current_streak = game.play()
        case 1:  # Normal random
            game = gameplay.Normal(pairs, streak_current=current_streak, order="random")

            current_streak = game.play()
        case 2:  # Normal reverse order
            game = gameplay.Normal(pairs, streak_current=current_streak, current_question=max_question, order="reverse")

            current_streak = game.play()
        case 3:  # Reverse
            game = gameplay.Reverse(pairs)
            game.streak_current = current_streak

            current_streak = game.play()
        case 4:  # Reverse random
            game = gameplay.Reverse(pairs, streak_current=current_streak, order="random")
            game.streak_current = current_streak

            current_streak = game.play()
        case 5:  # Reverse reverse order
            game = gameplay.Reverse(pairs, streak_current=current_streak, current_question=max_question, order="reverse")
            game.streak_current = current_streak

            current_streak = game.play()
        case 6:  # Multiple choice
            game = gameplay.MultipleChoice(pairs)
            game.streak_current = current_streak

            current_streak = game.play()
        case 7:  # Multiple choice random
            game = gameplay.MultipleChoice(pairs, streak_current=current_streak, order="random")
            game.streak_current = current_streak

            current_streak = game.play()
        case 8:  # Multiple choice reverse order
            game = gameplay.MultipleChoice(pairs, streak_current=current_streak, current_question=max_question, order="reverse")
            game.streak_current = current_streak

            current_streak = game.play()
        case 9:  # Survive!
            game = gameplay.Survive(pairs)
            game.streak_current = current_streak

            current_streak = game.play()
        case 10:  # The empty option
            raise Exception("Out of all the options, you had to choose the empty one... :/")
        case 11:  # Settings
            options = core.get_options(mode="load")
            core.settings_menu(options, locked_values=locked_settings_values, static_values=static_settings_values)

            # Reload needed options
            max_question = core.settings_value_manipulator("max question")
        case 12:  # Quit
            exit(0)
