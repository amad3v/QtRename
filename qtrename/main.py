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
##############################################################################

import sys

from PyQt5.QtCore import (
    QtFatalMsg, QtCriticalMsg, QRect, QThreadPool, pyqtSlot,
    QTranslator, QEvent, QCoreApplication, pyqtSignal, Qt, QDir, qInstallMessageHandler
)
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import (QCompleter, QFileSystemModel, qApp, QFileDialog, QMessageBox, QApplication, QAction)

from qtrename import counters
from qtrename.About import About
from qtrename.Animation import Animation
from qtrename.TableView import DataSource
from qtrename.Theme import Settings
from qtrename.add_remove import add_remove_chars
from qtrename.common import *
from qtrename.mainwindow import MainWindow
from qtrename.preview import *
from qtrename.worker import Worker

app = QApplication(sys.argv)
translator = QTranslator()
tr_ = QCoreApplication.translate

if os_type == 'Windows':
    import ctypes

    app_id = 'amad3v.qtrename.qtrename'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)


class QtRename(MainWindow):
    done_clearing = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.data_source = DataSource(self)
        self.table_model = QStandardItemModel(self)
        self.thread_pool = QThreadPool(self)
        self.thread_pool.setMaxThreadCount(1)
        self.completer = QCompleter(self)
        self.fsm = QFileSystemModel(self.completer)
        self.settings = Settings('.config/qtrename')
        self.animation = Animation(self, animation_tones[self.theme_name[1]][0],
                                   QRect(0, 0, self.width(), self.height()),
                                   animation_tones[self.theme_name[1]][1])
        self.curr_lang = 'en'
        self.swap_enabled = False
        self.tab_preview_func = {
            (0, 0): self.preview_general_replace,
            (0, 1): self.preview_general_casing,
            (0, 2): self.preview_general_addrem,
            (0, 3): self.preview_general_move,
            (0, 4): self.preview_general_spaces,
            (1, 0): self.preview_numbers_counter,
            (1, 1): self.preview_numbers_renumber
        }
        self.is_case_sensitive = {True: 0, False: re.I}
        self.view_selection = []
        self.process_name = ProcessName.FILENAME
        self.flags = QDirIterator.NoIteratorFlags
        self.animation_on = False
        self.current_tab = (0, 0)
        self.file_case = 'same'
        self.ext_case = 'same'
        self.func_args = None
        self.filter_files = True
        self.filter_dirs = False
        self.addrem_func_args = {
            'insert': '',
            'add_num': 0,
            'overwrite': False,
            'backw_add': False,
            'delete': 0,
            'delete_at': 0,
            'backw_del': False,
            'del_chars': False,
            'both_ops': False,
            'to_process': self.process_name
        }
        self.app_icon = QPixmap(":/qtrenamer/imgs/app_icon")
        self.app_title = 'QtRename 1.1.1'
        self.app_description = self.tr(self.about_desc)
        self.app_link = 'https://github.com/amad3v/QtRename'
        self.stacked_index = 0
        self.regex_enabled = False
        self.current_path = str(path_func.home())
        self.ext_filters = self.txt_filter_ext.text()
        self.filter_ext = '*.*'
        self.run_once = -1
        self.actions = {
            'exit': qApp.quit,
            'clear': self.clear_selection,
            'about': self.show_about,
            'about_qt': QApplication.instance().aboutQt,
            'undo': self.undo_renaming,
            'rename': self.rename_items,
            'errors': self.show_errors
        }
        self.fetcher_busy = False

        self.setup_models()
        self.setup_defaults()
        self.setup_slots()
        self.list_content()

    def setup_defaults(self):
        self.table_model.setHorizontalHeaderLabels((self.before, self.after, '', ''))
        self.lst_loaded_files.setModel(self.table_model)
        self.txt_load_path.setCompleter(self.completer)
        self.txt_load_path.setText(self.current_path)

    def setup_models(self):
        self.fsm.setRootPath(root_dir[os_type])
        self.fsm.setFilter(QDir.NoDotAndDotDot | QDir.Dirs)
        self.completer.setModel(self.fsm)
        self.completer.setCaseSensitivity(False)
        self.completer.setMaxVisibleItems(5)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setFilterMode(Qt.MatchContains)

    def setup_slots(self):
        super().setup_slots()
        self.data_source.reset_model.connect(self.empty_model)
        self.data_source.update_row.connect(self.update_model)
        self.data_source.update_item.connect(self.table_model.setItem)
        self.done_clearing.connect(self.data_source.ready_to_load)
        self.timer.timeout.connect(self.animation.movie_start)

    def show_about(self):
        About(self, self.app_icon, self.app_title, self.tr(self.about_desc),
              self.app_link, self.about_warning, self.about_license).exec_()

    def theme_setter(self, action):
        new_theme = self.set_theme(*dict_slots[action.data()])
        palette = new_theme[0]
        self.theme_name = new_theme[1]
        theme_wrapper(palette)
        self.animation.setup_animation(animation_tones[self.theme_name[1]][0], animation_tones[self.theme_name[1]][1])

    def load_data(self):
        self.data_source.setup_data_source(
            self.current_path,
            self.filter_ext.split(','),
            self.filter_files,
            self.filter_dirs,
            self.flags,
            self.func_args,
            self.process_name
        )
        self.start_animation()
        self.start_worker(self.data_source.start_collector, self.on_done_collecting)

    def start_worker(self, main_func, finish_func=None, args=None):
        ops_worker = Worker(main_func, args)
        ops_worker.signals.done.connect(finish_func)
        self.thread_pool.start(ops_worker)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.lst_loaded_files.resizeEvent(event)
        self.animation.setGeometry(QRect(0, 0, event.size().width(), event.size().height()))

    def current_options(self):
        if not self.stacked_index:
            self.tab_preview_func[(0, self.tab_general.currentIndex())]()
        else:
            self.tab_preview_func[(1, self.tab_numbers.currentIndex())]()

    def undo_renaming(self):
        self.action_undo.setEnabled(False)
        self.start_animation()
        self.start_worker(undo_rename, self.list_content)

    def rename_items(self):
        self.action_undo.setEnabled(True)
        self.start_animation()
        self.start_worker(self.data_source.rename_files, self.list_content, (self.get_selected_rows, rename_items))

    def on_selection_changed(self, lst):
        self.view_selection = lst
        self.tab_preview_func[self.current_tab]()

    def start_animation(self):
        if not self.animation_on:
            self.animation_on = True
            self.timer.start()
            self.fetcher_busy = True
            self.update_status()

    def validate_filter(self):
        if self.filter_ext == self.txt_filter_ext.text(): return
        self.filter_ext = get_filter(self.txt_filter_ext.text())

        if self.filter_ext == '*':
            self.txt_filter_ext.setText('*.*')
        else:
            self.txt_filter_ext.setText(self.filter_ext)

        self.list_content()

    def set_processing_options(self):
        self.process_name = dict_process[(self.chk_process_name.isChecked(), self.chk_process_ext.isChecked())]
        if self.txt_load_path.text(): self.current_options()

    def set_include_files(self):
        self.filter_files = self.chk_file_in.isChecked()
        if self.txt_load_path.text(): self.load_data()

    def set_include_dirs(self):
        self.filter_dirs = self.chk_dirs_in.isChecked()
        if self.txt_load_path.text(): self.load_data()

    def set_include_subdirs(self):
        self.flags = flags_dict[self.chk_subdirs_in.isChecked()]
        if self.txt_load_path.text(): self.load_data()

    def menu_trigger(self, menu_action):
        menu_action_label = str(menu_action.data())
        if menu_action_label in self.actions:
            self.actions[menu_action_label]()

    def check_regex(self, to_find):
        if self.regex_enabled:
            try:
                re.compile(to_find, self.is_case_sensitive[self.chk_sensetive.isChecked()])
            except re.error:
                return False

        return True

    def preview_general_replace(self):
        self.start_animation()
        to_find = self.txt_find.text()

        if not self.check_regex(to_find):
            to_find = ''

        skip = 0 if self.swap_enabled or self.regex_enabled else self.spn_skip.value()

        fun_args = (
            self.get_selected_rows,
            get_preview_replace,
            self.process_name,
            to_find,
            self.txt_replace.text(),
            skip,
            self.spn_max_swap.value(),
            self.chk_swap.isChecked(),
            self.is_case_sensitive[self.chk_sensetive.isChecked()],
            self.regex_enabled
        )

        self.start_worker(self.data_source.load_preview, self.stop_animation, fun_args)

    def preview_general_casing(self):
        self.start_animation()

        if self.chk_ignore_upper.isChecked():
            keep_option = 'upper'
        elif self.chk_ignore_mixed.isChecked():
            keep_option = 'mixed'
        else:
            keep_option = ''

        fun_args = (
            self.get_selected_rows,
            get_preview_casing,
            self.file_case,
            self.ext_case,
            keep_option
        )

        self.start_worker(self.data_source.load_preview, self.stop_animation, fun_args)

    def preview_general_addrem(self):
        self.start_animation()
        self.add_chars()
        self.remove_chars()
        self.addrem_chars()
        self.addrem_func_args['to_process'] = self.process_name

        fun_args = (self.get_selected_rows, add_remove_chars, self.addrem_func_args)
        self.start_worker(self.data_source.load_preview, self.stop_animation, fun_args)

    def preview_general_move(self):
        self.start_animation()

        fun_args = (
            self.get_selected_rows,
            get_preview_move,
            self.process_name,
            int(self.spn_move_from.value()),
            int(self.spn_move.value()),
            self.chk_backw_move.isChecked(),
            int(self.spn_to_pos.value()),
            self.chk_backw_to.isChecked(),
            self.chk_relative.isChecked()
        )

        self.start_worker(self.data_source.load_preview, self.stop_animation, fun_args)

    def preview_general_spaces(self):
        self.start_animation()

        fun_args = (
            self.get_selected_rows,
            get_preview_spaces,
            self.process_name,
            self.chk_leading.isChecked(),
            self.chk_trailing.isChecked(),
            self.chk_many_one.isChecked(),
            self.chk_maintain_before.isChecked(),
            self.txt_maintain_before.text(),
            self.chk_maintain_after.isChecked(),
            self.txt_maintain_after.text(),
            self.rdb_x_chars.isChecked(),
            self.rdb_one_char.isChecked(),
            self.txt_x_chars.text(),
            self.txt_one_char.text()
        )

        self.start_worker(self.data_source.load_preview, self.stop_animation, fun_args)

    def preview_numbers_counter(self):
        self.start_animation()
        func_args = (
            self.get_selected_rows,
            get_preview_counter,
            self.process_name,
            self.cmb_counter.currentIndex(),
            self.txt_separator.text(),
            self.rdb_keep_name.isChecked(),
            self.txt_replace_name.text()
        )

        self.start_worker(self.data_source.load_preview, self.stop_animation, func_args)

    def preview_numbers_renumber(self):
        self.start_animation()

        counters.p_enumerate = int(self.spn_start_enum.value())

        func_args = (
            self.get_selected_rows,
            get_preview_renumber,
            self.process_name,
            int(self.spn_start_enum.value()),
            int(self.spn_step.value()),
            self.txt_sep_enum.text(),
            self.chk_padding.isChecked(),
            self.table_model.rowCount()
        )

        self.start_worker(self.data_source.load_preview, self.on_num_renumber_finished, func_args)

    def set_case_status(self):
        if not self.chk_ignore_mixed.isChecked() and not self.chk_ignore_upper.isChecked():
            self.run_once = -1

    def switch_upper(self):
        if self.chk_ignore_upper.isChecked() and self.run_once != 0:
            self.run_once = 0
            self.chk_ignore_mixed.setChecked(False)

        self.set_case_status()
        self.set_file_case()

    def switch_mixed(self):
        if self.chk_ignore_mixed.isChecked() and self.run_once != 1:
            self.chk_ignore_upper.setChecked(False)
            self.run_once = 1

        self.set_case_status()
        self.set_file_case()

    def set_file_case(self):
        if self.rdb_cupper_file.isChecked():
            self.file_case = 'upper'
        elif self.rdb_clower_file.isChecked():
            self.file_case = 'lower'
        elif self.rdb_csentence_file.isChecked():
            self.file_case = 'sentence'
        elif self.rdb_ctitle_file.isChecked():
            self.file_case = 'title'
        elif self.rdb_csame_file.isChecked():
            self.file_case = 'same'
        elif self.rdb_cinvert_file.isChecked():
            self.file_case = 'invert'
        elif self.rdb_crandom_file.isChecked():
            self.file_case = 'random'

        self.animation_on = True
        self.preview_general_casing()

    def set_ext_case(self):
        if self.rdb_cupper_ext.isChecked():
            self.ext_case = 'upper'
        elif self.rdb_clower_ext.isChecked():
            self.ext_case = 'lower'
        elif self.rdb_ctitle_ext.isChecked():
            self.ext_case = 'title'
        elif self.rdb_csame_ext.isChecked():
            self.ext_case = 'same'
        elif self.rdb_cinvert_ext.isChecked():
            self.ext_case = 'invert'
        elif self.rdb_crandom_ext.isChecked():
            self.ext_case = 'random'

        self.animation_on = True
        self.preview_general_casing()

    def on_addrem_changed(self, state):
        if state == 2:
            self.grp_add.setCheckable(False)
            self.grp_remove.setCheckable(False)
        else:
            self.grp_add.setCheckable(True)
            self.grp_remove.setCheckable(True)
            self.grp_add.setChecked(True)
            self.grp_remove.setChecked(False)

        self.animation_on = True
        self.preview_general_addrem()

    def on_grp_add_toggled(self, checked):
        self.grp_remove.setChecked(not checked)

        self.animation_on = True
        self.preview_general_addrem()

    def on_grp_rem_toggled(self, checked):
        self.grp_add.setChecked(not checked)
        self.animation_on = True
        self.preview_general_addrem()

    def add_chars(self):
        if not self.txt_insert.isEnabled():
            self.addrem_func_args['insert'] = ''
            self.addrem_func_args['add_num'] = 0
            self.addrem_func_args['overwrite'] = False
            self.addrem_func_args['backw_add'] = False
        else:
            self.addrem_func_args['insert'] = self.txt_insert.text()
            self.addrem_func_args['add_num'] = self.spn_at_add.value()
            self.addrem_func_args['overwrite'] = self.chk_overwrite.isChecked()
            self.addrem_func_args['backw_add'] = self.chk_backw_add.isChecked()

    def remove_chars(self):
        if not self.spn_del.isEnabled():
            self.addrem_func_args['delete'] = 0
            self.addrem_func_args['delete_at'] = 0
            self.addrem_func_args['del_chars'] = False
            self.addrem_func_args['backw_del'] = False
        else:
            self.addrem_func_args['delete'] = int(self.spn_del.value())
            self.addrem_func_args['delete_at'] = int(self.spn_at_del.value())
            self.addrem_func_args['backw_del'] = self.chk_backw_del.isChecked()
            self.addrem_func_args['del_chars'] = True

    def addrem_chars(self):
        self.addrem_func_args['both_ops'] = self.chk_add_remove.isChecked()

    def on_maintain_before(self):
        self.txt_maintain_before.setEnabled(self.chk_maintain_before.isChecked())
        self.animation_on = True
        self.preview_general_spaces()

    def on_maintain_after(self):
        self.txt_maintain_after.setEnabled(self.chk_maintain_after.isChecked())
        self.animation_on = True
        self.preview_general_spaces()

    def on_chars_toggled(self):
        self.txt_x_chars.setEnabled(self.rdb_x_chars.isChecked())
        if not self.txt_x_chars.isEnabled():
            self.txt_x_chars.setText('')
        self.animation_on = True
        self.preview_general_spaces()

    def on_char_toggled(self):
        self.txt_one_char.setEnabled(self.rdb_one_char.isChecked())
        if not self.txt_one_char.isEnabled():
            self.txt_one_char.setText('')
        self.animation_on = True
        self.preview_general_spaces()

    def on_replace_name_toggled(self):
        self.txt_replace_name.setEnabled(self.rdb_replace_name.isChecked())
        self.preview_numbers_counter()

    def on_rename_clicked(self):
        if not self.check_regex(self.txt_find.text()):
            QMessageBox(QMessageBox.Warning,
                        self.tr(self.error), self.tr(self.invalid_regex),
                        QMessageBox.Ok, self).exec_()

            self.txt_find.setFocus()
            self.txt_find.selectAll()
            return

        self.rename_items()
        self.view_selection = []
        self.lst_loaded_files.setFocus()

    def on_tab_gen_changed(self, index):
        self.chk_process_name.setEnabled(not (index == 1))
        self.chk_process_ext.setEnabled(not (index == 1))

        self.current_tab = (0, index)
        self.tab_preview_func[self.current_tab]()

    def on_tab_nums_changed(self, index):
        self.chk_process_name.setEnabled(True)
        self.chk_process_ext.setEnabled(True)
        self.current_tab = (1, index)
        self.tab_preview_func[self.current_tab]()

    def open_dir(self, model_index):
        try:
            row_data = path_func(model_index.siblingAtColumn(2).data()).joinpath(model_index.data())
            full_path = str(row_data)

            if path_func(full_path).is_dir():
                self.txt_load_path.setText(full_path)
                self.list_content()
        except:
            return

    def level_up(self):
        current_path = self.txt_load_path.text()
        if current_path == path_func(current_path).root:
            return
        self.txt_load_path.setText(str(path_func(current_path).parent))
        self.list_content()

    def next_stacked_page(self):
        if self.stacked_index == 1:
            self.stacked_index = 0
            self.current_tab = (self.stacked_index, 0)
            self.tab_general.setCurrentIndex(0)
        else:
            self.stacked_index += 1
            self.current_tab = (self.stacked_index, 0)
            self.tab_numbers.setCurrentIndex(0)

        self.stacked_tabs.setCurrentIndex(self.stacked_index)
        self.tab_preview_func[self.current_tab]()

    def previous_stacked_page(self):
        if self.stacked_index == 0:
            self.stacked_index = 1
            self.current_tab = (self.stacked_index, 0)
            self.tab_numbers.setCurrentIndex(0)
        else:
            self.stacked_index -= 1
            self.current_tab = (self.stacked_index, 0)
            self.tab_general.setCurrentIndex(0)

        self.stacked_tabs.setCurrentIndex(self.stacked_index)
        self.tab_preview_func[self.current_tab]()

    def get_dir(self):
        directory = QFileDialog.getExistingDirectory(caption=self.tr(self.ch_dir), directory=self.current_path)

        if not validate_path(directory):
            QMessageBox(QMessageBox.Warning, self.tr(self.error), self.tr(self.invalid_dir), QMessageBox.Ok,
                        self).exec_()
            return

        self.current_path = str(path_func(directory))
        self.txt_load_path.setText(self.current_path)
        self.load_data()

    def list_content(self):
        self.view_selection = []
        directory = self.txt_load_path.text()
        if not validate_path(directory):
            return
        self.current_path = directory
        self.txt_load_path.setText(directory)
        self.fsm.setRootPath(directory)
        self.load_data()

    def init_lang(self):
        lang = self.app_lang
        self.load_language(lang)
        for i in self.lang_menu.actions():
            if i.data() == lang:
                i.setChecked(True)

    def init_theme(self):
        theme, tone = self.theme_name
        index = dict_tones[tone][2]
        self.menu_themes.actions()[index].setChecked(True)
        current_theme = self.set_theme(theme, tone)
        self.theme_name = current_theme[1]
        return current_theme[0]

    def update_status(self):
        self.table_model.setHorizontalHeaderLabels((self.before, self.after, '', ''))
        if self.fetcher_busy:
            self.lbl_status.setText(self.running)
        else:
            self.lbl_status.setText(f'{self.table_model.rowCount()} {self.lbl_items}')

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            self.retranslate_ui()
            self.lst_loaded_files.retranslate_ui()
            self.update_status()
        super().changeEvent(event)

    def load_language(self, language):
        if self.curr_lang != language:
            self.curr_lang = language
            switch_translator(translator, language)
            self.app_lang = language

    def on_lang_changed(self, action: QAction):
        if action:
            self.load_language(action.data())

    def enable_swap(self, state):
        if self.regex_enabled:
            return
        state = True if state == 2 else False
        self.spn_skip.setEnabled(not state)
        self.swap_enabled = state
        self.preview_general_replace()

    def enable_regex(self, state):
        self.chk_swap.setEnabled(not state)
        # self.spn_max_swap.setEnabled(not state)
        self.lbl_skip.setEnabled(not state)
        # self.lbl_max.setEnabled(not state)
        if self.chk_swap.isChecked():
            self.spn_skip.setEnabled(False)
        else:
            self.spn_skip.setEnabled(not state)
        self.regex_enabled = state
        self.animation_on = True
        self.preview_general_replace()

    @pyqtSlot()
    def stop_animation(self):
        self.timer.stop()
        self.animation_on = False
        self.animation.movie_stop()
        self.fetcher_busy = False
        self.update_status()

    @pyqtSlot()
    def on_num_renumber_finished(self):
        self.stop_animation()
        counters.p_enumerate = int(self.spn_start_enum.value())

    @pyqtSlot()
    def on_done_collecting(self):
        self.stop_animation()
        self.lst_loaded_files.setModel(self.table_model)
        self.lst_loaded_files.hide_columns(2, 5)
        self.tab_preview_func[self.current_tab]()
        self.fetcher_busy = False
        self.update_status()

    @pyqtSlot(list)
    def update_model(self, rows):
        for row in rows:
            self.table_model.appendRow(row)

    @pyqtSlot()
    def empty_model(self):
        self.table_model.clear()
        while self.table_model.rowCount():
            pass
        self.table_model.setHorizontalHeaderLabels((self.before, self.after, '', ''))
        self.done_clearing.emit(True)

    @pyqtSlot()
    def clear_selection(self):
        self.lst_loaded_files.clearSelection()
        self.tab_preview_func[self.current_tab]()

    @property
    def theme_name(self):
        return self.settings.get_theme

    @theme_name.setter
    def theme_name(self, theme):
        self.settings.save_theme(theme[0], theme[1])

    @property
    def app_lang(self):
        return self.settings.get_language

    @app_lang.setter
    def app_lang(self, lang):
        self.settings.save_lang(lang)

    @property
    def get_selected_rows(self):
        if not self.view_selection:
            return ()
        else:
            return self.view_selection[0].row(), self.view_selection[-1].row() + 1


def switch_translator(translator, filename):
    app.removeTranslator(translator)
    if translator.load(f":/qtrenamer/i18n/{filename}"):
        app.installTranslator(translator)


def theme_wrapper(palette):
    app.setPalette(palette)


def qt_message_handler(mode, context, message):
    if mode == QtCriticalMsg:
        mode = 'CRITICAL'
    elif mode == QtFatalMsg:
        mode = 'FATAL'

    if mode in ('CRITICAL', 'FATAL'):
        QMessageBox(QMessageBox.Critical, mode, message, QMessageBox.Ok).exec_()


def main():
    app.setStyle('Fusion')
    qInstallMessageHandler(qt_message_handler)
    window = QtRename()
    window.init_lang()
    app.setPalette(window.init_theme())
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
