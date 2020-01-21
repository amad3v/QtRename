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

def g_move_general(text, from_pos, count, is_backwards, new_pos, is_new_backwards, is_new_relative):
    if not is_backwards:
        result = move_chars(text[:from_pos] + text[from_pos + count:],
                            text[from_pos:from_pos + count],
                            new_pos,
                            is_new_backwards,
                            is_new_relative,
                            from_pos)
    else:
        if not from_pos:
            result = move_chars(text[:-count],
                                text[-count:],
                                new_pos - len(text) + count,
                                is_new_backwards,
                                is_new_relative,
                                from_pos)
        else:
            result = move_chars(text[:-count - from_pos] + text[-from_pos:],
                                text[-count - from_pos:-from_pos],
                                new_pos - len(text) + count,
                                is_new_backwards,
                                is_new_relative,
                                from_pos)

    return '' if result == text else result


def move_chars(text, to_move, pos, is_backward = False, is_relative = False, relative_to = 0):
    final_pos = pos

    if is_backward:
        if is_relative: final_pos -= relative_to
        return text[:-final_pos] + to_move + text[-final_pos:]
    else:
        if is_relative: final_pos += relative_to
        return text[:final_pos] + to_move + text[final_pos:]

