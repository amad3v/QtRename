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

import os
import subprocess
from pathlib import Path

from PyQt5.QtCore import Qt, pyqtSlot, QPoint, pyqtSignal, QItemSelection, QItemSelectionModel
from PyQt5.QtWidgets import QTableView, QAction, QMenu, QAbstractItemView

from qtrename.common import os_type


class TableView(QTableView):
    selection_changed = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)  # |
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.verticalHeader().hide()
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.horizontalScrollBar().hide()
        self.__show_action = QAction('Open in &explorer', self)
        self.__open_action = QAction('Open &file', self)
        self.__c_menu = QMenu(self)
        self.customContextMenuRequested.connect(self.on_view_context_menu)
        self.s = None

    @pyqtSlot(QPoint)
    def on_view_context_menu(self, point):
        idx = self.indexAt(point)

        if idx.column() != 0: return

        path = Path(idx.sibling(idx.row(), 2).data(Qt.DisplayRole))
        item = path.joinpath(idx.data(Qt.DisplayRole))

        self.__open_action.setDisabled(item.is_dir())

        self.__show_action.triggered.connect(lambda: self.open_in_explorer(path, item, False))
        self.__open_action.triggered.connect(lambda: self.open_in_explorer(path, item, True))

        self.__c_menu.addAction(self.__show_action)
        self.__c_menu.addSeparator()
        self.__c_menu.addAction(self.__open_action)
        self.__c_menu.popup(self.viewport().mapToGlobal(point))

    @pyqtSlot(Path, Path, bool)
    def open_in_explorer(self, path, item, is_open=False):
        if not is_open:
            if item.is_file():
                path_to_item = str(path)
            else:
                path_to_item = str(item)
        else:
            path_to_item = str(item)

        if os_type == 'Windows':
            # if open file is cancelled
            # OSError is raised
            try:
                os.startfile(path_to_item)
            except OSError:
                return
        elif os_type == 'Linux':
            subprocess.Popen(['xdg-open', path_to_item])
        else:
            subprocess.Popen(['open', path_to_item])

    def resizeEvent(self, event):
        super().resizeEvent(event)
        list_width = int(self.width() / 2) - 1
        self.setColumnWidth(0, list_width)
        self.setColumnWidth(1, list_width)

    def selectionChanged(self, selected, deselected):
        self.selection_changed.emit(self.selectionModel().selectedRows(0))

    def hide_columns(self, start, end):
        for i in range(start, end):
            self.setColumnHidden(i, True)
            
