#!/usr/bin/env python

############################################
# https://github.com/LuuppiChan/luupycards #
############################################

import json
import re
import os
import sys
import shutil
import logging
import argparse
from pathlib import Path
import concurrent.futures

from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets

from info import Ui_info
from seek import Ui_Seek
from ui import Ui_Luupycards
import core_functions as core
from licence import Ui_licence
import gameplay_modules as gameplay
from import_dialog import Ui_DialogImport
from documentation import Ui_documentation


VERSION_NUMBER = "v.2.4"

# argparse
# Create parser
parser = argparse.ArgumentParser(description="Simple flip card program. (GUI!)")

# Add arguments
parser.add_argument("-debug", type=str, default="critical", required=False, help="Choose logging level (debug, info, error or critical (default))")
args = parser.parse_args()  # parse them

# Create logging configuration
match args.debug:
    case "debug":
        log_level = logging.DEBUG
    case "info":
        log_level = logging.INFO
    case "error":
        log_level = logging.ERROR
    case "critical" | _:
        log_level = logging.CRITICAL

# logging
mainlog = logging.getLogger(__name__)
logging.basicConfig(filename=f"{core.get_data_dir()}/luupy.log", encoding="utf-8", level=log_level, filemode="w")


class LicenceWidget(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(LicenceWidget, self).__init__(parent)
        self.ui = Ui_licence()
        self.ui.setupUi(self)


class DocumentationWidget(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(DocumentationWidget, self).__init__(parent)
        self.ui = Ui_documentation()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.hide)


class InfoWidget(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(InfoWidget, self).__init__(parent)
        self.ui = Ui_info()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.hide)

        self.ui.checkBox.setChecked(gameplay.fuzzy_is_available)
        self.ui.checkBox.setEnabled(False)

        self.ui.pushButton_licence.clicked.connect(self.show_licence)

        self.ui.label.setText(f"Luupycards {VERSION_NUMBER}")

    def show_licence(self):
        licence = LicenceWidget(self)
        licence.show()


class ImportDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ImportDialog, self).__init__(parent)
        self.ui = Ui_DialogImport()
        self.ui.setupUi(self)

        # gameplay pair related
        self.pairs = list()

        self.hide_json()
        self.hide_nq()

        self.ui.comboBox_import.activated.connect(self.combobox_update)

        self.ui.pushButton_cancel.clicked.connect(self.cancel_button)
        self.ui.pushButton_ok.clicked.connect(self.ok_button)

        self.ui.radioButton_nq.clicked.connect(self.show_nq)
        self.ui.radioButton_csv.clicked.connect(self.hide_nq)

        self.filepaths = list()
        self.mode = "CSV"
        self.methods = {
            "json" : {
                "default" : False,
                "japan" : False,
                "sentences" : False
            },
            "csv" : {
                "default" : False,
                "alternative": False,
                "nq" : False
            }
        }
        self.selected_a_file = False
        self.all_categories = ["Hiragana", "Katakana", "Radical", "Vocab Meaning", "Vocabulary", "Kanji"]
        self.pronunciation = False

    def closeEvent(self, arg__1: QtGui.QCloseEvent) -> None:
        window.setEnabled(True)
        return super().closeEvent(arg__1)

    def combobox_update(self):
        current_text = self.ui.comboBox_import.currentText()
        if current_text == "CSV":
            mainlog.info("CSV modes")
            self.hide_json()
            self.show_csv()
            self.mode = current_text
        elif current_text == "JSON":
            mainlog.info("JSON modes")
            self.hide_csv()
            self.show_json()
            self.mode = current_text
        else:
            mainlog.error("Whoa! I didn't know this mode existed! %s", self.ui.comboBox_import.currentText())
        self.show_nq() if not self.ui.radioButton_nq.isHidden() and self.ui.radioButton_nq.isChecked() else self.hide_nq()

    def ok_button(self):
        if self.mode == "CSV":
            self.methods["csv"]["default"] = True if self.ui.radioButton_csv.isChecked() else False
            self.methods["csv"]["nq"] = True if self.ui.radioButton_nq.isChecked() else False
            self.methods["alternative"] = True if self.ui.radioButton_alternative.isChecked() else False

            self.filepaths = QtWidgets.QFileDialog.getOpenFileNames(self, "Open Pair File", "pair_file(s)", "Pair files (*.csv)")
            self.filepaths = self.filepaths[0]  # only the file paths

        elif self.mode == "JSON":
            self.methods["json"]["default"] = True if self.ui.checkBox_json.isChecked() else False
            self.methods["json"]["japan"] = True if self.ui.checkBox_jp.isChecked() else False
            self.methods["json"]["sentences"] = True if self.ui.checkBox_sentences.isChecked() else False

            if not(self.methods["json"]["default"] or self.methods["json"]["japan"] or self.methods["json"]["sentences"]):
                please = QtWidgets.QMessageBox(self)
                please.setText("You didn't check any import methods you silly!")
                please.setInformativeText("Please select at least one.")
                please.setStandardButtons(QtWidgets.QMessageBox.Ok)
                please.exec()
                self.filepaths = []
            else:
                self.filepaths = QtWidgets.QFileDialog.getOpenFileNames(self, "Open Pair File", "pair_file(s)", "Pair files (*.json)")
                self.filepaths = self.filepaths[0]  # only the file paths

        if self.filepaths:
            self.selected_a_file = True
            mainlog.info("User selected file(s)")
            self.import_pairs()
            window.setEnabled(True)
            if len(self.filepaths) == 1:
                json_match = re.search(r"^.*[/\\](.*\.json|.*\.csv)$", self.filepaths[0])
                window.ui.label_pair_status.setText(f"Loaded {len(self.pairs) -1} pairs from {json_match.group(1)}.")
            else:
                window.ui.label_pair_status.setText(f"Loaded {len(self.pairs) -1} pairs from multiple files.")
            window.pair_inspector_load()
            self.hide()
        else:
            self.selected_a_file = False
            mainlog.info("User did not select a file")

    def cancel_button(self):
        window.setEnabled(True)
        self.hide()

    def import_pairs(self):
        self.pairs.clear()

        pair_import = core.PairImport()
        if self.mode == "CSV":
            if self.methods["csv"]["default"]:
                for file in self.filepaths:
                    self.pairs.extend(pair_import.pair_import(file))
            elif self.methods["alternative"]:
                for file in self.filepaths:
                    self.pairs.extend(pair_import.pair_import_csv_alternative(file))
            elif self.methods["csv"]["nq"]:
                # only first one since I assume there's only a single file
                self.pairs = pair_import.nq_import(self.filepaths[0], self.selected_categories(), self.pronunciation)
        elif self.mode == "JSON":
            pair_import.default_json = True if self.methods["json"]["default"] else False
            pair_import.jp_mode = True if self.methods["json"]["japan"] else False
            pair_import.sentences = True if self.methods["json"]["sentences"] else False

            for file in self.filepaths:
                self.pairs.extend(pair_import.pair_import_json(file))

        window.pairs.clear()
        window.pairs = self.pairs.copy()

    def hide_csv(self):
        mainlog.info("csv hidden")
        self.ui.radioButton_csv.hide()
        self.ui.radioButton_nq.hide()

    def show_csv(self):
        mainlog.info("csv shown")
        self.ui.radioButton_csv.show()
        self.ui.radioButton_nq.show()

    def hide_json(self):
        mainlog.info("json hidden")
        self.ui.checkBox_json.hide()
        self.ui.checkBox_jp.hide()
        self.ui.checkBox_sentences.hide()

    def show_json(self):
        mainlog.info("json shown")
        self.ui.checkBox_json.show()
        self.ui.checkBox_jp.show()
        self.ui.checkBox_sentences.show()

    def hide_nq(self):
        mainlog.info("nq hidden")
        self.ui.label_nq.hide()
        self.ui.checkBox_nq_hiragana.hide()
        self.ui.checkBox_nq_katakana.hide()
        self.ui.checkBox_nq_radical.hide()
        self.ui.checkBox_nq_kanji.hide()
        self.ui.checkBox_nq_vocabulary_meaning.hide()
        self.ui.checkBox_nq_vocabulary.hide()
        self.ui.checkBox_nq_pronunciation.hide()

    def show_nq(self):
        mainlog.info("nq shown")
        self.ui.label_nq.show()
        self.ui.checkBox_nq_hiragana.show()
        self.ui.checkBox_nq_katakana.show()
        self.ui.checkBox_nq_radical.show()
        self.ui.checkBox_nq_kanji.show()
        self.ui.checkBox_nq_vocabulary_meaning.show()
        self.ui.checkBox_nq_vocabulary.show()
        self.ui.checkBox_nq_pronunciation.show()

    def selected_categories(self) -> list:
        selected_list = []
        if self.ui.checkBox_nq_hiragana.isChecked(): selected_list.append("Hiragana")
        if self.ui.checkBox_nq_katakana.isChecked(): selected_list.append("Katakana")
        if self.ui.checkBox_nq_radical.isChecked(): selected_list.append("Radical")
        if self.ui.checkBox_nq_kanji.isChecked(): selected_list.append("Kanji")
        if self.ui.checkBox_nq_pronunciation.isChecked(): self.pronunciation = True
        if self.ui.checkBox_nq_vocabulary_meaning.isChecked(): selected_list.append("Vocab Meaning")
        if self.ui.checkBox_nq_vocabulary.isChecked(): selected_list.append("Vocabulary")
        return selected_list


