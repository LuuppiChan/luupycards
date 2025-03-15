#!/bin/python
if                                          'ArchBTW':
                                            import os \
                                           ; import sys\
                                         ; import  shutil\
                                        ; import  logging \
                                      ;  import   argparse  \
                                     ; from pathlib  import  \
                                   Path    ;   from    PySide6 \
                                  import QtWidgets    ;   from  \
                                PySide6     import   QtCore;  from\
                               PySide6    import  QtGui ;   import \
                             core_functions   as core    ;    import \
                            gameplay_modules    as   gameplay         \
                          ;os.system("pyside6-uic main.ui -o ui.py"  )  \
                         ; from  ui  import              Ui_Luupycards  \
                       ;parser = argparse.                ArgumentParser  (
                      description       =                  "Simple flip card \
                    program. (GUI!)")   ;                  (parser.add_argument
                  ("-debug", type = str ,                  default = "critical",
                required = False                               ,   help   =     \
              "Choose logging                                       level (debug, \
           info, error                                                   or critical\
       (default))"                                                           )); args\
     = parser                                                                . parse_args()


match args.debug:
    case "debug":
        log_level = logging.DEBUG
    case "info":
        log_level = logging.INFO
    case "error":
        log_level = logging.ERROR
    case "critical" | _:
        log_level = logging.CRITICAL

