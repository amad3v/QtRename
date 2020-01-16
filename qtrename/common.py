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

import platform
import re
from enum import Enum
from pathlib import Path

from PyQt5 import QtGui
from PyQt5.QtCore import QDirIterator
from PyQt5.QtGui import QFont, QPalette, QPixmap, QIcon, QColor

os_type = platform.system()

PRIMARY_DARK = QColor(53, 53, 53)
TEXT_DARK = QColor(255, 255, 255)
DISABLED_DARK = QColor(128, 128, 128)
BASE_DARK = QColor(25, 25, 25)

windows = '\\/:*?"<>|'

flags_dict = {
    True: QDirIterator.Subdirectories,
    False: QDirIterator.NoIteratorFlags
}

animation_tones = {'green': ":/qtrenamer/anim/animg",
                   'pink': ":/qtrenamer/anim/animp",
                   'orange': ":/qtrenamer/anim/animo",
                   'blue': ":/qtrenamer/anim/animd",
                   'default': ":/qtrenamer/anim/animd"}

dark_theme = {'p_color': (PRIMARY_DARK, QPalette.Window, QPalette.AlternateBase, QPalette.Button),
              't_color': (TEXT_DARK, QPalette.WindowText, QPalette.ToolTipBase, QPalette.ToolTipText,
                          QPalette.Text, QPalette.ButtonText, QPalette.HighlightedText)}

dict_tones = {
    'orange': (QColor(255, 102, 0, 128), QColor(255, 102, 0), 3, 'Dark &Orange'),
    'green': (QColor(42, 218, 130, 128), QColor(42, 218, 130), 2, 'Dark &Green'),
    'pink': (QColor(218, 42, 130, 128), QColor(218, 42, 130), 4, 'Dark &Pink'),
    'blue': (QColor(42, 130, 218, 128), QColor(42, 130, 218), 1, 'Dark &Blue'),
    'default': (None, None, 0, '&Default')
}


dict_slots = {
    dict_tones['orange'][3]: ('dark', 'orange'),
    dict_tones['green'][3]: ('dark', 'green'),
    dict_tones['pink'][3]: ('dark', 'pink'),
    dict_tones['blue'][3]: ('dark', 'blue'),
    dict_tones['default'][3]: ('default', 'default')
}


errors_map = {
    'exists': [],
    'perms': [],
    'not_found': [],
    'other': []
}


labels2errors = (
    ('all', 'All'),
    ('exists', 'File/directory already exists'),
    ('perms', 'Permission denied'),
    ('not_found', 'File/directory doesn\'t exist'),
    ('other', 'Other errors')
)

root_dir = {
    'Windows': Path.home().drive,
    'Linux': Path.home().root,
    'Darwin': Path.home().root
}

list_old_names = []



class ProcessName(Enum):
    NONE = -1
    FILENAME = 0
    EXTENSION = 1
    FULLNAME = 2


dict_process = {
    (True, True): ProcessName.FULLNAME,
    (True, False): ProcessName.FILENAME,
    (False, True): ProcessName.EXTENSION,
    (False, False): ProcessName.NONE
}


def undo_rename():
    global list_old_names

    for old_file, new_file in list_old_names:
        try:
            if new_file.exists():
                raise FileExistsError

            if not old_file.exists():
                raise FileNotFoundError

            old_file.rename(new_file)

        except FileExistsError:
            errors_map['exists'].append(f'{str(old_file)} -> {Path(new_file).name}')

        except PermissionError:
            errors_map['perms'].append(f'{str(old_file)} -> {Path(new_file).name}')

        except FileNotFoundError:
            errors_map['not_found'].append(f'{str(old_file)} -> {Path(new_file).name}')

        except Exception:
            errors_map['other'].append(f'{str(old_file)} -> {Path(new_file).name}')
        finally:
            continue

    list_old_names.clear()


def rename_items(parent, old_name, new_name):
    if not new_name: return

    global list_old_names
    old_file = Path(parent).joinpath(old_name)
    new_file = Path(parent).joinpath(new_name)

    try:
        if new_file.exists():
            raise FileExistsError

        if not old_file.exists():
            raise FileNotFoundError

        list_old_names.append((new_file, old_file))
        old_file.rename(new_file)

    except FileExistsError:
        errors_map['exists'].append(f'{str(old_file)} -> {new_name}')

    except FileNotFoundError:
        errors_map['not_found'].append(f'{str(old_file)} -> {new_name}')

    except PermissionError:
        errors_map['perms'].append(f'{str(old_file)} -> {new_name}')

    except Exception:
        errors_map['other'].append(f'{str(old_file)} -> {new_name}')


def set_bold(is_bold) -> QFont:
    bold = QFont()
    bold.setBold(is_bold)

    return bold


def verify_filter(subject):
    if not subject:
        return True
    pattern = re.compile(r"(^\*\.\w+$)|(^\*\.\*$)|(^\*$)", re.I)

    return pattern.match(subject)


def get_filter(subject):
    if not subject or subject == '*.*': return '*'

    if re.match(r"(^\w+$)", subject, re.I): return '*.' + subject
    if re.match(r"(^\.{1}\w+$)", subject, re.I): return '*' + subject

    return subject


def get_icon(resource):
    icon = QIcon()
    icon.addPixmap(QPixmap(resource), QtGui.QIcon.Normal, QtGui.QIcon.Off)

    return icon


def validate_path(directory):
    if not directory: return False
    if Path(directory).is_dir(): return True
    return False
