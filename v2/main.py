import os
import sys
import logging
import argparse

from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtGui

import core_functions as core
import gameplay_modules as gameplay

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
    case "critical" | _:  # the wild card is so that it won't warn me.
        log_level = logging.CRITICAL

# logging
mainlog = logging.getLogger(__name__)


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

        # options
        self.reload_settings()
        self.game_options = dict()
        
        ## Buttons
        # Quit buttons
        self.ui.button_quit.clicked.connect(self.quit_action)
        self.ui.actionQuit.triggered.connect(self.quit_action)

        self.ui.actionOpen.triggered.connect(self.open_dir_dialog)  # file buttons
        self.ui.button_play.clicked.connect(self.gameplay_setup)  # Start playing
        self.ui.button_check.clicked.connect(self.correct_checkbutton)  # check button
        self.ui.pushButton_check_mc.clicked.connect(self.correct_checkbutton)  # check button mc

        mainlog.info("Set up class init.")

    def correct_checkbutton(self):
        line_text = self.ui.lineEdit_answer.text()
        if line_text:
            self.the_game.user_input = line_text
            result = self.the_game.answer_check_gui(line_text)

            self.set_info(result[1])
            self.set_question(self.the_game.print_question())
            self.ui.lineEdit_answer.clear()

            match result[0]:
                case "correct":
                    pass
        else:
            mainlog.info("Empty button press.")

    def open_dir_dialog(self):
        file_path = QtWidgets.QFileDialog.getOpenFileName(self, "Open Pair File", "pair_file", "Pair files (*.json *.csv)")
        if file_path[0]:
            print(file_path[0])
            self.pairs = core.determine_pair_file(file_path[0])

    @staticmethod
    def quit_action():
        exit()

    def set_streak(self, streak):
        self.ui.label_streak = streak
        self.ui.label_streak_mc = streak

    def set_question(self, question):
        self.ui.label_question.setText(question)
        self.ui.label_question_mc.setText(question)

    def set_info(self, info):
        self.ui.label_game_info.setText(info)
        self.ui.label_game_info_mc.setText(info)

    def gameplay_setup(self):
        if self.pairs:
            mainlog.info("Creating gameplay...")
            # determine mode
            current_mode = self.ui.comboBox_modes.currentText()
            current_order = self.ui.comboBox_question_order.currentText()

            # set tab to play
            self.ui.tab_main.setCurrentWidget(self.ui.tab_play)
            if current_mode == "Multiple Choice":
                self.ui.stackedWidget_gameplay.setCurrentWidget(self.ui.multiple_choice)
            else:
                self.ui.stackedWidget_gameplay.setCurrentWidget(self.ui.input)
            self.ui.action_tabls_play.setEnabled(True)
            self.ui.tab_play.setEnabled(True)

            print(current_mode, current_order)  # then pass to backend
            self.the_game = gameplay.determine_gamemode(current_mode, current_order, self.pairs)

            self.set_streak(self.the_game.streak_current)
            self.set_question(self.the_game.print_question())
        else:
            mainlog.info("No pairs detected.")
            QtWidgets.QMessageBox.warning(self, "Pair error!", "Please import pairs before you start playing!")

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

    def save_settings(self):
        pass


if __name__ == "__main__":
    if os.name == "nt":
        mainlog.critical("Warning! This program is intended for Linux, using Windows WILL have unexpected behaviour!")
    app = QtWidgets.QApplication(sys.argv)
    #app.setStyle('Breeze')  # I'll set it properly later
    style_name = app.style().metaObject().className()
    if style_name == "QFusionStyle":
        palette = QtGui.QPalette()  # it works so it's fine
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
