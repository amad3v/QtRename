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

from PyQt5 import QtCore
from PyQt5.QtCore import QMetaObject, QSize, QMargins, QTimer, QRect, pyqtSlot, Qt, QModelIndex
from PyQt5.QtGui import QFont, QPalette
from PyQt5.QtWidgets import QMainWindow, QWidget, QSizePolicy, QStackedWidget, QTabWidget, QFrame, QGroupBox, QSpinBox, \
    QLabel, QLineEdit, QCheckBox, QRadioButton, QComboBox, QGridLayout, QPushButton, QMenuBar, QMenu, QStatusBar, \
    QAction, QVBoxLayout, QSpacerItem, QApplication, QActionGroup, QDesktopWidget

import qtrename.counters
from qtrename.Errors import Errors
from qtrename.TableView import TableView
from qtrename.common import *
import qtrename.qtrenamer_rc


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QtRename")
        self.central_widget = QWidget(self)
        self.setWindowIcon(get_icon(":/qtrenamer/imgs/app_icon"))
        QMetaObject.connectSlotsByName(self)

        self.stacked_tabs = QStackedWidget(self.centralWidget())
        self.stk_general = QWidget()
        self.stk_numbers = QWidget()
        self.layout_stk_general = QVBoxLayout()
        self.layout_stk_numbers = QVBoxLayout()

        self.tab_general = QTabWidget(self.stk_general)
        self.tab_replace = QWidget()
        self.tab_casing = QWidget()
        self.tab_add_remove = QWidget()
        self.tab_move = QWidget()
        self.tab_spaces = QWidget()

        self.tab_numbers = QTabWidget(self.stk_numbers)
        self.tab_counter = QWidget()
        self.tab_renumber = QWidget()

        self.setup_menu()
        self.setup_timer()
        self.setup_stacks()
        self.setup_tabs()
        self.setup_tab_replace()
        self.setup_tab_casing()
        self.setup_tab_add_remove()
        self.setup_tab_move()
        self.setup_tab_spaces()
        self.setup_tab_counter()
        self.setup_tab_renumber()
        self.setup_options()
        self.setup_view()
        self.setup_central_widget()
        self.setup_buttons()
        self.setup_text()
        self.setup_tab_order()
        self.setup_center()

        QtCore.QMetaObject.connectSlotsByName(self)

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self.resize_buttons()

    def showEvent(self, a0):
        super().showEvent(a0)
        self.resize_buttons()

    def show_errors(self):
        Errors(self).exec_()

    def setup_center(self):
        self.av_geo = QDesktopWidget().availableGeometry()
        self.setMinimumSize(int(self.av_geo.width() * 0.75), int(self.av_geo.height() * 0.75))
        self.setGeometry(0,0,int(self.av_geo.width() * 0.75), int(self.av_geo.height() * 0.75))

        self.main_rect = self.frameGeometry()
        self.center_point = self.av_geo.center()
        self.main_rect.moveCenter(self.center_point)
        self.move(self.main_rect.topLeft())

    def setup_timer(self):
        self.timer = QTimer()
        self.timer.setInterval(400)
        self.timer.setSingleShot(True)

    def setup_buttons(self):
        self.btn_rename = QPushButton('&Rename', self.centralWidget())
        self.btn_rename.setFixedSize(80, 30)
        self.btn_rename.raise_()

        self.stk_next = QPushButton('>', self.centralWidget())
        self.stk_next.setFixedSize(30, 30)
        self.stk_next.raise_()

        self.stk_previous = QPushButton('<', self.centralWidget())
        self.stk_previous.setFixedSize(30, 30)
        self.stk_previous.raise_()

    def setup_central_widget(self):
        self.layout_sections = QGridLayout()
        self.layout_sections.setContentsMargins(QMargins(5, 5, 5, 5))
        self.layout_sections.addWidget(self.options_group, 0, 0, 1, 1)
        self.layout_sections.addLayout(self.files_list_layout, 0, 1, 2, 1)
        self.layout_sections.addWidget(self.stacked_tabs, 1, 0, 1, 1)
        self.layout_sections.setColumnStretch(1, 3)
        self.layout_sections.setColumnStretch(0, 1)

        self.central_widget.setLayout(self.layout_sections)
        self.setCentralWidget(self.central_widget)

    def setup_text(self):
        self.tab_general.setTabText(self.tab_general.indexOf(self.tab_replace), "Replace")
        self.tab_general.setTabText(self.tab_general.indexOf(self.tab_casing), "Casing")
        self.tab_general.setTabText(self.tab_general.indexOf(self.tab_add_remove), "Add/Remove")
        self.tab_general.setTabText(self.tab_general.indexOf(self.tab_move), "Move")
        self.tab_general.setTabText(self.tab_general.indexOf(self.tab_spaces), "Spaces")
        self.tab_numbers.setTabText(self.tab_numbers.indexOf(self.tab_counter), "Counter")
        self.tab_numbers.setTabText(self.tab_numbers.indexOf(self.tab_renumber), "Enumerate")

    def setup_menu(self):
        self.menubar = QMenuBar(self)
        self.main_menu = QMenu('&Settings', self.menubar)
        self.menu_themes = QMenu('&Themes', self.main_menu)

        self.themes_group = QActionGroup(self.menu_themes)
        self.statusbar = QStatusBar(self)

        self.action_undo = QAction('&Undo', self)
        self.action_about = QAction('&About', self)
        self.action_exit = QAction('E&xit', self)
        self.action_default = QAction('&Default', self)
        self.action_dark_blue = QAction('Dark &Blue', self)
        self.action_dark_green = QAction('Dark &Green', self)
        self.action_dark_orange = QAction('Dark &Orange', self)
        self.action_dark_pink = QAction('Dark &Pink', self)
        self.action_rename = QAction('&Rename', self)
        self.action_errors = QAction('&Errors Log', self)
        self.actionAbout_Qt = QAction('About Qt', self)

        self.action_undo.setShortcut("Ctrl+Z")
        self.action_about.setShortcut("F1")
        self.action_exit.setShortcut("Ctrl+Q")
        self.action_rename.setShortcut("Ctrl+R")
        self.action_errors.setShortcut("Ctrl+E")

        self.action_undo.setEnabled(False)
        self.action_default.setCheckable(True)
        self.action_default.setChecked(True)
        self.action_dark_blue.setCheckable(True)
        self.action_dark_green.setCheckable(True)
        self.action_dark_orange.setCheckable(True)
        self.action_dark_pink.setCheckable(True)

        self.menu_themes.addAction(self.action_default)
        self.menu_themes.addAction(self.action_dark_blue)
        self.menu_themes.addAction(self.action_dark_green)
        self.menu_themes.addAction(self.action_dark_orange)
        self.menu_themes.addAction(self.action_dark_pink)

        self.themes_group.addAction(self.action_default)
        self.themes_group.addAction(self.action_dark_blue)
        self.themes_group.addAction(self.action_dark_green)
        self.themes_group.addAction(self.action_dark_orange)
        self.themes_group.addAction(self.action_dark_pink)

        self.main_menu.addAction(self.action_undo)
        self.main_menu.addAction(self.action_rename)
        self.main_menu.addAction(self.action_errors)
        self.main_menu.addAction(self.menu_themes.menuAction())
        self.main_menu.addAction(self.action_about)
        self.main_menu.addAction(self.actionAbout_Qt)
        self.main_menu.addSeparator()
        self.main_menu.addAction(self.action_exit)

        self.menubar.addAction(self.main_menu.menuAction())

        self.setMenuBar(self.menubar)
        self.themes_group.setExclusive(True)

        self.setStatusBar(self.statusbar)
        self.lbl_status = QLabel()
        self.lbl_status.setAlignment(Qt.AlignRight)
        self.statusbar.addPermanentWidget(self.lbl_status)

    def setup_slots(self):
        self.tab_general.currentChanged.connect(self.on_tab_gen_changed)
        self.tab_numbers.currentChanged.connect(self.on_tab_nums_changed)
        self.menu_themes.triggered[QAction].connect(self.theme_selector)
        self.stk_previous.clicked.connect(self.previous_stacked_page)
        self.stk_next.clicked.connect(self.next_stacked_page)
        self.btn_load_path.clicked.connect(self.get_dir)
        self.btn_rename.clicked.connect(self.on_rename_clicked)
        self.btn_go_up.clicked.connect(self.level_up)
        self.txt_load_path.editingFinished.connect(self.list_content)
        self.txt_filter_ext.editingFinished.connect(self.check_field)
        self.lst_loaded_files.doubleClicked.connect(self.open_dir)
        self.lst_loaded_files.selection_changed.connect(self.on_selection_changed)



        self.rdb_cupper_file.toggled.connect(self.set_file_case)
        self.rdb_clower_file.toggled.connect(self.set_file_case)
        self.rdb_csentence_file.toggled.connect(self.set_file_case)
        self.rdb_ctitle_file.toggled.connect(self.set_file_case)
        self.rdb_csame_file.toggled.connect(self.set_file_case)
        self.rdb_cinvert_file.toggled.connect(self.set_file_case)
        self.rdb_crandom_file.toggled.connect(self.set_file_case)

        self.rdb_cupper_ext.toggled.connect(self.set_ext_case)
        self.rdb_clower_ext.toggled.connect(self.set_ext_case)
        self.rdb_ctitle_ext.toggled.connect(self.set_ext_case)
        self.rdb_csame_ext.toggled.connect(self.set_ext_case)
        self.rdb_cinvert_ext.toggled.connect(self.set_ext_case)
        self.rdb_crandom_ext.toggled.connect(self.set_ext_case)

        self.chk_ignore_mixed.stateChanged.connect(self.switch_mixed)
        self.chk_ignore_upper.stateChanged.connect(self.switch_upper)

        self.txt_replace.textChanged.connect(self.preview_general_replace)
        self.txt_find.textChanged.connect(self.check_options)
        self.txt_find.editingFinished.connect(self.preview_general_replace)
        self.chk_swap.stateChanged.connect(self.enable_swap)
        self.chk_sensetive.stateChanged.connect(self.preview_general_replace)
        self.spn_max_swap.valueChanged.connect(self.preview_general_replace)
        self.spn_skip.valueChanged.connect(self.preview_general_replace)
        self.chk_regex.stateChanged.connect(self.enable_regex)

        self.chk_add_remove.stateChanged.connect(self.on_addrem_changed)
        self.grp_add.clicked.connect(self.on_grp_add_toggled)
        self.grp_remove.clicked.connect(self.on_grp_rem_toggled)
        self.txt_insert.textChanged.connect(self.preview_general_addrem)
        self.spn_at_add.valueChanged.connect(self.preview_general_addrem)
        self.chk_overwrite.stateChanged.connect(self.preview_general_addrem)
        self.chk_backw_add.stateChanged.connect(self.preview_general_addrem)
        self.spn_del.valueChanged.connect(self.preview_general_addrem)
        self.spn_at_del.valueChanged.connect(self.preview_general_addrem)
        self.chk_backw_del.stateChanged.connect(self.preview_general_addrem)
        self.chk_add_remove.stateChanged.connect(self.preview_general_addrem)

        self.spn_move.valueChanged.connect(self.preview_general_move)
        self.spn_move_from.valueChanged.connect(self.preview_general_move)
        self.chk_backw_move.stateChanged.connect(self.preview_general_move)
        self.spn_to_pos.valueChanged.connect(self.preview_general_move)
        self.chk_backw_to.stateChanged.connect(self.preview_general_move)
        self.chk_relative.stateChanged.connect(self.preview_general_move)

        self.chk_leading.stateChanged.connect(self.preview_general_spaces)
        self.chk_trailing.stateChanged.connect(self.preview_general_spaces)
        self.chk_many_one.stateChanged.connect(self.preview_general_spaces)
        self.chk_maintain_before.stateChanged.connect(self.on_maintain_before_checked)
        self.txt_maintain_before.textChanged.connect(self.preview_general_spaces)
        self.chk_maintain_after.stateChanged.connect(self.on_maintain_after_checked)
        self.txt_maintain_after.textChanged.connect(self.preview_general_spaces)
        self.rdb_x_chars.toggled.connect(self.on_x_chars_toggled)
        self.rdb_one_char.toggled.connect(self.on_one_char_toggled)
        self.txt_x_chars.textChanged.connect(self.preview_general_spaces)
        self.txt_one_char.textChanged.connect(self.preview_general_spaces)

        self.cmb_counter.currentIndexChanged.connect(self.preview_numbers_counter)
        self.txt_separator.textChanged.connect(self.preview_numbers_counter)
        self.rdb_keep_name.toggled.connect(self.preview_numbers_counter)
        self.txt_replace_name.textChanged.connect(self.preview_numbers_counter)
        self.rdb_replace_name.toggled.connect(self.on_replace_name_toggled)

        self.spn_start_enum.valueChanged.connect(self.preview_numbers_renumber)
        self.spn_step.valueChanged.connect(self.preview_numbers_renumber)
        self.txt_sep_enum.textChanged.connect(self.preview_numbers_renumber)
        self.chk_padding.stateChanged.connect(self.preview_numbers_renumber)
        self.chk_file_in.stateChanged.connect(self.set_files)
        self.chk_dirs_in.stateChanged.connect(self.set_dirs)
        self.chk_subdirs_in.stateChanged.connect(self.set_sub_dirs)
        self.chk_process_name.stateChanged.connect(self.set_process_name)
        self.chk_process_ext.stateChanged.connect(self.set_process_name)

        self.menubar.triggered[QAction].connect(self.process_trigger)

    def setup_tab_order(self):
        lst_widgets = (
            self.chk_file_in, self.chk_dirs_in, self.chk_subdirs_in, self.chk_process_name, self.chk_process_ext,
            self.btn_load_path, self.txt_load_path, self.txt_filter_ext, self.btn_go_up, self.tab_general,
            self.txt_find, self.txt_replace, self.spn_skip, self.spn_max_swap, self.chk_sensetive,
            self.chk_swap, self.chk_regex, self.btn_rename, self.stk_previous, self.stk_next, self.rdb_cupper_file,
            self.rdb_clower_file, self.rdb_csentence_file, self.rdb_ctitle_file, self.rdb_csame_file,
            self.rdb_cinvert_file, self.rdb_crandom_file, self.rdb_cupper_ext, self.rdb_clower_ext, self.rdb_ctitle_ext,
            self.rdb_csame_ext, self.rdb_cinvert_ext, self.rdb_crandom_ext, self.chk_ignore_upper,
            self.chk_ignore_mixed, self.txt_insert, self.spn_at_add, self.chk_overwrite, self.chk_backw_add,
            self.spn_del, self.spn_at_del, self.chk_backw_del, self.chk_add_remove, self.spn_move, self.spn_move_from,
            self.chk_backw_move, self.spn_to_pos, self.chk_backw_to, self.chk_relative, self.chk_leading,
            self.chk_trailing, self.chk_many_one, self.chk_maintain_before, self.txt_maintain_before,
            self.chk_maintain_after, self.txt_maintain_after, self.rdb_x_chars, self.txt_x_chars,
            self.rdb_one_char, self.txt_one_char, self.chk_padding, self.tab_numbers, self.rdb_replace_name,
            self.cmb_counter, self.rdb_keep_name, self.txt_replace_name, self.txt_separator, self.spn_start_enum,
            self.spn_step, self.txt_sep_enum,  self.lst_loaded_files
        )

        for i in range(1, len(lst_widgets)):
            self.setTabOrder(lst_widgets[i - 1], lst_widgets[i])

    def setup_options(self):
        self.options_group = QFrame()
        self.options_group.setFrameShape(QFrame.StyledPanel)
        self.options_group.setFrameShadow(QFrame.Sunken)
        self.options_layout = QGridLayout(self.options_group)
        self.lbl_include = QLabel('Include')
        self.lbl_options = QLabel('Options')
        self.chk_file_in = QCheckBox('Files', self.options_group)
        self.chk_process_name = QCheckBox('Process Names', self.options_group)
        self.chk_dirs_in = QCheckBox('Directories', self.options_group)
        self.chk_process_ext = QCheckBox('Process Extensions', self.options_group)
        self.chk_subdirs_in = QCheckBox('Subdirectories', self.options_group)

        self.lbl_include.setFont(set_bold(True))
        self.lbl_options.setFont(set_bold(True))

        self.chk_file_in.setChecked(True)
        self.chk_process_name.setChecked(True)

        self.options_layout.addWidget(self.lbl_include, 0, 0, 1, 1)
        self.options_layout.addWidget(self.lbl_options, 0, 1, 1, 1)
        self.options_layout.addWidget(self.chk_file_in, 1, 0, 1, 1)
        self.options_layout.addWidget(self.chk_process_name, 1, 1, 1, 1)
        self.options_layout.addWidget(self.chk_dirs_in, 2, 0, 1, 1)
        self.options_layout.addWidget(self.chk_process_ext, 2, 1, 1, 1)
        self.options_layout.addWidget(self.chk_subdirs_in, 3, 0, 1, 1)

        self.options_group.setLayout(self.options_layout)

    def setup_view(self):
        self.files_list_layout = QGridLayout()
        self.btn_load_path = QPushButton('')
        self.btn_go_up = QPushButton('')
        self.txt_load_path = QLineEdit()
        self.txt_filter_ext = QLineEdit()
        self.lst_loaded_files = TableView(self.centralWidget())

        self.btn_load_path.setIcon(get_icon(":/qtrenamer/imgs/lookup"))
        self.btn_load_path.setIconSize(QtCore.QSize(24, 24))
        self.btn_load_path.setFixedSize(QSize(30, 30))
        self.btn_go_up.setIcon(get_icon(":/qtrenamer/imgs/up"))
        self.btn_go_up.setIconSize(QtCore.QSize(24, 24))
        self.btn_go_up.setFixedSize(QSize(30, 30))
        self.txt_filter_ext.setText('*.*')
        self.txt_filter_ext.setFixedWidth(50)

        self.files_list_layout.addWidget(self.btn_load_path, 0, 0, 1, 1)
        self.files_list_layout.addWidget(self.btn_go_up, 0, 1, 1, 1)
        self.files_list_layout.addWidget(self.txt_load_path, 0, 2, 1, 1)
        self.files_list_layout.addWidget(self.txt_filter_ext, 0, 3, 1, 1)
        self.files_list_layout.addWidget(self.lst_loaded_files, 1, 0, 1, 4)

    def setup_tabs(self):
        self.tab_general.setTabPosition(QTabWidget.West)
        self.tab_general.setCurrentIndex(0)
        self.tab_numbers.setCurrentIndex(0)
        self.tab_numbers.setTabPosition(QTabWidget.West)
        self.tab_general.addTab(self.tab_replace, '')
        self.tab_general.addTab(self.tab_casing, '')
        self.tab_general.addTab(self.tab_add_remove, '')
        self.tab_general.addTab(self.tab_move, '')
        self.tab_general.addTab(self.tab_spaces, '')
        self.tab_numbers.addTab(self.tab_counter, '')
        self.tab_numbers.addTab(self.tab_renumber, '')

    def setup_stacks(self):
        self.stacked_tabs.setFrameShape(QFrame.NoFrame)
        self.stacked_tabs.setLineWidth(1)
        self.stacked_tabs.addWidget(self.stk_general)
        self.stacked_tabs.addWidget(self.stk_numbers)
        self.stacked_tabs.setCurrentIndex(0)
        self.lbl_stk_general = QLabel('General', self.stk_general)
        self.lbl_stk_numbers = QLabel('Numbers', self.stk_numbers)

        font = QFont()
        font.setPointSize(14)
        font.setBold(True)

        self.lbl_stk_general.setFont(font)
        self.lbl_stk_numbers.setFont(font)

        self.layout_stk_general.addWidget(self.lbl_stk_general)
        self.layout_stk_general.addWidget(self.tab_general)
        self.layout_stk_general.setContentsMargins(QMargins(0, 0, 0, 0))
        self.layout_stk_numbers.addWidget(self.lbl_stk_numbers)
        self.layout_stk_numbers.addWidget(self.tab_numbers)
        self.layout_stk_numbers.setContentsMargins(QMargins(0, 0, 0, 0))

        self.stk_general.setLayout(self.layout_stk_general)
        self.stk_numbers.setLayout(self.layout_stk_numbers)

    def setup_tab_replace(self):
        self.grp_replace = QGroupBox('Find && Replace', self.tab_replace)
        self.layout_gen_replace = QGridLayout()
        self.layout_tab_replace = QVBoxLayout()
        tab_replace_spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.lbl_find = QLabel('Find:', self.grp_replace)
        self.txt_find = QLineEdit(self.grp_replace)
        self.lbl_replace = QLabel('Replace:', self.grp_replace)
        self.txt_replace = QLineEdit(self.grp_replace)
        self.lbl_skip = QLabel('Skip:', self.grp_replace)
        self.spn_skip = QSpinBox(self.grp_replace)
        self.lbl_max = QLabel('Max:', self.grp_replace)
        self.spn_max_swap = QSpinBox(self.grp_replace)
        self.chk_sensetive = QCheckBox('Case sensitive', self.grp_replace)
        self.chk_swap = QCheckBox('Swap mode', self.grp_replace)
        self.chk_regex = QCheckBox('RegEx', self.grp_replace)

        self.spn_skip.setAlignment(QtCore.Qt.AlignRight)
        self.spn_skip.setMaximumWidth(100)
        self.spn_max_swap.setAlignment(QtCore.Qt.AlignRight)
        self.spn_max_swap.setMaximumWidth(100)

        self.layout_gen_replace.addWidget(self.lbl_find, 0, 0, 1, 4)
        self.layout_gen_replace.addWidget(self.txt_find, 1, 0, 1, 4)
        self.layout_gen_replace.addWidget(self.lbl_replace, 2, 0, 1, 4)
        self.layout_gen_replace.addWidget(self.txt_replace, 3, 0, 1, 4)
        self.layout_gen_replace.addWidget(self.lbl_skip, 4, 0, 1, 1)
        self.layout_gen_replace.addWidget(self.spn_skip, 4, 1, 1, 1)
        self.layout_gen_replace.addWidget(self.lbl_max, 4, 2, 1, 1)
        self.layout_gen_replace.addWidget(self.spn_max_swap, 4, 3, 1, 1)
        self.layout_gen_replace.addWidget(self.chk_sensetive, 5, 0, 1, 4)
        self.layout_gen_replace.addWidget(self.chk_swap, 6, 0, 1, 4)
        self.layout_gen_replace.addWidget(self.chk_regex, 7, 0, 1, 4)

        self.grp_replace.setLayout(self.layout_gen_replace)

        self.layout_tab_replace.addWidget(self.grp_replace)
        self.layout_tab_replace.addSpacerItem(tab_replace_spacer)

        self.tab_replace.setLayout(self.layout_tab_replace)

        self.grp_replace.setFont(set_bold(True))
        self.set_font_weight(self.grp_replace)

    def setup_tab_casing(self):
        self.grp_case_ext = QGroupBox('Extension', self.tab_casing)
        self.grp_case_file = QGroupBox('Filename', self.tab_casing)
        self.grp_case_options = QGroupBox('Options', self.tab_casing)
        self.layout_case_file = QGridLayout()
        self.layout_case_ext = QGridLayout()
        self.layout_case_options = QVBoxLayout()
        self.layout_tab_case = QVBoxLayout()
        tab_case_spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.rdb_cupper_ext = QRadioButton('Upper Case', self.grp_case_ext)
        self.rdb_csame_ext = QRadioButton('Same Case', self.grp_case_ext)
        self.rdb_clower_ext = QRadioButton('Lower Case', self.grp_case_ext)
        self.rdb_cinvert_ext = QRadioButton('Invert Case', self.grp_case_ext)
        self.rdb_ctitle_ext = QRadioButton('Title Case', self.grp_case_ext)
        self.rdb_crandom_ext = QRadioButton('Random Case', self.grp_case_ext)

        self.rdb_cupper_file = QRadioButton('Upper Case', self.grp_case_file)
        self.rdb_csame_file = QRadioButton('Same Case', self.grp_case_file)
        self.rdb_clower_file = QRadioButton('Lower Case', self.grp_case_file)
        self.rdb_cinvert_file = QRadioButton('Invert Case', self.grp_case_file)
        self.rdb_csentence_file = QRadioButton('Sentence Case', self.grp_case_file)
        self.rdb_crandom_file = QRadioButton('Random Case', self.grp_case_file)
        self.rdb_ctitle_file = QRadioButton('Title Case', self.grp_case_file)

        self.chk_ignore_upper = QCheckBox('Ignore all upper case words', self.grp_case_options)
        self.chk_ignore_mixed = QCheckBox('Ignore mixed case words', self.grp_case_options)

        self.rdb_csame_ext.setChecked(True)
        self.rdb_csame_file.setChecked(True)

        self.layout_case_file.addWidget(self.rdb_cupper_file, 0, 0, 1, 1)
        self.layout_case_file.addWidget(self.rdb_csame_file, 0, 1, 1, 1)
        self.layout_case_file.addWidget(self.rdb_clower_file, 1, 0, 1, 1)
        self.layout_case_file.addWidget(self.rdb_cinvert_file, 1, 1, 1, 1)
        self.layout_case_file.addWidget(self.rdb_csentence_file, 2, 0, 1, 1)
        self.layout_case_file.addWidget(self.rdb_crandom_file, 2, 1, 1, 1)
        self.layout_case_file.addWidget(self.rdb_ctitle_file, 3, 0, 1, 1)
        self.grp_case_file.setLayout(self.layout_case_file)

        self.layout_case_ext.addWidget(self.rdb_cupper_ext, 0, 0, 1, 1)
        self.layout_case_ext.addWidget(self.rdb_csame_ext, 0, 1, 1, 1)
        self.layout_case_ext.addWidget(self.rdb_clower_ext, 1, 0, 1, 1)
        self.layout_case_ext.addWidget(self.rdb_cinvert_ext, 1, 1, 1, 1)
        self.layout_case_ext.addWidget(self.rdb_ctitle_ext, 2, 0, 1, 1)
        self.layout_case_ext.addWidget(self.rdb_crandom_ext, 2, 1, 1, 1)
        self.grp_case_ext.setLayout(self.layout_case_ext)

        self.layout_case_options.addWidget(self.chk_ignore_upper)
        self.layout_case_options.addWidget(self.chk_ignore_mixed)
        self.grp_case_options.setLayout(self.layout_case_options)

        self.layout_tab_case.addWidget(self.grp_case_file)
        self.layout_tab_case.addWidget(self.grp_case_ext)
        self.layout_tab_case.addWidget(self.grp_case_options)
        self.layout_tab_case.addSpacerItem(tab_case_spacer)

        self.tab_casing.setLayout(self.layout_tab_case)

        self.grp_case_file.setFont(set_bold(True))
        self.grp_case_ext.setFont(set_bold(True))
        self.grp_case_options.setFont(set_bold(True))

        self.set_font_weight(self.grp_case_file)
        self.set_font_weight(self.grp_case_ext)
        self.set_font_weight(self.grp_case_options)

    def setup_tab_add_remove(self):
        self.grp_add = QGroupBox('Add', self.tab_add_remove)
        self.grp_remove = QGroupBox('Remove', self.tab_add_remove)
        self.layout_addrem_add = QGridLayout()
        self.layout_addrem_rem = QGridLayout()
        self.layout_tab_addrem = QVBoxLayout()
        tab_addrem_spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.lbl_insert = QLabel('Insert', self.grp_add)
        self.txt_insert = QLineEdit(self.grp_add)
        self.chk_overwrite = QCheckBox('Overwrite', self.grp_add)
        self.lbl_at_add = QLabel('Starting at', self.grp_add)
        self.chk_backw_add = QCheckBox('Backwards', self.grp_add)
        self.spn_at_add = QSpinBox(self.grp_add)
        self.lbl_delete = QLabel('Delete', self.grp_remove)
        self.lbl_at_del = QLabel('Starting at', self.grp_remove)
        self.chk_backw_del = QCheckBox('Backwards', self.grp_remove)
        self.spn_del = QSpinBox(self.grp_remove)
        self.spn_at_del = QSpinBox(self.grp_remove)
        self.chk_add_remove = QCheckBox('Remove then add', self.tab_add_remove)

        self.grp_add.setCheckable(True)
        self.grp_add.setChecked(False)
        self.spn_at_add.setMinimum(0)
        self.spn_at_add.setAlignment(QtCore.Qt.AlignRight)
        self.spn_at_add.setMaximumWidth(100)
        self.grp_remove.setCheckable(True)
        self.grp_remove.setChecked(False)
        self.spn_at_del.setMinimum(0)
        self.spn_at_del.setAlignment(QtCore.Qt.AlignRight)
        self.spn_at_del.setMaximumWidth(100)
        self.spn_del.setMinimum(1)
        self.spn_del.setAlignment(QtCore.Qt.AlignRight)
        self.spn_del.setMaximumWidth(100)

        self.layout_addrem_add.addWidget(self.lbl_insert, 0, 0, 1, 1)
        self.layout_addrem_add.addWidget(self.txt_insert, 0, 1, 1, 1)
        self.layout_addrem_add.addWidget(self.lbl_at_add, 1, 0, 1, 1)
        self.layout_addrem_add.addWidget(self.spn_at_add, 1, 1, 1, 1)
        self.layout_addrem_add.addWidget(self.chk_overwrite, 2, 0, 1, 2)
        self.layout_addrem_add.addWidget(self.chk_backw_add, 3, 0, 1, 2)

        self.grp_add.setLayout(self.layout_addrem_add)

        self.layout_addrem_rem.addWidget(self.lbl_delete, 0, 0, 1, 1)
        self.layout_addrem_rem.addWidget(self.spn_del, 0, 1, 1, 1)
        self.layout_addrem_rem.addWidget(self.lbl_at_del, 1, 0, 1, 1)
        self.layout_addrem_rem.addWidget(self.spn_at_del, 1, 1, 1, 1)
        self.layout_addrem_rem.addWidget(self.chk_backw_del, 2, 0, 1, 2)

        self.grp_remove.setLayout(self.layout_addrem_rem)

        self.layout_tab_addrem.addWidget(self.grp_add)
        self.layout_tab_addrem.addWidget(self.grp_remove)
        self.layout_tab_addrem.addWidget(self.chk_add_remove)
        self.layout_tab_addrem.addSpacerItem(tab_addrem_spacer)

        self.tab_add_remove.setLayout(self.layout_tab_addrem)

        self.grp_add.setFont(set_bold(True))
        self.grp_remove.setFont(set_bold(True))

        self.set_font_weight(self.grp_add)
        self.set_font_weight(self.grp_remove)

    def setup_tab_move(self):
        self.grp_move_move = QGroupBox('Move', self.tab_move)
        self.grp_move_to = QGroupBox('To', self.tab_move)
        self.layout_move_move = QGridLayout()
        self.layout_move_to = QGridLayout()
        self.layout_tab_move = QVBoxLayout()
        self.lbl_move = QLabel('Move', self.tab_move)
        self.spn_move = QSpinBox(self.tab_move)
        self.lbl_move_from = QLabel('From position', self.tab_move)
        self.spn_move_from = QSpinBox(self.tab_move)
        self.chk_backw_move = QCheckBox('Backwards', self.tab_move)
        self.lbl_to_move = QLabel('To position', self.tab_move)
        self.spn_to_pos = QSpinBox(self.tab_move)
        self.chk_backw_to = QCheckBox('Backwards', self.tab_move)
        self.chk_relative = QCheckBox('Relative to starting point', self.tab_move)
        tab_move_spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.spn_move_from.setAlignment(QtCore.Qt.AlignRight)
        self.spn_move_from.setMaximumWidth(100)
        self.spn_to_pos.setAlignment(QtCore.Qt.AlignRight)
        self.spn_to_pos.setMaximumWidth(100)
        self.spn_move.setMinimum(0)
        self.spn_move.setAlignment(QtCore.Qt.AlignRight)
        self.spn_move.setMaximumWidth(100)

        self.layout_move_move.addWidget(self.lbl_move, 0, 0, 1, 1)
        self.layout_move_move.addWidget(self.spn_move, 0, 1, 1, 1)
        self.layout_move_move.addWidget(self.lbl_move_from, 1, 0, 1, 1)
        self.layout_move_move.addWidget(self.spn_move_from, 1, 1, 1, 1)
        self.layout_move_move.addWidget(self.chk_backw_move, 2, 0, 1, 2)

        self.grp_move_move.setLayout(self.layout_move_move)

        self.layout_move_to.addWidget(self.lbl_to_move, 0, 0, 1, 1)
        self.layout_move_to.addWidget(self.spn_to_pos, 0, 1, 1, 1)
        self.layout_move_to.addWidget(self.chk_backw_to, 1, 0, 1, 2)
        self.layout_move_to.addWidget(self.chk_relative, 2, 0, 1, 2)

        self.grp_move_to.setLayout(self.layout_move_to)

        self.layout_tab_move.addWidget(self.grp_move_move)
        self.layout_tab_move.addWidget(self.grp_move_to)
        self.layout_tab_move.addSpacerItem(tab_move_spacer)

        self.tab_move.setLayout(self.layout_tab_move)

        self.grp_move_move.setFont(set_bold(True))
        self.grp_move_to.setFont(set_bold(True))

        self.set_font_weight(self.grp_move_move)
        self.set_font_weight(self.grp_move_to)

    def setup_tab_spaces(self):
        self.grp_trim = QGroupBox('Trim', self.tab_spaces)
        self.grp_maintain = QGroupBox('Maintain', self.tab_spaces)
        self.grp_customized = QGroupBox('Customized', self.tab_spaces)
        self.layout_spaces_trim = QVBoxLayout()
        self.layout_spaces_maintain = QGridLayout()
        self.layout_spaces_customized = QGridLayout()
        self.layout_tab_spaces = QVBoxLayout()
        tab_spaces_spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.chk_leading = QCheckBox('Leading Spaces', self.grp_trim)
        self.chk_trailing = QCheckBox('Trailing Spaces', self.grp_trim)
        self.chk_many_one = QCheckBox('Multiple spaces', self.grp_trim)
        self.rdb_x_chars = QRadioButton('Replace', self.grp_customized)
        self.rdb_one_char = QRadioButton('Replace', self.grp_customized)
        self.lbl_x_chars = QLabel('with spaces', self.grp_customized)
        self.lbl_one_char = QLabel('with 1 space', self.grp_customized)
        self.txt_x_chars = QLineEdit(self.grp_customized)
        self.txt_one_char = QLineEdit(self.grp_customized)
        self.chk_maintain_before = QCheckBox('Before', self.grp_maintain)
        self.chk_maintain_after = QCheckBox('After', self.grp_maintain)
        self.txt_maintain_before = QLineEdit(self.grp_maintain)
        self.txt_maintain_after = QLineEdit(self.grp_maintain)

        self.txt_x_chars.setEnabled(False)
        self.txt_x_chars.setMaxLength(1)
        self.txt_one_char.setEnabled(False)
        self.txt_one_char.setMaxLength(1)
        self.txt_maintain_before.setEnabled(False)
        self.txt_maintain_after.setEnabled(False)

        self.layout_spaces_trim.addWidget(self.chk_leading)
        self.layout_spaces_trim.addWidget(self.chk_trailing)
        self.layout_spaces_trim.addWidget(self.chk_many_one)
        self.grp_trim.setLayout(self.layout_spaces_trim)

        self.layout_spaces_maintain.addWidget(self.chk_maintain_before, 0, 0)
        self.layout_spaces_maintain.addWidget(self.txt_maintain_before, 0, 1)
        self.layout_spaces_maintain.addWidget(self.chk_maintain_after, 1, 0)
        self.layout_spaces_maintain.addWidget(self.txt_maintain_after, 1, 1)
        self.grp_maintain.setLayout(self.layout_spaces_maintain)

        self.layout_spaces_customized.addWidget(self.rdb_x_chars, 0, 0)
        self.layout_spaces_customized.addWidget(self.txt_x_chars, 0, 1)
        self.layout_spaces_customized.addWidget(self.lbl_x_chars, 0, 2)
        self.layout_spaces_customized.addWidget(self.rdb_one_char, 1, 0)
        self.layout_spaces_customized.addWidget(self.txt_one_char, 1, 1)
        self.layout_spaces_customized.addWidget(self.lbl_one_char, 1, 2)

        self.grp_customized.setLayout(self.layout_spaces_customized)

        self.layout_tab_spaces.setContentsMargins(QMargins(5, 5, 5, 5))
        self.layout_tab_spaces.addWidget(self.grp_trim)
        self.layout_tab_spaces.addWidget(self.grp_maintain)
        self.layout_tab_spaces.addWidget(self.grp_customized)
        self.layout_tab_spaces.addSpacerItem(tab_spaces_spacer)

        self.tab_spaces.setLayout(self.layout_tab_spaces)

        self.grp_trim.setFont(set_bold(True))
        self.grp_maintain.setFont(set_bold(True))
        self.grp_customized.setFont(set_bold(True))

        self.set_font_weight(self.grp_trim)
        self.set_font_weight(self.grp_maintain)
        self.set_font_weight(self.grp_customized)

    def setup_tab_counter(self):
        self.grp_counter = QGroupBox('Counter', self.tab_counter)
        self.layout_counter = QGridLayout()
        self.layout_tab_counter = QVBoxLayout()
        tab_counter_spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.txt_replace_name = QLineEdit(self.grp_counter)
        self.txt_separator = QLineEdit(self.grp_counter)
        self.lbl_separator = QLabel('Separator', self.grp_counter)
        self.rdb_keep_name = QRadioButton('Keep filename', self.grp_counter)
        self.lbl_counter = QLabel('Counter', self.grp_counter)
        self.cmb_counter = QComboBox(self.grp_counter)
        self.rdb_replace_name = QRadioButton('Replace filename', self.grp_counter)

        self.rdb_keep_name.setChecked(True)
        self.cmb_counter.addItems(qtrename.counters.lst_counter)
        self.cmb_counter.setCurrentIndex(0)
        self.layout_counter.addWidget(self.lbl_counter, 0, 0, 1, 1)
        self.layout_counter.addWidget(self.cmb_counter, 0, 1, 1, 1)
        self.layout_counter.addWidget(self.lbl_separator, 1, 0, 1, 1)
        self.layout_counter.addWidget(self.txt_separator, 1, 1, 1, 1)
        self.layout_counter.addWidget(self.rdb_keep_name, 2, 0, 1, 2)
        self.layout_counter.addWidget(self.rdb_replace_name, 3, 0, 1, 1)
        self.layout_counter.addWidget(self.txt_replace_name, 3, 1, 1, 1)
        self.grp_counter.setLayout(self.layout_counter)

        self.grp_counter.setFont(set_bold(True))

        self.set_font_weight(self.grp_counter)

        self.layout_tab_counter.addWidget(self.grp_counter)
        self.layout_tab_counter.addSpacerItem(tab_counter_spacer)

        self.tab_counter.setLayout(self.layout_tab_counter)

    def setup_tab_renumber(self):
        self.grp_renum_gen = QGroupBox('Enumerate', self.tab_renumber)
        self.grp_enumerate = QGridLayout(self.grp_renum_gen)
        self.layout_tab_renumber = QVBoxLayout()
        tab_renumber_spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.lbl_start_enum = QLabel('Start from', self.grp_renum_gen)
        self.spn_start_enum = QSpinBox(self.grp_renum_gen)
        self.lbl_step = QLabel('Step', self.grp_renum_gen)
        self.spn_step = QSpinBox(self.grp_renum_gen)
        self.chk_padding = QCheckBox('Zero padding', self.grp_renum_gen)
        self.txt_sep_enum = QLineEdit(self.grp_renum_gen)
        self.lbl_sep_enum = QLabel('Separator', self.grp_renum_gen)

        self.spn_start_enum.setMaximum(99999999)
        self.spn_start_enum.setMinimum(0)
        self.spn_start_enum.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.spn_step.setMaximum(99999999)
        self.spn_step.setMinimum(1)
        self.spn_step.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.grp_enumerate.addWidget(self.lbl_start_enum, 0, 0, 1, 1)
        self.grp_enumerate.addWidget(self.spn_start_enum, 0, 1, 1, 1)
        self.grp_enumerate.addWidget(self.lbl_step, 1, 0, 1, 1)
        self.grp_enumerate.addWidget(self.spn_step, 1, 1, 1, 1)
        self.grp_enumerate.addWidget(self.lbl_sep_enum, 2, 0, 1, 1)
        self.grp_enumerate.addWidget(self.txt_sep_enum, 2, 1, 1, 1)
        self.grp_enumerate.addWidget(self.chk_padding, 3, 0, 1, 1)

        self.grp_renum_gen.setLayout(self.grp_enumerate)

        self.grp_renum_gen.setFont(set_bold(True))

        self.set_font_weight(self.grp_renum_gen)

        self.layout_tab_renumber.addWidget(self.grp_renum_gen)
        self.layout_tab_renumber.addSpacerItem(tab_renumber_spacer)

        self.tab_renumber.setLayout(self.layout_tab_renumber)

    def set_font_weight(self, widget):
        for child in widget.children():
            try:
                child.setFont(set_bold(False))
            except:
                continue

    def resize_buttons(self):
        left = self.tab_counter.width() if self.stacked_tabs.currentIndex() else self.tab_replace.width()
        top = self.options_group.height()

        self.btn_rename.move(left - 120, top + 10)
        self.stk_next.move(left + 10, top + 10)
        self.stk_previous.move(left - 22, top + 10)

    def set_theme(self, theme, tone = ''):

        if theme == 'default':
            palette = QApplication.style().standardPalette()
            return (palette, (theme, tone))


        elif theme == 'dark':
            palette = QPalette()

            for color in dark_theme.keys():
                for item in dark_theme[color][1:]:
                    palette.setColor(item, dark_theme[color][0])

            palette.setColor(QPalette.Base, BASE_DARK)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, dict_tones[tone][1])
            palette.setColor(QPalette.Highlight, dict_tones[tone][0])

            palette.setColor(QPalette.Disabled, QPalette.Text, DISABLED_DARK)
            palette.setColor(QPalette.Disabled, QPalette.WindowText, DISABLED_DARK)
            palette.setColor(QPalette.Disabled, QPalette.ButtonText, DISABLED_DARK)

            return (palette, (theme, tone))

    @pyqtSlot(int)
    def enable_swap(self, state):
        pass

    @pyqtSlot(int)
    def enable_regex(self, state):
        pass

    @pyqtSlot(int)
    def on_tab_gen_changed(self, index):
        pass

    @pyqtSlot(int)
    def on_tab_nums_changed(self, index):
        pass

    def theme_selector(self, action):
        pass

    @pyqtSlot()
    def previous_stacked_page(self):
        pass

    @pyqtSlot()
    def next_stacked_page(self):
        pass

    @pyqtSlot()
    def get_dir(self):
        pass

    @pyqtSlot()
    def on_rename_clicked(self):
        pass

    @pyqtSlot()
    def level_up(self):
        pass

    @pyqtSlot()
    def list_content(self):
        pass

    @pyqtSlot()
    def check_field(self):
        pass

    @pyqtSlot(QModelIndex)
    def open_dir(self, model_index: QModelIndex):
        pass

    @pyqtSlot(list)
    def on_selection_changed(self, lst):
        pass



    @pyqtSlot()
    def set_file_case(self):
        pass


    @pyqtSlot()
    def set_ext_case(self):
        pass


    @pyqtSlot()
    def switch_mixed(self):
        pass

    @pyqtSlot()
    def switch_upper(self):
        pass


    @pyqtSlot()
    def preview_general_replace(self):
        pass

    @pyqtSlot()
    def check_options(self):
        pass


    @pyqtSlot(int)
    def on_addrem_changed(self, state):
        pass

    @pyqtSlot(bool)
    def on_grp_add_toggled(self, checked):
        pass

    @pyqtSlot(bool)
    def on_grp_rem_toggled(self, checked):
        pass

    @pyqtSlot()
    def preview_general_addrem(self):
        pass


    @pyqtSlot()
    def preview_general_move(self):
        pass


    @pyqtSlot()
    def preview_general_spaces(self):
        pass

    @pyqtSlot()
    def on_maintain_before_checked(self):
        pass

    @pyqtSlot()
    def on_maintain_after_checked(self):
        pass

    @pyqtSlot()
    def on_x_chars_toggled(self):
        pass

    @pyqtSlot()
    def on_one_char_toggled(self):
        pass


    @pyqtSlot()
    def preview_numbers_counter(self):
        pass

    @pyqtSlot()
    def on_replace_name_toggled(self):
        pass


    @pyqtSlot()
    def preview_numbers_renumber(self):
        pass

    @pyqtSlot()
    def set_files(self):
        pass

    @pyqtSlot()
    def set_dirs(self):
        pass

    @pyqtSlot()
    def set_sub_dirs(self):
        pass

    @pyqtSlot()
    def set_process_name(self):
        pass

    @pyqtSlot(QAction)
    def process_trigger(self, menu_action: QAction):
        pass
