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
- Fuzzy select percentage (Requires you to have the thefuzz module)
#### I'll note more things here later.
- FOSS

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
The game is kind of useless without pairs to play with.

This section will be done later.

## Settings
There are minimal checks for if a setting value is valid!
Invalid values may break the game!
