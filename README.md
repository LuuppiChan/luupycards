# Luupycards
Flip card game written in Python

I was inspired to make this thanks to "[Nihongo Quest](https://store.steampowered.com/app/1556070/Nihongo_Quest/)".

# Why the name?
`Luup`: Part of my nickname Luuppi (which literally means "loop") and it kind of references to the gameplay where you can play the cards on a loop.

`y`: I added it since it's written in Python and sounds better than "Luupcards"

`cards`: This is a flip **CARD** game

#### Pronunciation:
`Luupy` like "loopy", the other part is self-explanatory

## Features
#### Modes
- Normal
- Reverse (Questions are answers)
- Multiple choice
- Survive (You have only `n` amount of lives)
#### Question orders
- Forward
- Backward
- Random
#### Settings
- Reset all time streaks
- Min and max question for random (You can change, but they are automatically set)
- Show question number
- Max multiple choice options
- Lives for Survive!
- Fuzzy select percentage (Requires you to have the fuzzywuzzy module)
#### I'll note more things here later.
- FOSS

# Usage (Note that this has been copied and fitted from lfg!)
If you have any issues understanding how to use this application please make an issue.
THERE ARE VIDEO EXAMPLES OF SOME THINGS. Although some knowledge is highly recommended.
## Installation (V1)
- Video of installation process will be available later.
- This is a Linux-only application for now!

Clone this repository with the following command.
```bash
git clone https://github.com/LuuppiZ/luupycards
```
You can make a launch script for easier usage, here's an example launch script, I'll call it `luupycards` since that's how I want to call it from the terminal:
```bash
#!/bin/bash
. "/path/to/luupycards/luupycards" "$@"
```
- Replace `/path/to/luupycards/v1/main.py` with the actual path to main.py
- This will launch the launch script in the repository. The launch script automatically enables the Python virtual environment for you. 

Make the script executable:
```bash
chmod a+x /path/to/luupycards
```
Move it to a local binary folder. In this example we use ~/.local/bin/ but you can use any other too. 
(Make sure to put the real path to `luupycards`)
(Make sure that this folder is set to binary path. If you don't know how just Google it. "How to set ~/.local/bin/ as binary path" or something like that)
```bash
mv /path/to/luupycards ~/.local/bin/luupycards
```
To check that it works open up a new terminal and type `luupycards -h` it should open the help. If not it's likely that the folder you put it is not a binary folder. Do the "Move it to a local binary folder" step again.

## Import question/answer pairs
Nothing is capital sensitive! The answer and user input is converted to lowercase when they are compared.

You need to use the example file or make one yourself. To make one yourself you can use LibreOffice Calc for example.
[Video example of doing that (legacy)](https://youtu.be/zH3Lg1INpUI) this is basically identical.
### Some things you need to know before making a file
- Un-even rows are questions
- Even rows are answers
- For example put a question in cell A1 and the answer on A2. If you have multiple options for the answer put them to B2, C2 etc. there should be no max question/answer limit.
See the example.csv on every release that supports it.
- Check the examples/ directory for examples!

How I suggest the pairs to be made (example):
```
How long is the road?,,
two hundred meters,200 meters,200m
```
Here the first answer has every sing answer in one string. This is so that when you want to see the correct answer the application will show the first cell's answer only. This might be changed in a future version but I'll rewrite this if it happens.
## Importing
Please refer to `luupycards -h`
Anyways here are the simple instructions:
`luupycards -i [csv file]` put the path to the \[csv file\]

## "Gameplay" if you can call it such
- Type the correct answer
- If an answer is the same as one of these they don't work. For example in multiple choice if the correct answer is `c` it will not say the correct answer, it will say that you chose the correct option.
- `c` or `correct` for the correct answer.
- `q` or `quit` for going back to main menu.
- `seek [sumber]` for seeking to that question. Put a space between seek and the number!
- In multiple choice you can type the answer or the letter. If you type `c` it either tells the correct answer or says it's correct if it's correct lol.

# Uninstalling
Just remove the folder where the game is.
There's also a settings file located at `~/.cache/luupycards/settings.json`
You can remove it by running this command
```bash
rm -r ~/.cache/luupycards/
```
It also removes the folder. You can remove the launch script from `bin/` if you made one.

## Settings
There are minimal checks for if a setting value is valid!
Invalid values may break the game!
