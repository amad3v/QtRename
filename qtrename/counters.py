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

p_counter = 0
p_enumerate = 0


def g_preview_counter(text: str, pos: int, sep: str, keep: bool, replace: str) -> str:
    tmp = text
    global p_counter
    p_counter += 1
    if not pos:
        tmp = f'{p_counter}{sep}{tmp}' if keep else f'{p_counter}{sep}{replace}'
    else:
        tmp = f'{tmp}{sep}{p_counter}' if keep else f'{replace}{sep}{p_counter}'

    return tmp if tmp != text else ''


def g_preview_renumber(text: str, start_from: int, increment: int, sep: str, zeros: bool, tot_count: int) -> str:
    global p_enumerate

    padding = '0' * (len(str((tot_count - 1) * increment + start_from)) - len(str(p_enumerate)))

    if not increment:
        return ''

    tmp = f'{padding}{p_enumerate}{sep}{text}' if zeros else f'{p_enumerate}{sep}{text}'

    p_enumerate += increment

    return tmp if tmp != text else ''
