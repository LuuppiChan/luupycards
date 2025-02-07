# SPDX-License-Identifier: GPL-2.0-or-later
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

game_version = "v1.1"
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

    match selected_mode:
        case 0:  # Normal
            game = gameplay.Normal(pairs, current_question=max_question, streak_current=current_streak, order="reverse")

            current_streak = game.play()
        case 1:  # Normal random
            game = gameplay.Normal(pairs, streak_current=current_streak, order="random")

            current_streak = game.play()
        case 2:  # Normal reverse order
            game = gameplay.Normal(pairs)
            game.order = "reverse"
            game.streak_current = current_streak

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
            game = gameplay.Reverse(pairs, current_question=max_question, streak_current=current_streak, order="reverse")
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

# LEGACY LOOP!
raise Exception("You broke out of the main loop, somehow...")
# setting up before gameplay loop
while True:
    selected_mode = core.main_menu(modes=modes, version=game_version)

    match selected_mode:
        case 0 | 3 | 6:
            current_question = 1
            playing = True
        case 2 | 5 | 8:
            current_question = len(pairs) - 1
            playing = True
        case 1 | 4 | 7 | 9: # randoms
            shuffled_questions = core.never_repeat_random_list(min_question, max_question)
            current_question = 0
            lives_left = core.settings_value_manipulator("lives")
            playing = True
            if selected_mode == 9:
                current_streak = 0
        case 11:
            options = core.get_options(mode="load")
            core.settings_menu(options, locked_values=locked_settings_values, static_values=static_settings_values)

            # Reload options
            all_time_streak = core.settings_value_manipulator("all time streak")
            all_time_streak_survival = core.settings_value_manipulator("all time survival streak")
            min_question = core.settings_value_manipulator("min question")
            max_question = core.settings_value_manipulator("max question")
            show_current_question_number = core.settings_value_manipulator("show current question number")
            lives_left = core.settings_value_manipulator("lives")
            
            playing = False
        case 12:
            exit(0)
        case 10:
            raise Exception("Out of all the options, you had to choose the empty one... :/")

    all_time_streak = core.settings_value_manipulator("all time streak")
    all_time_streak_survival = core.settings_value_manipulator("all time survival streak")
    os.system("clear")
    print(f"Now playing {modes[selected_mode][0]} mode")

    # gameplay loop here
    while playing:
        # gamemodes
        if selected_mode in [0, 1, 2, 9]: # normal + survive
            if selected_mode == 1:
                playing, current_question, current_streak, seeking = gameplay.normal(pairs, shuffled_questions[current_question], current_question_number_enabled=show_current_question_number, streak_current=current_streak, streak_all_time=all_time_streak)
            elif selected_mode == 9:
                playing, current_question, current_streak, seeking, lives_left = gameplay.survive(pairs, shuffled_questions[current_question], current_question_number_enabled=show_current_question_number, streak_current=current_streak, streak_all_time=all_time_streak_survival, lives=lives_left)
            else:
                playing, current_question, current_streak, seeking = gameplay.normal(pairs, current_question, current_question_number_enabled=show_current_question_number, streak_current=current_streak, streak_all_time=all_time_streak)

        elif selected_mode in [3, 4, 5]: # reverse
            if selected_mode == 4:
                playing, current_question, current_streak, seeking = gameplay.reverse(pairs, shuffled_questions[current_question], current_question_number_enabled=show_current_question_number, streak_current=current_streak, streak_all_time=all_time_streak)
            else:
                playing, current_question, current_streak, seeking = gameplay.reverse(pairs, current_question, current_question_number_enabled=show_current_question_number, streak_current=current_streak, streak_all_time=all_time_streak)

        elif selected_mode in [6, 7, 8]: # multiple choice
            if selected_mode == 7:
                playing, current_question, current_streak, seeking = gameplay.multiple_choice(pairs, shuffled_questions[current_question], current_question_number_enabled=show_current_question_number, streak_current=current_streak, streak_all_time=all_time_streak)
            else:
                playing, current_question, current_streak, seeking = gameplay.multiple_choice(pairs, current_question, current_question_number_enabled=show_current_question_number, streak_current=current_streak, streak_all_time=all_time_streak)

        else:
            raise Exception("gamemode isn't in gameplay modules, I'm honestly surprised this error appeared.")

        # next question for modes
        if not seeking:
            if selected_mode in [0, 3, 6]: # plus one
                if current_question == max_question:
                    current_question = 1
                else:
                    current_question = gameplay.next_question_plus_one(current_question)
            elif selected_mode in [2, 5, 8]: # minus one
                if current_question < 0:
                    current_question = max_question
                else:
                    current_question = gameplay.next_question_minus_one(current_question)
            elif selected_mode in [1, 4, 7, 9]: # random + survive
                if current_question >= max_question:
                    current_question = 0
                    shuffled_questions = core.never_repeat_random_list(min_question, max_question)
                else:
                    current_question = gameplay.next_question_plus_one(current_question)
            else:
                raise Exception("gamemode isn't in next_questions, I'm honestly surprised this error appeared.")

        elif seeking and selected_mode in [1, 4, 7, 9]: # random + survive seeking
            try:
                current_question = shuffled_questions.index(current_question)
                print(f"Seeking to {current_question}")
            except ValueError:
                print(f"{current_question} is an invalid seek number")
                current_question = shuffled_questions.index(1)

        elif seeking: # seeking normal
            try:
                pairs[current_question] # this is for checking if it's a valid index
                print(f"Seeking to {current_question}")
            except IndexError:
                print(f"{current_question} is an invalid seek number")
                current_question = 1

        if selected_mode == 9 and current_streak > all_time_streak_survival:
            core.settings_value_manipulator("all time survival streak", "write", current_streak)

        elif current_streak > all_time_streak:
            core.settings_value_manipulator("all time streak", "write", current_streak)

        all_time_streak = core.settings_value_manipulator("all time streak")
        all_time_streak_survival = core.settings_value_manipulator("all time survival streak")

        if lives_left == 0:
            print("Game over!")
            time.sleep(5)
            lives_left = core.settings_value_manipulator("lives")
            streak_current = gameplay.streak_functions(mode="break")
            playing = False
