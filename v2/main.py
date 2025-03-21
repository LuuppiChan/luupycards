#!/bin/python
import re
import os
import sys
import shutil
import logging
import argparse
from pathlib import Path

from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtGui

import core_functions as core
import gameplay_modules as gameplay
from seek import Ui_Seek

if True:  # Because of PEP8
    os.system("pyside6-uic main.ui -o ui.py")  # recreates this file automatically
    from ui import Ui_Luupycards  # this loads the ui

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


class SeekWidget(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SeekWidget, self).__init__(parent)
        self.ui = Ui_Seek()
        self.ui.setupUi(self)

        self.ui.pushButton_ok.clicked.connect(self.ok_press)
        self.ui.pushButton_cancel.clicked.connect(self.cancel_press)

        self.ui.spinBox_seek_value.setMaximum(window.the_game.max_question)
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

        mainlog.info("Set up class init.")

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
            self.ui.label_question_mc.setText("")
            self.ui.label_question.setText("")

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
                self.ui.label_game_info_mc.setText("Quitting...")
            case "empty field":
                self.set_info("Please choose an option...")
            case "wrong":
                self.set_info(result[1])

    def open_dir_dialog(self):
        file_path = QtWidgets.QFileDialog.getOpenFileName(self, "Open Pair File", "pair_file", "Pair files (*.json *.csv)")
        if file_path[0]:
            print(file_path[0])
            self.pairs = core.determine_pair_file(file_path[0])
            json_match = re.search(fr"^.*[/\\](.*\.json|.*\.csv)$", file_path[0])
            self.ui.label_pair_status.setText(f"Loaded {len(self.pairs) -1} pairs from {json_match.group(1)}.")
            pairs = list()

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

            # pair lengths
            if core.settings_value_manipulator("max question") > len(self.pairs) - 1:
                core.settings_value_manipulator("max question", "dump", len(self.pairs) - 1)
            if core.settings_value_manipulator("min question") > core.settings_value_manipulator("max question"):
                core.settings_value_manipulator("min question", "dump", 1)
                
            self.reload_settings()

            # set tab to play
            self.ui.tab_main.setCurrentWidget(self.ui.tab_play)
            if self.current_mode == "Multiple Choice":
                self.ui.stackedWidget_gameplay.setCurrentWidget(self.ui.multiple_choice)
            else:
                self.ui.stackedWidget_gameplay.setCurrentWidget(self.ui.input)
            self.ui.action_tabls_play.setEnabled(True)
            self.ui.tab_play.setEnabled(True)

            print(self.current_mode, self.current_order)  # then pass to backend
            self.the_game = gameplay.determine_gamemode(self.current_mode, self.current_order, self.pairs)

            self.set_streak()
            self.set_question(self.the_game.play_gui())

            # Then back to finish mc and s!
            if self.current_mode == "Multiple Choice":
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
