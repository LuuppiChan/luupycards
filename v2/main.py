#!/usr/bin/env python
import json
import re
import os
import sys
import shutil
import logging
import argparse
from pathlib import Path

from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets

from seek import Ui_Seek
from ui import Ui_Luupycards
import core_functions as core
import gameplay_modules as gameplay
from import_dialog import Ui_DialogImport


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


class ImportDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ImportDialog, self).__init__(parent)
        self.ui = Ui_DialogImport()
        self.ui.setupUi(self)

        # gameplay pair related
        self.pairs = list()

        self.hide_json()

        self.ui.comboBox_import.activated.connect(self.combobox_update)

        self.ui.pushButton_cancel.clicked.connect(self.cancel_button)
        self.ui.pushButton_ok.clicked.connect(self.ok_button)

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
                "nq" : False
            }
        }
        self.selected_a_file = False

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

    def ok_button(self):
        if self.mode == "CSV":
            self.methods["csv"]["default"] = True if self.ui.radioButton_csv.isChecked() else False
            self.methods["csv"]["nq"] = True if self.ui.radioButton_nq.isChecked() else False

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
                json_match = re.search(fr"^.*[/\\](.*\.json|.*\.csv)$", self.filepaths[0])
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
            for file in self.filepaths:
                self.pairs.extend(pair_import.pair_import(file))
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


