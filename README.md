


# QtRename
![QtRename Logo](https://github.com/amad3v/QtRename/raw/master/qtrename/app.png)

feature-rich app to rename files for GNU/Linux and Windows

- [Installation](#installation)
- [Description](#description)
- [License](#license)
- [Features](#features)
- [Report a bug - Request feature](#report-a-bug---request-feature)
- [Screenshots](#screenshots)
- [Changelog](#changelog)

## **Installation**
### Linux:
    pip install qtrename

To avoid running the app from the command line, you need to add it to your apps menu:
- Download this [script](https://github.com/amad3v/QtRename/raw/master/setup.sh)
- Open the terminal and `cd` to the location of `setup.sh`
- run: `chmod u+x setup.sh`
- run: `./setup.sh`

Head to your apps menu, type qtfind or you can find it under Accessories.

### Windows:
- Download the installer from [here](https://github.com/amad3v/QtRename/releases/download/v1.0.0/QtRename.v1.0.0.exe) [Require [Microsoft Visual C++ 2015 Redistributable](https://www.microsoft.com/en-gb/download/details.aspx?id=48145)]

## **Description**

:heavy_check_mark: **QtRename** is a graphical interface for bulk renaming.

:heavy_check_mark: **QtRename** easy to use.

:heavy_check_mark: **QtRename** is for for Linux and Windows.

:heavy_check_mark: **QtRename** is made with PyQt5


## **License**
This program comes with absolutely no warranty.
See the [GNU General Public Licence](https://www.gnu.org/licenses/gpl-3.0.html), version 3 or later for details.

## **Features**
 - **Find and Replace:**
   * Skip the first *N* occurrences
   * Replace max *N* occurrences
   * Case sensitive
   * Swap chunks of characters
   * find occurrences using RegEx
 - **Casing:**
   * Change case file, extension or both (upper, lower, sentence, title, invert, random)
   * Ignore upper and/or mixed case
 - **Add/Remove**
   * Insert/Overwrite/Remove characters at a specific position (backwards option available)
   * Combine Insert/Overwrite/Remove
 - **Move** characters from onne position to another (absolute/relative position, backwards,)
 - **Spaces:**
   * Remove leading/trailing/multiple spaces
   * Keep a space before/after a set of characters
   * Replace specific character with a spaces
   * Replace a consecutive set of a specific characters with 1 space
 - **Counter:**
   * Insert numbers at the begining/end of the filename
   * Replace the filename with a unified name
   * Set a seperator between counter and filename
 - **Enumerate:**
   * Start counter from a specific numbers
   * Counter step
   * Set a separator
   * Zero padding
 - **Extra:**
   * Realtime preview
   * Selective preview
   * Rename filename, extension or both
   * Navigate directories (folders): from the list, open dialog, type in completer
   * filter by extension
   * Rename files / directories (folders) / subdirectories (sub-folders)
   * Themes: default and dark (4 tones: blue, green, orange and pink)
   * Undo renaming (only last one)
   * Errors Log
   
## **Report a bug - Request feature**
[https://github.com/amad3v/QtRename/issues](https://github.com/amad3v/QtRename/issues)

## **Screenshots**

*Dark theme (Linux):*

![dark theme linux](https://github.com/amad3v/QtRename/raw/master/docs/linux.png)

*Default theme (Windows):*

![default theme windows](https://github.com/amad3v/QtRename/raw/master/docs/win.png)

|Screenshots|Screenshots|
|---|---|
|![casing](https://github.com/amad3v/QtRename/raw/master/docs/casing.png)|![add/remove](https://github.com/amad3v/QtRename/raw/master/docs/addrem.png)|
|![move](https://github.com/amad3v/QtRename/raw/master/docs/move.png)|![spaces](https://github.com/amad3v/QtRename/raw/master/docs/spaces.png)|
|![counter](https://github.com/amad3v/QtRename/raw/master/docs/counter.png)|![enumerate](https://github.com/amad3v/QtRename/raw/master/docs/enum.png)|
## **Changelog**
- **1.1.0:**
	- Fixed MVC bugs
	- Fixed folders/Files opened incrementally
	- Adjusted GUI for low resolution screens
	- Added french translation
	- Minor improvements
- **1.0.0:**
	- Initial release


Copyright :copyright: 2020 - amad3v
