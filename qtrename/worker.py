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
    
    
from PyQt5.QtCore import *


class WorkerSignals(QObject):
    done = pyqtSignal()


class Worker(QRunnable):
    def __init__(self, func, args=None):
        super(Worker, self).__init__()

        self.func = func
        self.args = args
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        if self.args:
            self.func(self.args)
        else:
            self.func()

        self.signals.done.emit()