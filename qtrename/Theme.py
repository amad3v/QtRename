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
from qtrename.common import path_func


class Settings:
    def __init__(self, config_folder):
        self.__settings_dir = path_func(path_func.home().joinpath(config_folder))
        self.__settings_file = path_func(self.__settings_dir.joinpath('settings'))

        self.__settings = {}
        self.__is_settings_dir()
        self.__load_settings()

    def __is_settings_dir(self):
        if not self.__settings_dir.is_dir():
            self.__settings_dir.mkdir(parents=True, exist_ok=True)

    def __load_settings(self):
        settings_file = f'{str(self.__settings_file)}'

        try:
            with open(settings_file, 'r') as db:
                self.__settings = json.load(db)
        except:
            self.__settings = {'theme': 'default', 'tone': 'default', 'lang': 'en'}

    def __save_settings(self):
        with open(str(self.__settings_file), 'w') as db:
            json.dump(self.__settings, db)

    def save_theme(self, theme, tone):
        self.__settings['theme'] = theme
        self.__settings['tone'] = tone
        self.__save_settings()

    def save_lang(self, lang):
        self.__settings['lang'] = lang
        self.__save_settings()

    @property
    def get_theme(self):
        return self.__settings['theme'], self.__settings['tone']

    @property
    def get_language(self):
        return self.__settings['lang']
