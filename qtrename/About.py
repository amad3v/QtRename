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
 
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout
from qtrename.common import set_bold


class About(QDialog):
    def __init__(self, parent, icon, title, description, link):
        super().__init__(parent)
        self.setWindowTitle('About QtRename')
        self.app_icon = parent.windowIcon()
        self.logo = icon
        self.lbl_name = QLabel(title)
        self.lbl_description = QLabel(description)
        self.lbl_link = QLabel(f'<a href="{link}">GitHub.com</a>')
        self.lbl_copyright = QLabel('\nCopyright \xa9 2020 - amad3v\n')
        self.lbl_warning = QLabel('This program comes with absolutely no warranty.')
        self.license_link = 'https://www.gnu.org/licenses/gpl-3.0.html'
        self.license_text = f'See the <a href="{self.license_link}">GNU General Public License</a>' \
                            ' version 3 or later for details.'

        self.small_print = QFont()
        self.small_print.setPointSize(8)

        self.__init_ui()

    def __init_ui(self):
        # create picture container
        self.lbl_container = QLabel(self)
        self.lbl_container.setPixmap(self.logo)
        self.lbl_container.setAlignment(Qt.AlignCenter)

        # app label
        self.lbl_name.setFont(set_bold(True))
        self.lbl_name.setAlignment(Qt.AlignCenter)

        # app description
        self.lbl_description.setAlignment(Qt.AlignCenter)

        # app link
        self.lbl_link.setOpenExternalLinks(True)
        self.lbl_link.setAlignment(Qt.AlignCenter)

        # copyright
        self.lbl_copyright.setAlignment(Qt.AlignCenter)
        self.lbl_copyright.setFont(self.small_print)

        # warning
        self.lbl_warning.setAlignment(Qt.AlignCenter)
        self.lbl_warning.setFont(self.small_print)

        # license
        self.lbl_license = QLabel(self.license_text)
        self.lbl_license.setOpenExternalLinks(True)
        self.lbl_license.setAlignment(Qt.AlignCenter)
        self.lbl_license.setFont(self.small_print)

        # global layout
        self.global_layout = QVBoxLayout()
        self.global_layout.addWidget(self.lbl_container)
        self.global_layout.addWidget(self.lbl_name)
        self.global_layout.addWidget(self.lbl_description)
        self.global_layout.addWidget(self.lbl_link)
        self.global_layout.addWidget(self.lbl_copyright)
        self.global_layout.addWidget(self.lbl_warning)
        self.global_layout.addWidget(self.lbl_license)

        # dialog settings
        self.setWindowIcon(self.app_icon)
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(QSize(400, 310))
        self.setLayout(self.global_layout)
