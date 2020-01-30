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

from qtrename.casing import set_case, apply_case
from qtrename.common import ProcessName, path_func, has_dot
from qtrename.counters import g_preview_counter, g_preview_renumber
from qtrename.move import g_move_general
from qtrename.replace import g_replace_general
from qtrename.spaces import g_replace_spaces


def get_name_part(text, flag, has_dot):
    if not has_dot:
        return text

    if flag == ProcessName.FILENAME:
        return str(path_func(text).stem)

    if flag == ProcessName.EXTENSION:
        return str(path_func(text).suffix)[1:] if has_dot else str(path_func(text).suffix)

    if flag == ProcessName.FULLNAME:
        return text

    return ''


def set_name_part(mod_text, text, flag, has_dot):
    if not has_dot:
        return mod_text

    if not mod_text: return ''

    if flag == ProcessName.FILENAME:
        return f'{mod_text}{str(path_func(text).suffix)}'

    if flag == ProcessName.EXTENSION:
        return f'{str(path_func(text).stem)}.{mod_text}' if has_dot else f'{str(path_func(text).stem)}{mod_text}'

    if flag == ProcessName.FULLNAME:
        return mod_text


def get_preview_replace(element, func_args, is_dir):
    return base_preview(element, g_replace_general, func_args, is_dir) if func_args else ''


def get_preview_casing(element, func_args, is_dir):
    file_case = func_args[0]
    ext_case = func_args[1]
    keep = func_args[2]

    tmp_fname = str(path_func(element).stem)
    tmp_ename = str(path_func(element).suffix)

    if keep:
        full_name = set_case(tmp_fname, keep, apply_case[file_case]) + \
                    set_case(tmp_ename, keep, apply_case[ext_case])
    else:
        full_name = apply_case[file_case](tmp_fname) + apply_case[ext_case](tmp_ename)

    return '' if full_name == element else str(full_name)


def get_preview_move(element, func_args, is_dir):
    return base_preview(element, g_move_general, func_args, is_dir)


def get_preview_spaces(element, func_args, is_dir):
    return base_preview(element, g_replace_spaces, func_args, is_dir)


def get_preview_counter(element, func_args, is_dir):
    return base_preview(element, g_preview_counter, func_args, is_dir)


def get_preview_renumber(element, func_args, is_dir):
    return base_preview(element, g_preview_renumber, func_args, is_dir)


def base_preview(element, func, func_args, is_dir):
    file_name = func_args[0]
    if file_name == ProcessName.NONE: return ''

    tmp = get_name_part(element, file_name, has_dot(element, is_dir))
    output = func(tmp, *func_args[1:])

    if not output:
        return ''

    return set_name_part(output, element, file_name, has_dot(element, is_dir))



