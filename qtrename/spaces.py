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

import re

from qtrename.common import rectified_pattern, escape_metachars


def set_list(text):
    lst = []
    for char in text.replace(' ', ''):
        lst.append(char)

    return list(set(lst))


def maintain_space(text, is_before, before, is_after, after):
    before_list = set_list(before)
    after_list = set_list(after)
    tmp = text

    if is_before:
        for c in before_list:
            p = re.compile(fr"(?<! ){escape_metachars(c)}")
            tmp = p.sub(fr' {c}', tmp)

    if is_after:
        for c in after_list:
            p = re.compile(fr"{escape_metachars(c)}(?! )")
            tmp = p.sub(fr'{c} ', tmp)

    return tmp


def replace_chars(text, pattern, is_with_space):
    if not pattern: return ''

    rectified = rectified_pattern(pattern)

    try:
        re.compile(fr'{rectified}')
    except:
        return ''
    return re.sub(rf"{rectified}+", ' ', text) if is_with_space else text.replace(pattern, ' ')


def g_replace_spaces(text, leading, trailing, many_one, is_before, before, is_after, after, is_x_chars, is_one_char,
                     x_chars, one_char):
    tmp = text
    if is_x_chars: tmp = replace_chars(tmp, x_chars, False)
    if is_one_char: tmp = replace_chars(tmp, one_char, True)
    if leading: tmp = tmp.lstrip(' ')
    if trailing: tmp = tmp.rstrip(' ')
    if many_one: tmp = replace_chars(tmp, ' ', True)
    tmp = maintain_space(tmp, is_before, before, is_after, after)

    return '' if tmp == text else tmp
