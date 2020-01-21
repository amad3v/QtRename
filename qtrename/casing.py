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

from random import choice

apply_case = {'same': lambda x: x,
              'upper': lambda x: x.upper(),
              'lower': lambda x: x.lower(),
              'sentence': lambda x: x[0].upper() + x[1:].lower(),
              'title': lambda x: x.title(),
              'invert': lambda x: x.swapcase(),
              'random': lambda x: random_case(x)}

cases = ('upper', 'lower')


def random_case(text):
    tmp = ''
    for i in range(len(text)):
        tmp += apply_case[choice(cases)](text[i])

    return tmp


def keep_if_upper(text):
    lst_chunks = text.split()

    for i, item in enumerate(text.split()):
        if item.isupper():
            lst_chunks[i] = ''

    return lst_chunks


def keep_if_mixed(text):
    lst_chunks = text.split()

    for i, item in enumerate(text.split()):
        if not item.isupper() and not item.islower():
            lst_chunks[i] = ''

    return lst_chunks


def set_case(text, keep, case):
    keep_case = {'upper': keep_if_upper,
                 'mixed': keep_if_mixed}
    lst = keep_case[keep](text)
    lst_text = text.split()

    for i, item in enumerate(lst):
        if item:
            lst_text[i] = case(item)

    return ' '.join(lst_text)
