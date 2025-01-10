import os

import gameplay_modules as gameplay

def play(pairs, current_question):
    loop = ""
    print("Now playing normal mode.")
    while loop != "q":
        gameplay.print_question(pairs["questions"][current_question][0])
        user_input = gameplay.user_input()
        os.system("clear")
        check = gameplay.answer_check(user_input=user_input, correct_answers=pairs["answers"][current_question])
        if type(check) == int:
            current_question = check
        elif check == "correct":
            current_question = gameplay.next_question_plus_one(current_question)
        elif check == "wrong":
            pass
        elif check == "q" or "quit":
            loop = "q"

