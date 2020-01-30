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
from enum import IntFlag

from qtrename.common import os_type, rectified_pattern


class CaseSensitivity(IntFlag):
    IGNORECASE = re.IGNORECASE
    CASE = 0


def find_occurrences(text, to_find, skip, max_rpl, c_sensitive):
    lst = []
    tmp_find = rectified_pattern(to_find)

    try:
        pattern = re.compile(tmp_find, c_sensitive)
    except re.error:
        return lst

    matches = pattern.finditer(text)

    for match in matches:
        lst.append((match.start(), match.end()))

    if skip >= len(lst):
        return []

    if skip > 0:
        lst = lst[skip:]

    if 0 < max_rpl < len(lst):
        lst = lst[:max_rpl]

    return lst


def insensitive_replace(text, replace_with, positions):
    tmp = text[0:positions[0][0]]

    for i, item in enumerate(positions[:-1]):
        tmp += replace_with + text[item[1]:positions[i + 1][0]]

    tmp += replace_with + text[positions[-1][1]:]

    return tmp


def validate_replacement(text):
    special_chars = '/'
    if os_type == 'Windows':
        special_chars = '\\/:*?"<>|'

    for c in text:
        if c in special_chars:
            return True
    return False


def list_from_pos(text, positions):
    lst = []

    start = text[0:positions[0][0]]
    if start:
        lst.append(start)
        lst.append('')
    else:
        lst.append('')

    for i, item in enumerate(positions[:-1]):
        next_start = positions[i + 1][0]
        lst.append(text[item[1]:next_start])
        lst.append('')

    end = text[positions[-1][1]:]

    if end:
        lst.append(end)

    return lst


def remove_overlaps(source_list, target_list):
    tmp_lst = []
    for item in source_list:
        source_set = set(range(item[0], item[1]))
        for i, target in enumerate(target_list):
            target_set = set(range(target[0], target[1]))
            if source_set.intersection(target_set):
                tmp_lst.append(i)

    for i in tmp_lst:
        target_list.pop(i)


def find_replace(text, to_find, replace_with, skip, max_rpl, c_sensitive):
    tmp = ''

    if not to_find or validate_replacement(replace_with):
        return ''

    positions = find_occurrences(text, to_find, skip, max_rpl, c_sensitive)
    if not positions:
        return tmp

    first_occ = positions[0][0]

    if c_sensitive == re.IGNORECASE:
        tmp = replace_regex(text, to_find, replace_with, skip, max_rpl, c_sensitive, False)
    else:
        if not max_rpl:
            tmp = text[first_occ:].replace(to_find, replace_with)
            tmp = text[:first_occ] + tmp
        else:
            tmp = text[first_occ:].replace(to_find, replace_with, max_rpl)
            tmp = text[:first_occ] + tmp

    return '' if tmp == text else tmp


def swap_strings(text, to_find, swap_with, skip, max_rpl, c_sensitive):
    if not swap_with:
        return find_replace(text, to_find, swap_with, skip, max_rpl, c_sensitive)

    if not to_find or validate_replacement(swap_with):
        return ''

    pos_swap_with = find_occurrences(text, swap_with, skip, max_rpl, c_sensitive)

    if not pos_swap_with:
        return find_replace(text, to_find, swap_with, skip, max_rpl, c_sensitive)

    pos_to_find = find_occurrences(text, to_find, skip, max_rpl, c_sensitive)

    if not pos_to_find:
        return ''

    remove_overlaps(pos_to_find, pos_swap_with)

    if not pos_swap_with:
        return find_replace(text, to_find, swap_with, skip, max_rpl, c_sensitive)

    lst_find = find_occurrences(text, to_find, skip, max_rpl, c_sensitive)
    lst_find = list_from_pos(text, lst_find)
    tmp_swap = ''

    for i, item in enumerate(lst_find):
        if not item:
            lst_find[i] = swap_with
        else:
            tmp_swap += item + '/'

    tmp_swap = find_replace(tmp_swap, swap_with, to_find, skip, max_rpl, c_sensitive)
    lst_swap = tmp_swap.split('/')
    swap_counter = 0

    for i, item in enumerate(lst_find):
        if item != swap_with:
            lst_find[i] = lst_swap[swap_counter]
            swap_counter += 1

    return ''.join(lst_find)


def replace_regex(subject, to_replace, replace_with, skip, max_occ, case_sensitive, is_regex):
    if not to_replace:
        return ''

    rectified = to_replace
    if not is_regex:
        rectified = rectified_pattern(to_replace)

    pattern = re.compile(rectified, case_sensitive)
    matches = pattern.finditer(subject)
    result = ''

    if skip:
        for matchNum, match in enumerate(matches):
            if matchNum >= skip:
                result = subject[:match.start()] + pattern.sub(replace_with, subject[match.start():], max_occ)
                break
    else:
        result = pattern.sub(replace_with, subject, max_occ)

    if result == subject:
        return ''

    return result


def g_replace_general(text, to_find, replace_swap, skip, max_rpl, is_swap, c_sensitive, is_regex):
    if is_swap: return swap_strings(text, to_find, replace_swap, skip, max_rpl, c_sensitive)
    if is_regex: return replace_regex(text, to_find, replace_swap, skip, max_rpl, c_sensitive, True)
    return find_replace(text, to_find, replace_swap, skip, max_rpl, c_sensitive)
