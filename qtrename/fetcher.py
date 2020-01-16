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

from pathlib import Path

from PyQt5.QtCore import QDirIterator, QDir, Qt, QSize, QFileInfo
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtWidgets import QFileIconProvider

import qtrename.counters
from qtrename.common import ProcessName
from qtrename.preview import get_preview_replace


class Fetcher:
    def __init__(self, parent=None):
        self.__smi = QStandardItemModel(parent)
        self.__smi.setHorizontalHeaderLabels(('Before', 'After', '', '', ''))
        self.__dir = ''
        self.__filter_files = None
        self.__filter_dirs = None
        self.__flags = None
        self.__app_filter = ''
        self.__dir_iterator = None
        self.__func_args = None
        self.__icons = None
        self.__setup_icons()
        self.__file_name = ProcessName.FILENAME

    def __setup_icons(self):
        file_info = QFileInfo(str(Path().home()))
        self.__icons = (QIcon(QFileIconProvider().icon(file_info).pixmap(QSize(32, 32), QIcon.Disabled)),
                        QIcon(QFileIconProvider().icon(file_info).pixmap(QSize(32, 32))))

    def __get_icon(self, file_info):
        if not self.__filter_dirs and file_info.isDir():
            return self.__icons[0]

        if file_info.isDir():
            return self.__icons[1]

        return QIcon(QFileIconProvider().icon(file_info).pixmap(QSize(32, 32)))

    def setup_fetcher(self, *args):
        self.__dir = args[0]
        self.__filter_files = args[2]
        self.__filter_dirs = args[3]
        self.__flags = args[4]
        self.__func_args = args[5]
        self.__app_filter = args[1]
        self.__file_name = args[6]

    def __load_model(self):
        while self.__dir_iterator.hasNext():
            item = Path(self.__dir_iterator.next())
            next_element = item.name
            file_info = self.__dir_iterator.fileInfo()
            sort_order = 0 if file_info.isDir() else 1

            process_dirs = not self.__filter_dirs and file_info.isDir()

            if not self.__filter_files and file_info.isFile():
                continue

            self.__smi.appendRow((
                QStandardItem(self.__get_icon(file_info), next_element),
                QStandardItem(get_preview_replace(next_element, self.__func_args)),
                QStandardItem(str(item.parent)),
                QStandardItem(str(process_dirs)),
                QStandardItem(f'{sort_order}{next_element}'.lower())
            ))

    def rename_files(self, func_args):
        if not func_args[0]:
            for index_row in range(self.__smi.rowCount()):
                if self.__smi.item(index_row, 3).data(Qt.DisplayRole) == 'False':
                    func_args[1](self.__smi.item(index_row, 2).data(Qt.DisplayRole),
                                 self.__smi.item(index_row, 0).data(Qt.DisplayRole),
                                 self.__smi.item(index_row, 1).data(Qt.DisplayRole))

        else:
            for index in func_args[0]:
                if self.__smi.item(index.row(), 3).data(Qt.DisplayRole) == 'False':
                    func_args[1](self.__smi.item(index.row(), 2).data(Qt.DisplayRole),
                                 self.__smi.item(index.row(), 0).data(Qt.DisplayRole),
                                 index.data(Qt.DisplayRole))

    def load_preview(self, func_args):
        selection = func_args[0]
        qtrename.counters.p_counter = 0

        if not selection:
            for index_row in range(self.__smi.rowCount()):
                if self.__smi.item(index_row, 3).data(Qt.DisplayRole) == 'False':
                    new_name = func_args[1](self.__smi.item(index_row, 0).data(Qt.DisplayRole), func_args[2:])
                    self.__smi.item(index_row, 1).setText(new_name)
        else:
            for index_row in range(self.__smi.rowCount()):
                self.__smi.item(index_row, 1).setText('')

            for index in selection:
                if self.__smi.item(index.row(), 3).data(Qt.DisplayRole) == 'False':
                    new_name = func_args[1](index.data(Qt.DisplayRole), func_args[2:])
                    self.__smi.item(index.row(), 1).setText(new_name)

    def start_collector(self):
        self.__smi.removeRows(0, self.__smi.rowCount())

        self.__dir_iterator = QDirIterator(self.__dir, QDir.Dirs | QDir.NoSymLinks | QDir.NoDotAndDotDot, self.__flags)
        self.__load_model()

        self.__dir_iterator = QDirIterator(self.__dir, self.__app_filter, QDir.Files, self.__flags)
        self.__load_model()

    @property
    def smi_model(self):
        self.__smi.sort(4, Qt.AscendingOrder)
        return self.__smi
