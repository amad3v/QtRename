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

from PyQt5.QtCore import QSize, pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QListWidget, QSizePolicy, QGridLayout

from qtrename.common import labels2errors, errors_map


class Errors(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('Errors')
        self.app_icon = parent.windowIcon()

        self.lbl_errors = QLabel('Filter errors:')
        self.cmb_errors = QComboBox()
        self.lst_errors = QListWidget()

        self.cmb_errors.addItems([items[1] for items in labels2errors])

        self.cmb_errors.currentIndexChanged.connect(self.load_errors)

        self.__init_ui()
        self.load_all_errors()

    def __init_ui(self):
        # set geometry
        self.lbl_errors.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # global layout
        self.global_layout = QGridLayout()
        self.global_layout.addWidget(self.lbl_errors, 0, 0, 1, 1)
        self.global_layout.addWidget(self.cmb_errors, 0, 1, 1, 2)
        self.global_layout.addWidget(self.lst_errors, 1, 0, 1, 3)

        # dialog settings
        self.setWindowIcon(self.app_icon)
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(QSize(731, 386))
        self.setLayout(self.global_layout)

    @pyqtSlot(int)
    def load_errors(self, index):
        self.lst_errors.clear()
        if self.cmb_errors.currentIndex():
            self.lst_errors.addItems(errors_map[labels2errors[index][0]])
        else:
            self.load_all_errors()

    def load_all_errors(self):
        for _,vals in errors_map.items():
            self.lst_errors.addItems(vals)
