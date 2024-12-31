# SPDX-License-Identifier: GPL-2.0-or-later

# Temporary variables to test functionality, they will be imported from somewhere else later.
modes = [
    "normal",
    "reverse",
    "random",
    "random reverse",
    "multiple choice",
    "random multiple choice",
]
version = "v0.1"
selected_mode = ""
selected_input = ""

while True:
    print(f"Welcome to Luupycards! {version}")
    for i, mode in enumerate(modes, start=1): # Prints all modes and their numbers
        print(f"{i} for {mode}")
    selected_input = input("Type number or the full name: ")
    if selected_input.isdigit():
        selected_input = int(selected_input)
        if 0 <= selected_input -1 < len(modes): # Checks if input is correct
            selected_mode = selected_input - 1
            break
    elif selected_input in modes: # If user input is alphabetical
        selected_mode = modes.index(selected_input) # Finds the specific mode
        break
    print(f"Invalid selection \"{selected_input}\", please try again.")
print(selected_mode)
