# Luupycards
Flip card game written in Python

I was inspired to make this thanks to "[Nihongo Quest](https://nihongoquest.com/)".

# Why the name?
`Luup`: Part of my nickname Luuppi (which literally means "loop") and it kind of references to the gameplay where you can play the cards on a loop.

`y`: I added it since it's written in Python and sounds better than "Luupcards"

`cards`: This is a flip **CARD** game

#### Pronunciation:
`Luupy` like "loopy", the other part is self-explanatory

## Features
#### Modes
- Normal
- Multiple choice
- Survive! (You have only `n` amount of lives)
- Option to flip questions and answers
#### Question orders
- Forward
- Backward
- Random
#### Settings
- Min and max question for random (You can change, but they are automatically set when pressed play)
- Show question number
- Max multiple choice options (Choose how many multiple choice options you want)
- Lives for Survive!
- Fuzzy select percentage (Requires you to have the `thefuzz` module)
#### I'll note more things here later.
- FOSS (Well MIT, but still)
- Drag and drop pair files to load or open them with File -> Open or Open (Advanced)
- Inspector
  - Inspect your pairs in game or even make new ones and delete old ones. (If this app gets attraction I might add more editor functionality)
  - Save to memory instantly reloads them in game
  - Save to file opens a file dialog to save them into a pair file
- All documentation is in the game under Help -> Help!

# Installation V2 (Linux)

This is a graphical version of the application. You can find the instructions to the old tui version in `v1/installation.md` As far as I know this should also work on Windows, but it hasn't been tested.

1. Install Python if you haven't (duh)
2. Download this repository with
```bash
git clone https://github.com/LuuppiChan/luupycards.git
```
3. Go to the folder
```bash
cd luupycards
```
4. Install dependencies with pip
```bash
pip install -r requirements.txt
```
5. Use the installation script to get the desktop shortcut
```bash
chmod a+x install.sh
./install.sh
```
6. Open the app from your application menu.

# Making pair files
The documentation on everything about the game is in the game. 

From the top bar, go to Help -> Help! to see the documentation.

But in short this is an example pair file:
```csv
What is the capital of Japan?
Tokyo
What is the tallest mountain in the world?
Mount Everest,Everest
What is 5 + 3?
8
What is the currency of the United States?
Dollar,US Dollar,USD
```
As you can see, it follows a format where uneven lines are questions and even lines are answers.

## Settings
There are minimal checks for if a setting value is valid!
Invalid values may break the game!
