#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

sed "s|PATH/TO|$SCRIPT_DIR|m" template.desktop > luupycards.desktop

desktop-file-install --dir=$HOME/.local/share/applications luupycards.desktop

rm luupycards.desktop

echo "Installed, you can now open the app on your app menu."
