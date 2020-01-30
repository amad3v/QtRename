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
from qtrename.common import has_dot
from qtrename.preview import get_name_part, set_name_part


def delete_chars_backwards(text, index, number):
    if len(text) <= index:
        return ''
    else:
        lst = list(text)
        lst.reverse()
        for i in range(number):
            if index >= len(lst):
                break
            lst.pop(index)

        lst.reverse()

        return ''.join(lst)


def delete_chars(text, index, number):
    tmp = text[index:index + number]
    return text[0:index] + text[index:].replace(tmp, '', 1)


def insert_chars_global(text, index, to_insert, is_backward, is_overwrite):
    tmp = text
    if index > len(text):
        tmp = ''
    elif index == len(tmp) and not is_backward:
        tmp += to_insert
    else:
        if is_backward:
            tmp = insert_backwards(text, index, to_insert, is_overwrite)
        else:
            tmp = insert_chars(text, index, to_insert, is_overwrite)

    return tmp


def insert_chars(text, index, to_insert, is_overwrite):
    tmp = text

    if is_overwrite:
        lst = list(tmp)

        for i in range(len(to_insert)):
            lst_index = i + index
            if lst_index >= len(lst):
                lst.append(to_insert[i])
            else:
                lst[lst_index] = to_insert[i]
        tmp = ''.join(lst)
    else:
        lst = list(tmp)
        lst.insert(index, to_insert)
        tmp = ''.join(lst)

    return tmp


def insert_backwards(text, index, to_insert, is_overwrite):
    pos = -(index + 1)
    tmp = text
    lst = list(tmp)

    if pos == -1:
        lst.append(to_insert)
        tmp = ''.join(lst)
    else:
        if is_overwrite:
            pos = -index
            for i in range(len(to_insert)):
                lst.pop(pos + i)
            lst.insert(pos + len(to_insert), to_insert)
            tmp = ''.join(lst)
        else:
            lst.insert(pos, to_insert)
            tmp = ''.join(lst)
    return tmp


def add_remove_chars(text, fargs, is_dir):
    args = fargs[0]
    tmp = get_name_part(text, args['to_process'], has_dot(text, is_dir))

    if not tmp: return ''

    if args['del_chars'] or args['both_ops']:
        if args['backw_del']:
            tmp = delete_chars_backwards(tmp, args['delete_at'], args['delete'])
        else:
            tmp = delete_chars(tmp, args['delete_at'], args['delete'])

    if not args['del_chars'] or args['both_ops']:
        tmp = insert_chars_global(tmp, args['add_num'], args['insert'],
                                  args['backw_add'], args['overwrite'])

    tmp = set_name_part(tmp, text, args['to_process'], has_dot(text, is_dir))

    if tmp == text: return ''

    return tmp
