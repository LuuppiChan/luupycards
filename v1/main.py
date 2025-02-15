import argparse

import core_functions as core
import gameplay_modules as gameplay

# Create parser
parser = argparse.ArgumentParser(description="Simple flip card program.")

# Add arguments
parser.add_argument("-i", type=str, required=True, help="input csv file")
args = parser.parse_args()

# make pair list
pairs = core.pair_import(args.i)

game_version = "v1.2"
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

locked_settings_values = ["all time streak", "all time survival streak"]
static_settings_values = ["reset all time streak", "reset all time survival streak"]
playing = True
current_question = 1
shuffled_questions = [1, 2, 3]
core.settings_value_manipulator("max question", "dump", len(pairs) - 1)
max_question = core.settings_value_manipulator("max question")
min_question = core.settings_value_manipulator("min question")
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
