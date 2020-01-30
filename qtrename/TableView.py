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

from PyQt5.QtCore import Qt, pyqtSlot, QPoint, pyqtSignal, QVariant, QSize, QDirIterator, QDir, QObject, QCoreApplication
from PyQt5.QtGui import QIcon, QStandardItem
from PyQt5.QtWidgets import QTableView, QAction, QMenu, QAbstractItemView, QFileIconProvider, QHeaderView

from qtrename import counters
from qtrename.common import os_type, path_func
from qtrename.preview import get_preview_replace

tr_ = QCoreApplication.translate


class TableView(QTableView):
    selection_changed = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.verticalHeader().hide()
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.horizontalScrollBar().hide()
        self.horizontalHeader().setResizeContentsPrecision(QHeaderView.Stretch)
        self.horizontalHeader().setStretchLastSection(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__show_action = QAction(self)
        self.__open_action = QAction(self)
        self.__c_menu = QMenu(self)
        self.__c_menu.addAction(self.__show_action)
        self.__c_menu.addSeparator()
        self.__c_menu.addAction(self.__open_action)
        self.__path = None
        self.__item = None

        self.__show_action.triggered.connect(self.open_in_explorer)
        self.__open_action.triggered.connect(self.open_as_file)
        self.customContextMenuRequested.connect(self.on_view_context_menu)

        self.retranslate_ui()

    def retranslate_ui(self):
        self.__show_action.setText(tr_('TableView', u'Open in &explorer'))
        self.__open_action.setText(tr_('TableView', u'Open &file'))

    @pyqtSlot(QPoint)
    def on_view_context_menu(self, point):
        idx = self.indexAt(point)
        if idx.column() != 0: return
        self.__path = path_func(idx.sibling(idx.row(), 2).data(Qt.DisplayRole))
        self.__item = self.__path.joinpath(idx.data(Qt.DisplayRole))
        self.__open_action.setDisabled(self.__item.is_dir())
        self.__c_menu.popup(self.viewport().mapToGlobal(point))

    @pyqtSlot()
    def open_in_explorer(self):
        if self.__item.is_file():
            path_to_item = str(self.__path)
        else:
            path_to_item = str(self.__item)

        self.execute_open(path_to_item)

    @pyqtSlot()
    def open_as_file(self):
        self.execute_open(str(self.__item))

    def execute_open(self, filename):
        if os_type == 'Windows':
            # if open file is cancelled
            # OSError is raised
            try:
                os.startfile(filename)
            except OSError:
                return
        elif os_type == 'Linux':
            subprocess.Popen(['xdg-open', filename])
        else:
            subprocess.Popen(['open', filename])

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


class DataSource(QObject):
    reset_model = pyqtSignal()
    update_row = pyqtSignal(list)
    update_item = pyqtSignal(int, int, QVariant)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ready = False
        self.data_contents = []
        self.__dir = ''
        self.__app_filter = ''
        self.__filter_files = ''
        self.__filter_dirs = ''
        self.__flags = ''
        self.__func_args = None
        self.__file_name = ''

    def __get_icon(self, file_info):
        if not self.__filter_dirs and file_info.isDir():
            return QIcon(QFileIconProvider().icon(file_info).pixmap(QSize(32, 32), QIcon.Disabled))

        return QIcon(QFileIconProvider().icon(file_info).pixmap(QSize(32, 32)))

    def setup_data_source(self, *args):
        self.__dir = args[0]
        self.__app_filter = args[1]
        self.__filter_files = args[2]
        self.__filter_dirs = args[3]
        self.__flags = args[4]
        self.__func_args = args[5]
        self.__file_name = args[6]

    def start_collector(self):
        self.data_contents.clear()
        dir_iterator = QDirIterator(self.__dir, self.__app_filter,
                                    QDir.Files | QDir.AllDirs | QDir.NoSymLinks | QDir.NoDotAndDotDot,
                                    self.__flags)

        self.__load_ordered(dir_iterator)
        self.reset_model.emit()
        while not self.ready:
            pass
        self.ready = False
        self.update_row.emit(self.data_contents)

    def __load_ordered(self, dir_iterator):
        tmp_files = list()

        while dir_iterator.hasNext():
            item = path_func(dir_iterator.next())
            next_element = item.name
            file_info = dir_iterator.fileInfo()

            if file_info.isDir():
                process_item = self.__filter_dirs
            elif file_info.isFile():
                process_item = self.__filter_files
            else:
                process_item = False

            data = [QStandardItem(self.__get_icon(file_info), next_element),
                    QStandardItem(get_preview_replace(next_element, self.__func_args, file_info.isDir())),
                    QStandardItem(str(item.parent)),
                    QStandardItem(str(process_item))]

            if file_info.isDir():
                self.data_contents.append(data)
            else:
                tmp_files.append(data)

        self.data_contents.sort(key=lambda element: element[0].data(Qt.DisplayRole).lower())
        tmp_files.sort(key=lambda element: element[0].data(Qt.DisplayRole).lower())
        self.data_contents.extend(tmp_files)

    def rename_files(self, func_args):
        selection = func_args[0]
        func = func_args[1]

        if not selection:
            for row in self.data_contents:
                if row[1].data(Qt.DisplayRole):
                    func(row[2].data(Qt.DisplayRole),
                         row[0].data(Qt.DisplayRole),
                         row[1].data(Qt.DisplayRole))
            return

        for index in range(selection[0], selection[1]):
            if self.data_contents[index][1].data(Qt.DisplayRole):
                func(self.data_contents[index][2].data(Qt.DisplayRole),
                     self.data_contents[index][0].data(Qt.DisplayRole),
                     self.data_contents[index][1].data(Qt.DisplayRole))

    def load_preview(self, func_args):
        selection = func_args[0]
        func = func_args[1]
        counters.p_counter = 0

        if not selection:
            for i, row in enumerate(self.data_contents):
                is_dir = path_func(row[2].data(Qt.DisplayRole)).joinpath(row[0].data(Qt.DisplayRole)).is_dir()
                if row[3].data(Qt.DisplayRole) == 'True':
                    new_name = QStandardItem(func(row[0].data(Qt.DisplayRole), func_args[2:], is_dir))
                    self.data_contents[i][1] = new_name
                    self.update_item.emit(i, 1, new_name)
            return

        for i, row in enumerate(self.data_contents):
            if i in range(selection[0], selection[1]):
                if row[3].data(Qt.DisplayRole) == 'True':
                    is_dir = path_func(row[2].data(Qt.DisplayRole)).joinpath(row[0].data(Qt.DisplayRole)).is_dir()
                    new_name = QStandardItem(func(row[0].data(Qt.DisplayRole), func_args[2:], is_dir))
                    self.data_contents[i][1] = new_name
                    self.update_item.emit(i, 1, new_name)
            else:
                self.data_contents[i][1] = QStandardItem('')
                self.update_item.emit(i, 1, QStandardItem(''))

    @pyqtSlot(bool)
    def ready_to_load(self):
        self.ready = True