class SeekWidget(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SeekWidget, self).__init__(parent)
        self.ui = Ui_Seek()
        self.ui.setupUi(self)

        self.ui.pushButton_ok.clicked.connect(self.ok_press)
        self.ui.pushButton_cancel.clicked.connect(self.cancel_press)

        self.ui.spinBox_seek_value.setMaximum(window.the_game.max_question)
        self.ui.spinBox_seek_value.setValue(window.the_game.current_question)
        self.seek_value = self.ui.spinBox_seek_value.value()
        self.user_entered_number = False

    def ok_press(self):
        self.seek_value = self.ui.spinBox_seek_value.value()  # refresh
        self.user_entered_number = True
        self.hide()
        window.correct_checkbutton_mc(f"seek {self.seek_value}")

    def cancel_press(self):
        self.user_entered_number = False
        self.hide()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_Luupycards()
        self.ui.setupUi(self)

        ## setting up
        # gameplay stuff
        self.the_game = gameplay.MainGameplay([{"question" : "Please open a file.", "answer": "Please open a file."}])
        self.pairs = list()
        self.ui.tab_play.setEnabled(False)  # this is enabled by the game setup thingy
        self.current_mode = "Unset"
        self.current_order = "Unset"

        # options
        self.reload_settings()
        self.game_options = core.get_options()
        
        ## Buttons
        # Quit buttons
        self.ui.button_quit.clicked.connect(self.quit_action)
        self.ui.actionQuit.triggered.connect(self.quit_action)

        self.ui.actionOpen.triggered.connect(self.open_dir_dialog)  # file buttons
        self.ui.button_play.clicked.connect(self.gameplay_setup)  # Start playing
        self.ui.button_check.clicked.connect(self.correct_checkbutton)  # check button
        self.ui.pushButton_check_mc.clicked.connect(self.correct_checkbutton_mc)  # check button mc

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

        # font changes
        self.ui.actionBig_mode.triggered.connect(self.big_font_mode)

        self.ui.actionTest_trigger.triggered.connect(self.test_trigger)
        self.ui.actionOpen_Advanced.triggered.connect(self.advanced_import)

        # inspector
        self.ui.actionSave.triggered.connect(self.pair_inspector_save_to_file)
        self.ui.button_save_file.clicked.connect(self.pair_inspector_save_to_file)
        self.ui.button_save_memory.clicked.connect(self.pair_inspector_save_to_memory)
        self.ui.pushButton_new_row.clicked.connect(self.pair_inspector_add_row)
        self.ui.pushButton_delete_row.clicked.connect(self.pair_inspector_remove_row)
        self.pair_widget_items = {
            "question" : [],
            "answer" : [],
        }
        self.pair_inspector_load()

        mainlog.info("Set up class init.")

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

    def correct_checkbutton(self):
        line_text = self.ui.lineEdit_answer.text()
        if line_text:
            self.reload_settings()
            self.the_game.user_input = line_text.lower()
            result = self.the_game.answer_check_gui(line_text)

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
                case "quit":
                    self.ui.tab_main.setCurrentWidget(self.ui.tab_main_menu)
                    self.ui.tab_play.setEnabled(False)
                    self.ui.label_game_info.setText("Quitting...")
                    self.ui.label_game_info_mc.setText("Quitting...")
                case "empty field":  # this shouldn't appear though
                    self.set_info("This shouldn't appear. Please inform if this appears.")
                    mainlog.error("Empty field appeared!")
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

            self.set_question("")
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

                self.set_question("")
                self.set_question(self.the_game.play_gui())
            case "wrong":
                self.set_info(result[1])

    def open_dir_dialog(self):
        self.pairs.clear()
        pair_import = core.PairImport()
        file_paths = QtWidgets.QFileDialog.getOpenFileNames(self, "Open Pair File", "pair_file", "Pair files (*.json *.csv)")
        if file_paths[0]:
            print(file_paths[0])
            for file in file_paths[0]:
                self.pairs.extend(pair_import.determine_pair_file(file))
                mainlog.debug("self.pairs now has %s pair(s)", len(self.pairs))
                json_match = re.search(fr"^.*[/\\](.*\.json|.*\.csv)$", file)
                self.ui.label_pair_status.setText(f"Loaded {len(self.pairs) -1} pairs from {json_match.group(1)}.")

        self.pair_inspector_load()

    @staticmethod
    def quit_action():
        exit()

    def set_streak(self):
        streak = self.the_game.streak_current
        streak_all = self.the_game.streak_all_time

        self.ui.label_streak.setText(f"Current streak: {streak}")
        self.ui.label_streak_mc.setText(f"Current streak: {streak}")

        self.ui.label_streak.setToolTip(f"Current streak: {streak}, All time streak: {streak_all}")
        self.ui.label_streak_mc.setToolTip(f"Current streak: {streak}, All time streak: {streak_all}")

        self.ui.label_streak.setStatusTip(f"Current streak: {streak}, All time streak: {streak_all}")
        self.ui.label_streak_mc.setStatusTip(f"Current streak: {streak}, All time streak: {streak_all}")

    def set_question(self, question):
        self.ui.label_question.setText(question)
        self.ui.label_question_mc.setText(question)

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
            button.setText(choice)

        self.big_font_mode()  # ensures the buttons get big font

    def seek_mc(self):
        seek = SeekWidget(self)
        seek.show()

    def correct_mc(self):
        self.correct_checkbutton_mc("correct")

    def gameplay_setup(self):
        if self.pairs:
            mainlog.info("Creating gameplay...")
            # determine mode
            self.current_mode = self.ui.comboBox_modes.currentText()
            self.current_order = self.ui.comboBox_question_order.currentText()

            # pair lengths so that user can only change then after gameplay has been initialized
            #if core.settings_value_manipulator("max question") > len(self.pairs) - 1:
            core.settings_value_manipulator("max question", "dump", len(self.pairs) - 1)
            #if core.settings_value_manipulator("min question") > core.settings_value_manipulator("max question"):
            core.settings_value_manipulator("min question", "dump", 1)
                
            self.reload_settings()

            # set tab to play
            self.ui.tab_main.setCurrentWidget(self.ui.tab_play)
            if self.current_mode in ["Multiple Choice", "Multiple Choice Reverse"]:
                self.ui.stackedWidget_gameplay.setCurrentWidget(self.ui.multiple_choice)
            else:
                self.ui.stackedWidget_gameplay.setCurrentWidget(self.ui.input)
            self.ui.action_tabls_play.setEnabled(True)
            self.ui.tab_play.setEnabled(True)

            print(self.current_mode, self.current_order)  # then pass to backend
            self.the_game = gameplay.determine_gamemode(self.current_mode, self.current_order, self.pairs, self.ui.checkBox_question_flip.isChecked())

            self.set_streak()
            self.set_question(self.the_game.play_gui())

            # Then back to finish mc and s!
            if self.current_mode in ["Multiple Choice", "Multiple Choice Reverse"]:
                self.spawn_mc_buttons()
            elif self.current_mode == "Survive!":
                self.ui.label_lives.setText(f"Lives left: {self.the_game.lives}")
            else:
                self.ui.label_lives.setText("")

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
        are_you_sure = QtWidgets.QMessageBox(self)
        are_you_sure.setText("Are you sure you want to reset all the settings?")
        are_you_sure.setInformativeText("Your all time streaks will be reset!")
        are_you_sure.setStandardButtons(QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.Cancel)
        are_you_sure.exec()

        if are_you_sure.buttonClicked:
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
        self.check_invalid_settings()
        core.get_options("dump", self.game_options)
        mainlog.info("Saved settings")
        self.reload_settings()
        mainlog.info("Reloaded settings")

    def check_invalid_settings(self):
        options_orig = core.get_options()

        if self.game_options["min question"] > self.game_options["max question"]:
            self.game_options["max question"] = self.game_options["min question"]
        if self.pairs:
            if self.game_options["max question"] > len(self.pairs):
                self.game_options["max question"] = len(self.pairs) -1

        if options_orig != self.game_options:
            mainlog.warning("Found illegal settings values, fixing...")

    def pair_inspector_load(self):
        pair0 = {
            "question": ["Wait... question zero? What's the answer though..."],
            "answer": ["Luupycards"],
        }
        if self.pairs:
            if self.pairs[0] == pair0:
                self.pairs.pop(0)

        for _ in range(self.ui.tableWidget.rowCount()):  # first remove all old rows
            self.ui.tableWidget.removeRow(0)

        for i, pair in enumerate(self.pairs):
            self.ui.tableWidget.insertRow(i)

            question = QtWidgets.QTableWidgetItem()
            question.setText(";".join(pair["question"]))

            answer = QtWidgets.QTableWidgetItem()
            answer.setText(";".join(pair["answer"]))

            self.ui.tableWidget.setItem(i, 0, question)  # questions
            self.ui.tableWidget.setItem(i, 1, answer)  # answers

            self.pair_widget_items["question"].append(question)
            self.pair_widget_items["answer"].append(answer)


        # after everything is done adds the pair back
        if self.pairs:
            if self.pairs[0] != pair0:
                self.pairs.insert(0, pair0)

    def pair_inspector_save_to_memory(self):
        self.pairs.clear()

        for (question, answer) in zip(self.pair_widget_items["question"], self.pair_widget_items["answer"]):
            self.pairs.append(
                {
                    "question" : question.text().split(";"),
                    "answer" : answer.text().split(";"),
                }
            )

        # after everything is done adds the pair back
        pair0 = {
            "question": ["Wait... question zero? What's the answer though..."],
            "answer": ["Luupycards"],
        }
        self.pairs.insert(0, pair0)

    def pair_inspector_save_to_file(self):
        file_pairs = []

        for (question, answer) in zip(self.pair_widget_items["question"], self.pair_widget_items["answer"]):
            if question or answer:
                file_pairs.append(
                    {
                        "question": question.text().split(";"),
                        "answer": answer.text().split(";"),
                    }
                )

        full_json_file = {
            "pairs" : file_pairs
        }

        filepath = QtWidgets.QFileDialog.getSaveFileName(self, "Save Pair File", "new_pair_file.json", "Pair file (*.json)")
        filepath = filepath[0]  # only the file path

        if filepath:  # ensures user chose a location
            with open(filepath, "w") as file:
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

        self.pair_widget_items["question"].append(question)
        self.pair_widget_items["answer"].append(answer)

    def pair_inspector_remove_row(self):
        last_row = self.ui.tableWidget.rowCount() -1

        self.ui.tableWidget.removeRow(last_row)

        if self.pair_widget_items["question"]:
            self.pair_widget_items["question"].pop(-1)
            self.pair_widget_items["answer"].pop(-1)


if __name__ == "__main__":
    if os.name == "nt":
        mainlog.critical("Warning! This program is intended for Linux, using Windows WILL have unexpected behaviour!")
    app = QtWidgets.QApplication(sys.argv)
    #app.setStyle('Breeze')  # I'll set it properly later
    style_name = app.style().metaObject().className()
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

    sys.exit(app.exec())