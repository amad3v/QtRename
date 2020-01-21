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

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QMovie, QColor
from PyQt5.QtWidgets import QWidget, QLabel


class Animation(QWidget):
    def __init__(self, parent, file_name, rect, bg):
        super().__init__(parent)
        self.__m_widget = QWidget(self)
        self.__movie = QMovie()
        self.__movie.setCacheMode(QMovie.CacheAll)
        self.__movie_label = QLabel(self.__m_widget)

        self.__m_widget.setGeometry(rect)
        self.__m_widget.setAutoFillBackground(True)

        self.__movie_label.setAlignment(Qt.AlignCenter)
        self.__movie_label.setMovie(self.__movie)
        self.setup_animation(file_name, bg)
        self.movie_stop()

    def movie_start(self):
        self.__movie.start()
        self.show()

    def movie_stop(self):
        self.hide()
        self.__movie.stop()

    def setup_animation(self, file_name, color):
        self.__movie.setFileName(file_name)

        palette = QPalette()
        palette.setColor(QPalette.Background, color)
        self.__m_widget.setPalette(palette)

    def resizeEvent(self, event):
        self.__movie_label.setGeometry(int((self.width() - 200) / 2), int((self.height() - 200) / 2), 200, 200)