mainlog = logging.getLogger(__name__)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self): super(MainWindow, self).__init__(); self.ui = Ui_Luupycards(); self.ui.setupUi(self); self.the_game = gameplay.MainGameplay([{"question": "Please open a file.", "answer": "Please open a file."}]); self.pairs = list(); self.ui.tab_play.setEnabled(False); self.reload_settings(); self.game_options = core.get_options(); self.ui.button_quit.clicked.connect(self.quit_action); self.ui.actionQuit.triggered.connect(self.quit_action); self.ui.actionOpen.triggered.connect(self.open_dir_dialog); self.ui.button_play.clicked.connect(self.gameplay_setup); self.ui.button_check.clicked.connect(self.correct_checkbutton); self.ui.pushButton_check_mc.clicked.connect(self.correct_checkbutton); self.ui.button_settings_reset_2.clicked.connect(self.reset_settings); self.ui.button_settings_save_2.clicked.connect(self.save_settings); mainlog.info("Set up class init.")
    def correct_checkbutton(self): line_text = self.ui.lineEdit_answer.text(); self.the_game.user_input = line_text if line_text else None; result = self.the_game.answer_check_gui(line_text) if line_text else None; self.set_info(result[1]) if line_text else None; self.set_question(self.the_game.print_question()) if line_text else None; self.ui.lineEdit_answer.clear() if line_text else mainlog.info("Empty button press.")
    def open_dir_dialog(self):
        file_path = QtWidgets.QFileDialog.getOpenFileName(self, "Open Pair File", "pair_file","Pair files (*.json *.csv)"); print(file_path[0]); self.pairs = core.determine_pair_file(file_path[0]) if file_path[0] else None
    def quit_action(self):exit()
    def set_streak(self, streak): self.ui.label_streak = streak; self.ui.label_streak_mc = streak
    def set_question(self, question): self.ui.label_question.setText(question); self.ui.label_question_mc.setText(question)
    def set_info(self, info): self.ui.label_game_info.setText(info); self.ui.label_game_info_mc.setText(info)
    def gameplay_setup(self):
        if self.pairs: mainlog.info("Creating gameplay..."); current_mode = self.ui.comboBox_modes.currentText(); current_order = self.ui.comboBox_question_order.currentText(); self.ui.tab_main.setCurrentWidget(self.ui.tab_play); self.ui.stackedWidget_gameplay.setCurrentWidget(self.ui.multiple_choice) if current_mode == "Multiple Choice" else self.ui.stackedWidget_gameplay.setCurrentWidget(self.ui.input); self.ui.action_tabls_play.setEnabled(True); self.ui.tab_play.setEnabled(True); self.ui.label_lives.setText("Lives: 5") if current_mode == "Survive!" else self.ui.label_lives.setText(""); print(current_mode, current_order); self.the_game = gameplay.determine_gamemode(current_mode, current_order, self.pairs); self.set_streak(self.the_game.streak_current); self.set_question(self.the_game.print_question())
        else: mainlog.info("No pairs detected."); QtWidgets.QMessageBox.warning(self, "Pair error!", "Please import pairs before you start playing!\nFile -> Open")
    def reload_settings(self): self.game_options = core.get_options("load"); options = self.game_options; self.ui.all_time_streak_value_2.setText(str(options["all time streak"])); self.ui.all_time_survival_streak_value_2.setText(str(options["all time survival streak"])); self.ui.reset_all_time_streak_value_2.setChecked(options["reset all time streak"]); self.ui.reset_all_time_survival_streak_value_2.setChecked(options["reset all time survival streak"]); self.ui.min_question_value_2.setValue(options["min question"]); self.ui.max_question_value_2.setValue(options["max question"]); self.ui.show_current_question_number_value_2.setChecked(options["show current question number"]); self.ui.multiple_choice_max_options_value_2.setValue(options["multiple choice max options"]); self.ui.lives_value_2.setValue(options["lives"]); self.ui.fuzzy_select_precent_value_2.setValue(options["fuzzy select percent"])
    def reset_settings(self):
        are_you_sure = QtWidgets.QMessageBox(self); are_you_sure.setText("Are you sure you want to reset all the settings?"); are_you_sure.setInformativeText("Your all time streaks will be reset!"); are_you_sure.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel); are_you_sure.exec()
        if are_you_sure.buttonClicked: script_dir = os.path.dirname(os.path.abspath(__file__)); settings_path = os.path.join(script_dir, "settings.json"); home_dir = Path.home(); static_path = f"{home_dir}/.cache/luupycards"; settings_filename = "settings.json"; static_settings_path = os.path.join(static_path, settings_filename); os.makedirs(static_path, exist_ok=True); shutil.copy(settings_path, static_settings_path); mainlog.info("Reset settings"); self.reload_settings(); mainlog.info("Reloaded settings")
    def save_settings(self): self.game_options["all time streak"] = int(self.ui.all_time_streak_value_2.text()); self.game_options["all time survival streak"] = int(self.ui.all_time_survival_streak_value_2.text()); self.game_options["reset all time streak"] = self.ui.reset_all_time_streak_value_2.isChecked(); self.game_options["reset all time survival streak"] = self.ui.reset_all_time_survival_streak_value_2.isChecked(); self.game_options["min question"] = self.ui.min_question_value_2.value(); self.game_options["max question"] = self.ui.max_question_value_2.value(); self.game_options["show current question number"] = self.ui.show_current_question_number_value_2.isChecked(); self.game_options["multiple choice max options"] = self.ui.multiple_choice_max_options_value_2.value(); self.game_options["lives"] = self.ui.lives_value_2.value(); self.game_options["fuzzy select percent"] = self.ui.fuzzy_select_precent_value_2.value(); core.static_value_functions_gui(); self.check_invalid_settings(); core.get_options("dump", self.game_options); mainlog.info("Saved settings"); self.reload_settings(); mainlog.info("Reloaded settings")
    def check_invalid_settings(self):
                            options_orig = core.get_options(); self.game_options["max question"] = self.game_options["min question"] if self.game_options["min question"] > self.game_options["max question"] else None
                            if self.pairs: self.game_options["max question"] = len(self.pairs) - 1 if self.game_options["max question"] > len(self.pairs) else None; mainlog.warning("Found illegal settings values, fixing...") if options_orig != self.game_options else None


if __name__ == "__main__":
    mainlog.critical("Warning! This program is intended for Linux, using Windows WILL have unexpected behaviour!") if os.name == "nt" else None; app = QtWidgets.QApplication(sys.argv); style_name = app.style().metaObject().className()
    if style_name == "QFusionStyle": palette = QtGui.QPalette(); palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53)); palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white); palette.setColor(QtGui.QPalette.Base, QtGui.QColor(53, 53, 53)); palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53)); palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.black); palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white); palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white); palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53)); palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white); palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red); palette.setColor(QtGui.QPalette.Link, QtGui.QColor(218, 130, 218)); palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(218, 130, 218)); palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black); app.setPalette(palette); pass; window = MainWindow(); window.show(); sys.exit(app.exec())
