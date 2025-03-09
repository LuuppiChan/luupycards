# For now this reloads the ui file
import os
os.system("pyside6-uic main.ui -o ui.py")  # recreates this file automatically

import sys

from PySide6 import QtUiTools
from PySide6 import QtWidgets
from PySide6 import QtCore

from ui import Ui_Luupycards


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_Luupycards()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Breeze')  # I'll set it properly later

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
