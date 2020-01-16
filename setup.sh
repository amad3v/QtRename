#!/bin/sh

# make sure required directories exist
mkdir $HOME/.local/share/applications 2> /dev/null
mkdir $HOME/.local/share/icons 2> /dev/null

# write desktop file
printf "[Desktop Entry]\nName=QtRename Bulk Rename\nGenericName=Bulk Rename\nComment=Rename files/directories\nKeywords=files;rename;explorer;\nCategories=Qt;Utility;\nExec=%s %s\nIcon=%s/.local/share/icons/qtrename.png\nTerminal=false\nType=Application\nMimeType=inode/directory;\n" $(which qtrename) "%f" $HOME > $HOME/.local/share/applications/QtRename.desktop

# app icon in base64 format
ICON="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"

# decode and save the app's icon
echo -n $ICON | base64 -d > $HOME/.local/share/icons/qtrename.png

# done
echo "done!"
