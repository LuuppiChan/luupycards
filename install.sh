#!/bin/bash

# ensure these folders exist
mkdir -p $HOME/.cache/luupycards/
mkdir -p $HOME/.cache/luupycards/app/

echo "##############################"
echo "### DOWNLOADING REPOSITORY ###"
echo "##############################"

# download the repository
git clone https://github.com/LuuppiChan/luupycards.git $HOME/.cache/luupycards/app/

# go to that folder
cd $HOME/.cache/luupycards/app/

# Get the script directory (it should be the app folder)
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

sed "s|PATH/TO|$SCRIPT_DIR|m" template.desktop > luupycards.desktop

echo "######################"
echo "### INSTALLING APP ###"
echo "######################"

desktop-file-install --dir="$HOME/.local/share/applications" "luupycards.desktop"

rm luupycards.desktop

echo ""
echo "Installed, you can now open the app on your app menu."
