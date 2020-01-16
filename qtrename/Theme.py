 ############################################################################
##############################################################################
##   Feature-rich app to rename files for GNU/Linux and Windows             ##
##   Copyright (C) 2020  Mohamed Jouini                                     ##
##                                                                          ##
##   This program is free software: you can redistribute it and/or modify   ##
##   it under the terms of the GNU General Public License as published by   ##
##   the Free Software Foundation, either version 3 of the License, or      ##
##   (at your option) any later version.                                    ##
##                                                                          ##
##   This program is distributed in the hope that it will be useful,        ##
##   but WITHOUT ANY WARRANTY; without even the implied warranty of         ##
##   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          ##
##   GNU General Public License for more details.                           ##
##                                                                          ##
##   You should have received a copy of the GNU General Public License      ##
##   along with this program.  If not, see <https://www.gnu.org/licenses/>. ##
##############################################################################
 ############################################################################

import json
from pathlib import Path


class Theme:
    def __init__(self, config_folder):
        self.__theme_dir = Path(Path.home().joinpath(config_folder))
        self.__theme_file = Path(self.__theme_dir.joinpath('theme'))

        self.__theme = {}
        self.__is_theme_dir()
        self.__load_theme()

    def __is_theme_dir(self):
        if not self.__theme_dir.is_dir():
            self.__theme_dir.mkdir(parents=True, exist_ok=True)

    def __load_theme(self):
        theme_file = f'{str(self.__theme_file)}'

        try:
            with open(theme_file, 'r') as db:
                self.__theme = json.load(db)
        except:
            self.__theme = {'theme': 'default', 'tone': 'default'}

    def __save_theme(self):
        with open(str(self.__theme_file), 'w') as db:
            json.dump(self.__theme, db)

    def save_theme(self, theme, tone):
        self.__theme['theme'] = theme
        self.__theme['tone'] = tone
        self.__save_theme()

    @property
    def get_theme(self):
        return self.__theme['theme'], self.__theme['tone']