class SeekWidget(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SeekWidget, self).__init__(parent)
        self.ui = Ui_Seek()
        self.ui.setupUi(self)

        self.ui.pushButton_ok.clicked.connect(self.ok_press)
        self.ui.pushButton_cancel.clicked.connect(self.cancel_press)

        self.ui.spinBox_seek_value.setMaximum(len(window.the_game.pairs) - 1)
        self.ui.spinBox_seek_value.setValue(window.the_game.current_question)
        self.seek_value = self.ui.spinBox_seek_value.value()
        self.user_entered_number = False

        self.ui.spinBox_seek_value.valueChanged.connect(self.refresh_question)
        self.refresh_question()

    def ok_press(self):
        self.seek_value = self.ui.spinBox_seek_value.value()  # refresh
        self.user_entered_number = True
        self.hide()
        window.correct_checkbutton_mc(f"seek {self.seek_value}")

    def cancel_press(self):
        self.user_entered_number = False
        self.hide()

    def refresh_question(self):
        self.ui.label_question.setText(f"Question: {" / ".join(window.pairs[self.ui.spinBox_seek_value.value()][window.the_game.question])}")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_Luupycards()
        self.ui.setupUi(self)

        # options
        self.reload_settings()
        self.game_options = core.get_options()

        # gameplay
        self.pairs = []
        self.latest_pair_files: list[str] = []

        ## Buttons
        # Recent file list buttons
        # these 2 should be on the same order so the same index is the same item thankfully
        self.recent_files: list[list[str]] = self.game_options["recent files"]
        self.recent_actions: list[QtGui.QAction] = []

        self.ui.menuRecent_files.removeAction(self.ui.actionexample_csv)  # remove the default action

        self.refresh_recent()

        # Quit buttons
        self.ui.button_quit.clicked.connect(self.quit_action)
        self.ui.actionQuit.triggered.connect(self.quit_action)

        self.ui.actionOpen.triggered.connect(self.open_dir_dialog)  # file buttons
        self.ui.button_play.clicked.connect(self.gameplay_setup)  # Start playing
        self.ui.button_check.clicked.connect(self.correct_checkbutton)  # check button
        self.ui.pushButton_check_mc.clicked.connect(self.correct_checkbutton_mc)  # check button mc
        self.ui.actionNew_file.triggered.connect(self.new_pairs)  # new file
        self.ui.menuRecent_files.setToolTip("")

        # settings buttons
        self.ui.button_settings_reset_2.clicked.connect(self.reset_settings)
        self.ui.button_settings_save_2.clicked.connect(self.save_settings)

        # multiple choice
        self.ui.pushButton_seek_mc.clicked.connect(self.seek_mc)
        self.ui.pushButton_correct_mc.clicked.connect(self.correct_mc)
        self.mc_buttons = list()
        self.make_mc_buttons()  # makes some default buttons

        self.mc_choices = list()
        self.mc_correct_choice = ""

        self.ui.pushButton_seek.clicked.connect(self.seek_mc)  # added to the normal modes

        # misc menu
        self.ui.actionBig_mode.triggered.connect(self.big_font_mode)
        self.ui.actionTest_trigger.triggered.connect(self.test_trigger)
        self.ui.actionRegEx_support.triggered.connect(self.regex_setting)
        self.ui.actionShow_only_the_first_question.triggered.connect(self.question_change)
        self.ui.actionShow_only_first_answer.triggered.connect(self.button_refresh)

        self.ui.actionOpen_Advanced.triggered.connect(self.advanced_import)

        # help menu buttons
        self.ui.actionRead_the_docs.triggered.connect(self.open_help)
        self.ui.actionInfo.triggered.connect(self.open_info)

        # inspector
        self.ui.actionSave.triggered.connect(self.pair_inspector_save_to_file)
        self.ui.button_save_file.clicked.connect(self.pair_inspector_save_to_file)
        self.ui.button_save_memory.clicked.connect(self.pair_inspector_save_to_memory)
        self.ui.actionNew_Row.triggered.connect(self.pair_inspector_add_row)
        self.ui.actionRemove_Last_Row.triggered.connect(self.pair_inspector_remove_row)
        self.ui.actionNew_Row_After_Selected.triggered.connect(self.pair_inspector_new_row_after_selected)
        self.ui.actionDelete_Selected_Row.triggered.connect(self.pair_inspector_remove_selected_row)
        self.pair_widget_items = {
            "question" : [],
            "answer" : [],
        }
        self.pair_inspector_load()
        self.enough_pairs = True

        self.drop_data = {
            "file" : False,
            "text" : False
        }

        # session restore is after setups
        # gameplay stuff
        params: dict[str, str | bool | int | list[str]] = self.game_options["last game settings"]

        if params["pairs"]:
            self.open_dir_dialog(params["pairs"], True)  # tries to load last session pair files silently

        #if self.pairs:  # checks if the load was successful
        if False:  # restore is currently disabled
            #self.ui.comboBox_modes.setObjectName(params["mode"])
            #self.ui.comboBox_question_order.setObjectName(params["order"])
            # this isn't the correct method to changing the selected object #

            self.gameplay_setup("False", params["streak_current"], params["current_question"], True)
            self.ui.tab_main.setCurrentWidget(self.ui.tab_play)
        else:
            self.the_game = gameplay.MainGameplay(
                [{"question": ["Please open a file."], "answer": ["Please open a file."]}])
            self.ui.tab_play.setEnabled(False)  # this is enabled by the game setup thingy
            self.current_mode = "Unset"
            self.current_order = "Unset"

        # big mode
        self.ui.actionBig_mode.setChecked(self.game_options["big mode"])
        self.big_font_mode()

        mainlog.info("Set up class init.")

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent) -> None:
        # Reset all the options
        for key in self.drop_data.keys():
            self.drop_data[key] = False

        if event.mimeData().hasUrls():
            self.drop_data["file"] = True
            self.ui.label_drag.setText("Drop your pair file.")
            files = [u.toLocalFile() for u in event.mimeData().urls()]
            for file in files:
                json_match = re.search(r"^.*[/\\](.*\.json|.*\.csv)$", file)
                if not json_match:
                    self.ui.label_drag.setText("One or more of the files you're holding can't be pair (a) file(s)... Yet...")
            event.accept()
        elif event.mimeData().hasText():
            self.drop_data["text"] = True
            self.ui.label_drag.setText("Text is not supported... Yet...")
            event.accept()
        else:
            event.ignore()
        # Is this needed?
        return super().dragEnterEvent(event)

    def dragLeaveEvent(self, event: QtGui.QDragLeaveEvent) -> None:
        self.ui.label_drag.setText("")
        return super().dragLeaveEvent(event)

    def dropEvent(self, event):
        if self.drop_data["file"]:
            files = [u.toLocalFile() for u in event.mimeData().urls()]
            to_be_loaded = []
            has_invalid_files = False
            for file in files:
                json_match = re.search(r"^.*[/\\](.*\.json|.*\.csv)$", file)
                if not json_match:
                    has_invalid_files = True
                else:
                    to_be_loaded.append(file)

            if has_invalid_files:
                QtWidgets.QMessageBox.warning(self, "Filetype Error!", "Please select a valid filetype.\n(.csv or .json)\nOnly valid files will be loaded.")

            if to_be_loaded:
                self.open_dir_dialog(to_be_loaded)

        self.ui.label_drag.setText("")

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.game_options["last game settings"] = {
            "pairs": self.latest_pair_files,
            "reverse": self.the_game.question == "answer",
            "current_question": self.the_game.current_question,
            "streak_current": self.the_game.streak_current,
            "order": self.ui.comboBox_question_order.currentText().lower(),
            "mode": self.ui.comboBox_modes.currentText().lower(),
        }
        self.game_options["big mode"] = self.ui.actionBig_mode.isChecked()
        while len(self.game_options["recent files"]) > 11:  # 1 is the max amount of recent files (check recent_file_clicked under for more info)
            self.game_options["recent files"].pop(0)
        self.game_options["recent files"] = self.recent_files
        core.get_options("dump", self.game_options)
        return super().closeEvent(event)

    def recent_file_clicked(self, item: list[str]):
        # as a temporary solution I'll be having only a single recent file due to a massive skill issue
        #action = self.ui.menuRecent_files
        #self.open_dir_dialog(action.data())
        # Some signals can probably fix this
        # lambda with connect fixed it probably, haven't tested
        self.open_dir_dialog(item)
        #QtWidgets.QMessageBox.warning(self, "Not implemented", "This functionality is not yet implemented")


    def refresh_recent(self):
        if self.recent_files:
            while len(self.recent_files) > 11:  # ensure only n entries
                self.recent_files.pop(0)

            for file in self.recent_files:
                recent_file = QtGui.QAction()
                match = re.search(r".*[/\\](.*\.(?:csv|json))", file[0])
                if match:
                    filename: str = match.group(1)
                else:  # it should always find a name, but let's give it a name if a name isn't found for some reason.
                    filename = "unknown.csv"
                recent_file.setText(filename)
                #recent_file.setData(file)
                recent_file.triggered.connect(lambda _: self.recent_file_clicked(file))
                tooltip = ""
                for name in file:
                    tooltip = tooltip + f"{name} "
                recent_file.setToolTip(tooltip)
                recent_file.setStatusTip(tooltip)
                self.ui.menuRecent_files.addAction(recent_file)
                self.recent_actions.append(recent_file)

    def button_refresh(self) -> None:
        self.spawn_mc_buttons(new=False)

    def regex_setting(self):
        if self.ui.actionRegEx_support.isChecked():
            self.the_game.enabled_answer_checks["regex"] = True
        else:
            self.the_game.enabled_answer_checks["regex"] = False

    def advanced_import(self):
        self.setEnabled(False)
        mainlog.info("User used advanced import")
        advanced_import = ImportDialog(self)
        advanced_import.show()

    def big_font_mode(self):
        font_family = 'Sans Serif'
        if self.ui.actionBig_mode.isChecked():
            self.ui.label_question.setFont(QtGui.QFont(font_family, 20 * 2))
            self.ui.label_question_mc.setFont(QtGui.QFont(font_family, 20 * 2))
            self.ui.lineEdit_answer.setFont(QtGui.QFont(font_family, 16 * 2))
            self.ui.label_streak.setFont(QtGui.QFont(font_family, 12 * 2))
            self.ui.label_streak_mc.setFont(QtGui.QFont(font_family, 12 * 2))
            self.ui.label_game_info.setFont(QtGui.QFont(font_family, 12 *2 ))
            self.ui.label_game_info_mc.setFont(QtGui.QFont(font_family, 12 * 2))
            self.ui.button_check.setFont(QtGui.QFont(font_family, 16))
            self.ui.pushButton_check_mc.setFont(QtGui.QFont(font_family, 16))
            for button in self.mc_buttons:
                button.setFont(QtGui.QFont(font_family, 12*2))
            self.ui.pushButton_correct_mc.setFont(QtGui.QFont(font_family, 16))
            self.ui.pushButton_seek_mc.setFont(QtGui.QFont(font_family, 16))
            self.ui.pushButton_seek.setFont(QtGui.QFont(font_family, 16))
            self.ui.label_lives.setFont(QtGui.QFont(font_family, 16))
        else:
            self.ui.label_question.setFont(QtGui.QFont(font_family, 20))
            self.ui.label_question_mc.setFont(QtGui.QFont(font_family, 20))
            self.ui.lineEdit_answer.setFont(QtGui.QFont(font_family, 16))
            self.ui.label_streak.setFont(QtGui.QFont(font_family, 12))
            self.ui.label_streak_mc.setFont(QtGui.QFont(font_family, 12))
            self.ui.label_game_info.setFont(QtGui.QFont(font_family, 12))
            self.ui.label_game_info_mc.setFont(QtGui.QFont(font_family, 12))
            self.ui.button_check.setFont(QtGui.QFont(font_family, 12))
            self.ui.pushButton_check_mc.setFont(QtGui.QFont(font_family, 12))
            for button in self.mc_buttons:
                button.setFont(QtGui.QFont(font_family, 12))
            self.ui.pushButton_correct_mc.setFont(QtGui.QFont(font_family, 12))
            self.ui.pushButton_seek_mc.setFont(QtGui.QFont(font_family, 12))
            self.ui.pushButton_seek.setFont(QtGui.QFont(font_family, 12))
            self.ui.label_lives.setFont(QtGui.QFont(font_family, 12))

    def question_change(self) -> None:
        if self.ui.tab_play.isEnabled():
            self.set_question(("", [""], ""))
            self.set_question(self.the_game.play_gui())

    def correct_checkbutton(self):
        line_text = self.ui.lineEdit_answer.text()
        if line_text:
            self.reload_settings()
            self.the_game.user_input = line_text.lower()
            result = self.the_game.answer_check_gui(line_text.lower().strip())  # Makes it lower and strips trailing spaces (maybe should be in the answer check preferably)

            self.set_question(self.the_game.play_gui())
            self.ui.lineEdit_answer.clear()
            self.set_streak()

            if self.current_mode == "Survive!":
                # This will never be unset since it checks that survive mode is set, although it's not the best check
                self.ui.label_lives.setText(f"Lives left: {self.the_game.lives}")  # this is just in case

            match result[0]:
                case "correct":
                    self.set_info(result[1])
                case "fuzzy correct":
                    self.set_info(result[1])
                case "seek":
                    self.set_info(result[1])
                case "show correct answer":
                    self.set_info(result[1])
                    if self.current_mode == "Survive!":
                        self.set_info(self.the_game.return_correct_answers())
                        self.the_game.lives += -1
                        self.ui.label_lives.setText(f"Lives left: {self.the_game.lives}")
                        if self.the_game.lives == 0:
                            self.ui.tab_main.setCurrentWidget(self.ui.tab_main_menu)
                            self.ui.tab_play.setEnabled(False)

                            lose_dialog = QtWidgets.QMessageBox(self)
                            lose_dialog.setText("You died!")
                            lose_dialog.setInformativeText(self.the_game.return_correct_answers())
                            lose_dialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
                            lose_dialog.exec()

                case "quit":
                    self.ui.tab_main.setCurrentWidget(self.ui.tab_main_menu)
                    self.ui.tab_play.setEnabled(False)
                    self.ui.label_game_info.setText("Quitting...")
                    self.ui.label_game_info_mc.setText("Quitting...")
                case "empty field":  # this can appear when user inputs only whitespaces
                    self.set_info("Please type something...")
                case "wrong":
                    self.set_info(result[1])

                    if self.current_mode == "Survive!":
                        self.set_info(self.the_game.return_correct_answers())
                        self.the_game.lives += -1
                        self.ui.label_lives.setText(f"Lives left: {self.the_game.lives}")
                        if self.the_game.lives == 0:
                            self.ui.tab_main.setCurrentWidget(self.ui.tab_main_menu)
                            self.ui.tab_play.setEnabled(False)

                            lose_dialog = QtWidgets.QMessageBox(self)
                            lose_dialog.setText("You died!")
                            lose_dialog.setInformativeText(self.the_game.return_correct_answers())
                            lose_dialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
                            lose_dialog.exec()
        else:
            mainlog.info("Empty button press.")

            self.set_question(("", [""], ""))
            self.set_question(self.the_game.play_gui())

    def correct_checkbutton_mc(self, user_input = ""):
        self.reload_settings()

        if not user_input:
            for i, button in enumerate(self.mc_buttons):
                if button.isChecked():
                    user_input = button.text()

        self.the_game.user_input = user_input
        result = self.the_game.answer_check_gui(user_input)

        self.set_question(self.the_game.play_gui())
        self.set_streak()
        self.ui.lineEdit_answer.clear()

        match result[0]:
            case "correct":
                self.set_info(result[1])
                self.spawn_mc_buttons()
                self.big_font_mode()  # refreshes for button fonts
            case "fuzzy correct":
                self.set_info(result[1])
            case "seek":
                self.set_info(result[1])
                self.spawn_mc_buttons()
            case "show correct answer":
                self.set_info(result[1])
            case "quit":
                self.ui.tab_main.setCurrentWidget(self.ui.tab_main_menu)
                self.ui.tab_play.setEnabled(False)
                self.ui.label_game_info.setText("Quitting...")
                self.ui.label_game_info_mc.setText("Quitting...")
            case "empty field":
                self.set_info("Please choose an option...")

                self.set_question(("", [""], ""))
                self.set_question(self.the_game.play_gui())
            case "wrong":
                self.set_info(result[1])

    def open_dir_dialog(self, files: list[str] | None = None, suppress_misc_errors=False):
        try:
            self.pairs.clear()
            pair_import = core.PairImport()

            if not files:
                file_paths = QtWidgets.QFileDialog.getOpenFileNames(self, "Open Pair File", "pair_file", "Pair files (*.json *.csv)")
            else:
                file_paths = (files, "other information that file dialog gives")

            self.latest_pair_files = file_paths[0]  # saves for session restore function
            self.recent_files.append(file_paths[0])

            if file_paths[0]:  # if there are pair files
                # this multithreading is broken, fix it before commit!
                # What do you mean broken past me? It works perfectly fine.
                with concurrent.futures.ThreadPoolExecutor(60) as executor:
                    threads: list[concurrent.futures.Future] = []
                    print(file_paths[0])
                    for i, file in enumerate(file_paths[0]):
                        mainlog.info(f"Submitting to thread {i}")
                        threads.append(executor.submit(pair_import.determine_pair_file, file, False, False))
                        json_match = re.search(r"^.*[/\\](.*\.json|.*\.csv)$", file)
                        self.ui.label_pair_status.setText(f"Loaded {len(self.pairs) -1} pairs from {json_match.group(1)}.")
                    else:
                        print("All submitted!")

                    # This makes sure that all threads are finished before answer fetching
                    for i, future in enumerate(threads):
                        mainlog.debug(f"Waiting for thread {i}")
                        future.result()

                    mainlog.info("All results done.")

                    # after pairs are loaded
                    for future in threads:
                        self.pairs.extend(future.result())
                        mainlog.debug("self.pairs now has %s pair(s)", len(self.pairs))

                    mainlog.info("All loaded!")

                    if len(self.pairs) == 0:  # ensures there are pairs
                        raise FileNotFoundError

                    if len(file_paths[0]) == 1:
                        json_match = re.search(r"^.*[/\\](.*\.json|.*\.csv)$", file_paths[0][0])
                        self.ui.label_pair_status.setText(f"Loaded {len(self.pairs) -1} pairs from {json_match.group(1)}.")
                    else:
                        self.ui.label_pair_status.setText(f"Loaded {len(self.pairs) -1} pairs from multiple files.")

                    # only if new pair files
                    self.pair_inspector_load()

                    if self.ui.tab_play.isEnabled():
                        # setups the gameplay again if it's enabled
                        self.gameplay_setup("False", self.the_game.current_question, self.the_game.streak_current)

                mainlog.info("Threads closed.")

        except UnicodeEncodeError:
            self.ui.label_pair_status.setText("Pairs not loaded")
            QtWidgets.QMessageBox.critical(self, "Import Error!", "The file(s) you're trying to import aren't in a supported format (utf-8)")

        except FileNotFoundError:
            # In most cases this is caused by the raise statement above.
            self.ui.label_pair_status.setText("Pairs not loaded")

        except Exception as e:  # I'm sorry for making bad code, but I want feedback for the user.
            if suppress_misc_errors:
                pass
            else:
                self.ui.label_pair_status.setText("Pairs not loaded")
                error_message = QtWidgets.QMessageBox(self)
                error_message.setWindowTitle("Import Error!")
                error_message.setText("Something went wrong while trying to import pairs.\nPlease check that you gave a valid pair file.")
                error_message.setInformativeText(str(e))

    def quit_action(self):
        self.close()

    def set_streak(self):
        streak = self.the_game.streak_current
        streak_all = self.the_game.streak_all_time

        self.ui.label_streak.setText(f"Current streak: {streak}")
        self.ui.label_streak_mc.setText(f"Current streak: {streak}")

        self.ui.label_streak.setToolTip(f"Current streak: {streak}, All time streak: {streak_all}")
        self.ui.label_streak_mc.setToolTip(f"Current streak: {streak}, All time streak: {streak_all}")

        self.ui.label_streak.setStatusTip(f"Current streak: {streak}, All time streak: {streak_all}")
        self.ui.label_streak_mc.setStatusTip(f"Current streak: {streak}, All time streak: {streak_all}")

    def set_question(self, question: tuple[str, list[str], str]):  # and tooltips
        if self.ui.actionShow_only_the_first_question.isChecked():
            self.ui.label_question.setText(f"{question[2]}{question[1][0]}")
            self.ui.label_question_mc.setText(f"{question[2]}{question[1][0]}")
        else:
            self.ui.label_question.setText(f"{question[2]}{question[0]}")
            self.ui.label_question_mc.setText(f"{question[2]}{question[0]}")

        # question tooltip
        # checks if the pair has a question tooltip
        if f"{self.the_game.question} tooltip" in self.the_game.pairs[self.the_game.current_question]:
            tooltip = self.the_game.pairs[self.the_game.current_question][f"{self.the_game.question} tooltip"]

            self.ui.label_question.setToolTip(tooltip)
            self.ui.label_question.setStatusTip(tooltip)
            self.ui.label_question_mc.setToolTip(tooltip)
            self.ui.label_question_mc.setStatusTip(tooltip)
        else:
            # if the game mode is reverse it hides the question
            tooltip = f"{question[2]}{question[0]}" if self.the_game.question == "question" else "The question"

            self.ui.label_question.setToolTip(tooltip)
            self.ui.label_question.setStatusTip(tooltip)
            self.ui.label_question_mc.setToolTip(tooltip)
            self.ui.label_question_mc.setStatusTip(tooltip)

        # answer tooltip
        # checks if the pair has an answer tooltip
        if f"{self.the_game.answer} tooltip" in self.the_game.pairs[self.the_game.current_question]:
            tooltip = self.the_game.pairs[self.the_game.current_question][f"{self.the_game.answer} tooltip"]

            self.ui.lineEdit_answer.setStatusTip(tooltip)
            self.ui.lineEdit_answer.setToolTip(tooltip)
        else:
            tooltip = "The answer"

            self.ui.lineEdit_answer.setStatusTip(tooltip)
            self.ui.lineEdit_answer.setToolTip(tooltip)

    def set_info(self, info):
        self.ui.label_game_info.setText(info)
        self.ui.label_game_info_mc.setText(info)

    def spawn_mc_buttons(self, new=True):
        self.delete_mc_buttons()
        self.make_mc_buttons()

        if new:
            self.mc_correct_choice, self.mc_choices = self.the_game.generate_multiple_choice_answers_gui()
        else:
            self.mc_correct_choice, self.mc_choices = self.the_game.generate_multiple_choice_answers_gui(generate_new=False,
                                                                                                         correct_index=self.mc_correct_choice,
                                                                                                         multiple_choice_options=self.mc_choices)

        for (choice, button) in zip(self.mc_choices, self.mc_buttons):
            if self.ui.actionShow_only_first_answer.isChecked():
                button.setText(choice[0])
            else:
                button.setText(choice[1])

            #QtWidgets.QRadioButton.setToolTip()
            # Tooltip could maybe be added here. (It's way too difficult)

        self.big_font_mode()  # ensures the buttons get big font

    def seek_mc(self):
        seek = SeekWidget(self)
        seek.show()

    def correct_mc(self):
        self.correct_checkbutton_mc("correct")

    def gameplay_setup(self, new_game="True", current_streak=0, current_question=1, respect_user_minmax=False):
        if len(self.pairs) > 1:
            multiple_choice_criteria = True
            if new_game == "False":
                new_game = False
            else:
                new_game = True

            if current_question <= 0:
                # Honestly I don't know how to fix this any other way, but whatever.
                mainlog.error(f"Invalid question number {current_question}! This is likely from reloading the game when on question 1. Fixing...")
                current_question = 1

            # determine mode
            self.current_mode = self.ui.comboBox_modes.currentText()
            self.current_order = self.ui.comboBox_question_order.currentText()

            if self.current_mode == "Multiple Choice":
                if len(self.pairs) < core.settings_value_manipulator("multiple choice max options") + 1:
                    multiple_choice_criteria = False
                    mainlog.error("Not enough pairs to make options!")
                    QtWidgets.QMessageBox.warning(self, "Error!", "Not enough pairs to make options!\nPlease decrease multiple choice option count or make more pairs.")

            if self.pairs and multiple_choice_criteria:
                mainlog.info("Creating gameplay...")

                if respect_user_minmax:
                    pass
                else:
                    #if core.settings_value_manipulator("max question") > len(self.pairs) - 1:
                    core.settings_value_manipulator("max question", "dump", len(self.pairs) - 1)
                    #if core.settings_value_manipulator("min question") > core.settings_value_manipulator("max question"):
                    core.settings_value_manipulator("min question", "dump", 1)

                self.reload_settings()

                # set tab to play
                if new_game:
                    self.ui.tab_main.setCurrentWidget(self.ui.tab_play)
                    if self.current_mode in ["Multiple Choice", "Multiple Choice Reverse"]:
                        self.ui.stackedWidget_gameplay.setCurrentWidget(self.ui.multiple_choice)
                    else:
                        self.ui.stackedWidget_gameplay.setCurrentWidget(self.ui.input)
                    self.ui.action_tabls_play.setEnabled(True)
                    self.ui.tab_play.setEnabled(True)

                print(self.current_mode, self.current_order)  # then pass to backend
                self.the_game = gameplay.determine_gamemode(
                    self.current_mode,
                    self.current_order,
                    self.pairs,
                    self.ui.checkBox_question_flip.isChecked(),
                    current_question if self.game_options["min question"] < current_question < self.game_options["max question"] else self.game_options["min question"],
                    current_streak,
                    self.ui.actionRegEx_support.isChecked()
                )

                self.set_streak()
                self.set_question(self.the_game.play_gui())

                # Then back to finish mc and s!
                if self.current_mode in ["Multiple Choice", "Multiple Choice Reverse"]:
                    self.spawn_mc_buttons()
                elif self.current_mode == "Survive!":
                    self.ui.label_lives.setText(f"Lives left: {self.the_game.lives}")
                else:
                    self.ui.label_lives.setText("")

                self.set_info(f"Now playing: {self.current_mode}")

            elif not(self.current_mode == "Multiple Choice"):
                mainlog.info("No pairs detected.")
                QtWidgets.QMessageBox.warning(self, "Pair error!", "Please import pairs before you start playing!\nFile -> Open")
        else:
            mainlog.info("No pairs detected.")
            QtWidgets.QMessageBox.warning(self, "Pair error!", "Please import pairs before you start playing!\nFile -> Open")

    def make_mc_buttons(self):
        buttons_needed = core.settings_value_manipulator("multiple choice max options")
        self.mc_buttons = []

        for i in range(buttons_needed):
            button = QtWidgets.QRadioButton(f"This shouldn't show up :/ {i + 1}")
            button.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
            self.mc_buttons.append(button)
            self.ui.mc_options.addWidget(self.mc_buttons[i])

    def delete_mc_buttons(self):
        for button in self.mc_buttons:
            self.ui.mc_options.removeWidget(button)

        for _ in range(len(self.mc_buttons)):
            self.mc_buttons[0].deleteLater()
            self.mc_buttons.pop(0)

    def test_trigger(self):
        mainlog.info("Test trigger activated!")

    def reload_settings(self):
        self.game_options = core.get_options("load")
        options = self.game_options

        self.ui.all_time_streak_value_2.setText(str(options["all time streak"]))
        self.ui.all_time_survival_streak_value_2.setText(str(options["all time survival streak"]))
        self.ui.reset_all_time_streak_value_2.setChecked(options["reset all time streak"])
        self.ui.reset_all_time_survival_streak_value_2.setChecked(options["reset all time survival streak"])
        self.ui.min_question_value_2.setValue(options["min question"])
        self.ui.max_question_value_2.setValue(options["max question"])
        self.ui.show_current_question_number_value_2.setChecked(options["show current question number"])
        self.ui.multiple_choice_max_options_value_2.setValue(options["multiple choice max options"])
        self.ui.lives_value_2.setValue(options["lives"])
        self.ui.fuzzy_select_precent_value_2.setValue(options["fuzzy select percent"])

    def reset_settings(self):
        def ok():
            script_dir = os.path.dirname(os.path.abspath(__file__))
            settings_path = os.path.join(script_dir, "settings.json")

            # static settings path
            home_dir = Path.home()
            static_path = f"{home_dir}/.cache/luupycards"  # This isn't kinda cross-platform since Windows doesn't have this folder
            settings_filename = "settings.json"
            static_settings_path = os.path.join(static_path, settings_filename)

            # creates the static dir if it doesn't exist (just in case)
            os.makedirs(static_path, exist_ok=True)  # for cross-platform compatibility

            # creates settings file
            shutil.copy(settings_path, static_settings_path)  # for cross-platform compatibility

            mainlog.info("Reset settings")

            self.reload_settings()
            mainlog.info("Reloaded settings")

        are_you_sure = QtWidgets.QMessageBox(self)
        are_you_sure.setText("Are you sure you want to reset all the settings?")
        are_you_sure.setInformativeText("Your all time streaks will be reset!")
        are_you_sure.setStandardButtons(QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.Cancel)
        are_you_sure.button(QtWidgets.QMessageBox.Ok).clicked.connect(ok)
        are_you_sure.exec()

    def save_settings(self):
        self.game_options["all time streak"]                = int(self.ui.all_time_streak_value_2.text())
        self.game_options["all time survival streak"]       = int(self.ui.all_time_survival_streak_value_2.text())
        self.game_options["reset all time streak"]          = self.ui.reset_all_time_streak_value_2.isChecked()
        self.game_options["reset all time survival streak"] = self.ui.reset_all_time_survival_streak_value_2.isChecked()
        self.game_options["min question"]                   = self.ui.min_question_value_2.value()
        self.game_options["max question"]                   = self.ui.max_question_value_2.value()
        self.game_options["show current question number"]   = self.ui.show_current_question_number_value_2.isChecked()
        self.game_options["multiple choice max options"]    = self.ui.multiple_choice_max_options_value_2.value()
        self.game_options["lives"]                          = self.ui.lives_value_2.value()
        self.game_options["fuzzy select percent"]           = self.ui.fuzzy_select_precent_value_2.value()

        core.static_value_functions_gui()
        self.static_value_settings()
        self.check_invalid_settings()
        core.get_options("dump", self.game_options)
        mainlog.info("Saved settings")
        self.reload_settings()
        mainlog.info("Reloaded settings")

        # paris check seems kind of useless to be honest
        if self.pairs and self.ui.tab_play.isEnabled():
            current_question = self.the_game.current_question
            # setups the gameplay again
            self.gameplay_setup("False", self.the_game.streak_current, current_question, True)

    def check_invalid_settings(self):
        options_orig = core.get_options()

        if self.game_options["min question"] > self.game_options["max question"]:
            self.game_options["max question"] = self.game_options["min question"]
        if self.pairs:
            if self.game_options["max question"] > len(self.pairs):
                self.game_options["max question"] = len(self.pairs) -1

        if options_orig != self.game_options:
            mainlog.warning("Found illegal settings values, fixing...")

    def static_value_settings(self):
        static_values = ["reset all time streak", "reset all time survival streak"]

        # other static value functions can be added here
        if self.ui.reset_all_time_streak_value_2.isChecked():
            self.ui.reset_all_time_streak_value_2.setChecked(False)
            self.game_options["reset all time streak"] = False
            self.game_options["all time streak"] = 0

        if self.ui.reset_all_time_survival_streak_value_2.isChecked():
            self.ui.reset_all_time_survival_streak_value_2.setChecked(False)
            self.game_options["reset all time survival streak"] = False
            self.game_options["all time survival streak"] = 0

    @staticmethod
    def give_flag(flag, inside):
        return f"{";FLAG: {" + flag + "='" + inside + "'}"}"

    def pair_inspector_load(self):
        pair0 = core.PairImport.pair0
        if self.pairs:
            if self.pairs[0] == pair0:
                self.pairs.pop(0)

        for _ in range(self.ui.tableWidget.rowCount()):  # first remove all old rows
            self.ui.tableWidget.removeRow(0)

        for i, pair in enumerate(self.pairs):
            self.ui.tableWidget.insertRow(i)

            question = QtWidgets.QTableWidgetItem()
            questionstring = ";".join(pair["question"])
            if "question tooltip" in pair:
                tooltip = self.give_flag("tooltip", pair["question tooltip"] if pair['question tooltip'] != "The question" else "")
                if tooltip:
                    questionstring += tooltip
            question.setText(questionstring)

            answer = QtWidgets.QTableWidgetItem()

            answerstring = ";".join(pair["answer"])
            if "answer tooltip" in pair:
                answerstring += self.give_flag("tooltip", pair["answer tooltip"] if pair['answer tooltip'] != 'Input your answer' else "")

            if "regex" in pair:
                answerstring += self.give_flag("regex", "True" if pair["regex"] else "False")
            answer.setText(answerstring)

            self.ui.tableWidget.setItem(i, 0, question)  # questions
            self.ui.tableWidget.setItem(i, 1, answer)  # answers

        # after everything is done adds the pair back
        if self.pairs:
            if self.pairs[0] != pair0:
                self.pairs.insert(0, pair0)

    def ensure_loaded(self):
        # It seems that in some cases the C++ objects have already been deleted, so this loads them again
        self.pair_widget_items["question"].clear()
        self.pair_widget_items["answer"].clear()

        rows = self.ui.tableWidget.rowCount()

        for row in range(rows):
            self.pair_widget_items["question"].append(self.ui.tableWidget.item(row, 0))
            self.pair_widget_items["answer"].append(self.ui.tableWidget.item(row, 1))

    def pair_inspector_save_to_memory(self, return_pairs=False):
        pairs = []
        self.ensure_loaded()

        for (question, answer) in zip(self.pair_widget_items["question"], self.pair_widget_items["answer"]):
            pair = {
                "question": question.text().split(";"),
                "answer": answer.text().split(";"),
            }

            if "question tooltip" not in pair:
                for item in pair["question"]:
                    result = re.search(core.PairImport.tooltip_regex, item)
                    if result:
                        pair["question tooltip"] = result.group(1)
                        pair["question"].remove(item)

                if "question tooltip" not in pair:
                    pair["question tooltip"] = " / ".join(pair["question"])

            if "answer tooltip" not in pair:
                for item in pair["answer"]:
                    result = re.search(core.PairImport.tooltip_regex, item)
                    if result:
                        pair["answer tooltip"] = result.group(1)
                        pair["answer"].remove(item)
                    result = re.search(core.PairImport.regex_enabled_regex, item)
                    if result:
                        if result.group(1) in ["True", "true", "1", "Yes", "yes"]:
                            pair["regex"] = True
                        elif result.group(1) in ["False", "false", "0", "No", "no"]:
                            pair["regex"] = False

                if "answer tooltip" not in pair:
                    pair["answer tooltip"] = "Input your answer"

            pairs.append(pair.copy())

        # after everything is done adds the pair back
        pair0 = core.PairImport.pair0

        if return_pairs:
            return pairs
        else:
            pairs.insert(0, pair0)
            self.pairs.clear()
            self.pairs = pairs

        self.ui.label_pair_status.setText(f"Loaded {len(self.pairs) -1} pairs from Inspector.")

        if self.pairs:
            if self.ui.tab_play.isEnabled():
                # setups the gameplay again
                self.gameplay_setup("False", self.the_game.streak_current, self.the_game.current_question)

        else:
            QtWidgets.QMessageBox.warning(self, "Warning", "You don't have any pairs.\nRestart game play from main menu.")
            self.ui.tab_play.setEnabled(False)

    def pair_inspector_save_to_file(self):
        self.ensure_loaded()
        pairs = self.pair_inspector_save_to_memory(True)

        for pair in pairs:
            if "question tooltip" in pair:
                if pair["question tooltip"] == " / ".join(pair["question"]):
                    pair.pop("question tooltip")

            if "answer tooltip" in pair:
                if pair["answer tooltip"] == "Input your answer":
                    pair.pop("answer tooltip")

        full_json_file = {
            "pairs" : pairs
        }

        filepath = QtWidgets.QFileDialog.getSaveFileName(self, "Save Pair File", "new_pair_file.json", "Pair file (*.json)")
        filepath = filepath[0]  # only the file path

        if filepath:  # ensures user chose a location
            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(full_json_file, file, ensure_ascii=False, indent=4)

    def pair_inspector_add_row(self):
        last_row = self.ui.tableWidget.rowCount()

        self.ui.tableWidget.insertRow(last_row)

        question = QtWidgets.QTableWidgetItem()
        question.setText("")

        answer = QtWidgets.QTableWidgetItem()
        answer.setText("")

        self.ui.tableWidget.setItem(last_row, 0, question)  # questions
        self.ui.tableWidget.setItem(last_row, 1, answer)  # answers

    def pair_inspector_remove_row(self):
        last_row = self.ui.tableWidget.rowCount() -1

        self.ui.tableWidget.removeRow(last_row)

    def pair_inspector_remove_selected_row(self):
        this_row = self.ui.tableWidget.currentRow()

        self.ui.tableWidget.removeRow(this_row)

    def pair_inspector_new_row_after_selected(self):
        this_row = self.ui.tableWidget.currentRow() +1

        self.ui.tableWidget.insertRow(this_row)

        question = QtWidgets.QTableWidgetItem()
        question.setText("")

        answer = QtWidgets.QTableWidgetItem()
        answer.setText("")

        self.ui.tableWidget.setItem(this_row, 0, question)  # questions
        self.ui.tableWidget.setItem(this_row, 1, answer)  # answers

    def open_help(self):
        mainlog.info("User needs help")
        documentation = DocumentationWidget(self)
        documentation.show()

    def open_info(self):
        mainlog.info("User wants info")
        info = InfoWidget(self)
        info.show()

    def new_pairs(self):
        def ok():
            self.latest_pair_files = []
            self.pairs.clear()
            self.ui.tab_play.setEnabled(False)
            self.pair_inspector_load()
            self.ui.label_pair_status.setText("Pairs not loaded")
            if self.ui.tab_main.currentWidget() == self.ui.tab_play:
                self.ui.tab_main.setCurrentWidget(self.ui.tab_main_menu)

        if self.pairs:
            warning = QtWidgets.QMessageBox(self)
            warning.setText("Are you sure you want to create a new file")
            warning.setInformativeText("Unsaved pairs will be lost.")
            warning.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            warning.button(QtWidgets.QMessageBox.Ok).clicked.connect(ok)
            warning.exec()


if __name__ == "__main__":
    try:
        import qt_themes
    except ModuleNotFoundError:
        pass

    if os.name == "nt":
        mainlog.warning("This program is intended for Linux, using Windows may have unexpected behaviour!")
    app = QtWidgets.QApplication(sys.argv)

    # theming
    style_name = app.style().metaObject().className()
    #qt_themes.set_theme("blender") if style_name == "QFusionStyle" else None  # colors

    if style_name == "QFusionStyle":
        palette = QtGui.QPalette()  # it works so it's fine
        palette.setColor(QtGui.QPalette.Accent, QtGui.QColor(218, 130, 218))
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Base, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.black)
        palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
        palette.setColor(QtGui.QPalette.Link, QtGui.QColor(218, 130, 218))
        palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(218, 130, 218))
        palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
        app.setPalette(palette)

    window = MainWindow()
    window.show()

    # Windows fixes
    if os.name == "nt":
        # This is just ensuring:
        window.setWindowOpacity(1)  # Do not ever never remove this, it 100% breaks Windows compatibility.

    sys.exit(app.exec())
