# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'licence.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QScrollArea, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_licence(object):
    def setupUi(self, licence):
        if not licence.objectName():
            licence.setObjectName(u"licence")
        licence.resize(747, 584)
        font = QFont()
        font.setPointSize(12)
        licence.setFont(font)
        self.verticalLayout = QVBoxLayout(licence)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = QScrollArea(licence)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 717, 827))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_licence = QLabel(self.scrollAreaWidgetContents)
        self.label_licence.setObjectName(u"label_licence")
        self.label_licence.setWordWrap(True)
        self.label_licence.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

        self.verticalLayout_2.addWidget(self.label_licence)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(licence)

        QMetaObject.connectSlotsByName(licence)
    # setupUi

    def retranslateUi(self, licence):
        licence.setWindowTitle(QCoreApplication.translate("licence", u"MIT Licence", None))
        self.label_licence.setText(QCoreApplication.translate("licence", u"<html><head/><body><p>MIT License</p><p><br/></p><p>Copyright (c) 2025 Luuppi</p><p><br/></p><p>Permission is hereby granted, free of charge, to any person obtaining a copy</p><p>of this software and associated documentation files (the &quot;Software&quot;), to deal</p><p>in the Software without restriction, including without limitation the rights</p><p>to use, copy, modify, merge, publish, distribute, sublicense, and/or sell</p><p>copies of the Software, and to permit persons to whom the Software is</p><p>furnished to do so, subject to the following conditions:</p><p><br/></p><p>The above copyright notice and this permission notice shall be included in all</p><p>copies or substantial portions of the Software.</p><p><br/></p><p>THE SOFTWARE IS PROVIDED &quot;AS IS&quot;, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR</p><p>IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,</p><p>FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE</p><p>AUTHORS OR COPYRIGHT HOLDERS BE LIA"
                        "BLE FOR ANY CLAIM, DAMAGES OR OTHER</p><p>LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,</p><p>OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE</p><p>SOFTWARE.</p></body></html>", None))
    # retranslateUi

