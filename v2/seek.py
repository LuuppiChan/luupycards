# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'seek.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QVBoxLayout,
    QWidget)

class Ui_Seek(object):
    def setupUi(self, Seek):
        if not Seek.objectName():
            Seek.setObjectName(u"Seek")
        Seek.resize(289, 196)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Seek.sizePolicy().hasHeightForWidth())
        Seek.setSizePolicy(sizePolicy)
        Seek.setMaximumSize(QSize(289, 196))
        font = QFont()
        font.setPointSize(16)
        Seek.setFont(font)
        self.verticalLayout = QVBoxLayout(Seek)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_static_eqn = QLabel(Seek)
        self.label_static_eqn.setObjectName(u"label_static_eqn")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_static_eqn.sizePolicy().hasHeightForWidth())
        self.label_static_eqn.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.label_static_eqn, 0, Qt.AlignHCenter)

        self.spinBox_seek_value = QSpinBox(Seek)
        self.spinBox_seek_value.setObjectName(u"spinBox_seek_value")
        self.spinBox_seek_value.setMaximum(999999)
        self.spinBox_seek_value.setValue(1)

        self.verticalLayout.addWidget(self.spinBox_seek_value)

        self.label_question = QLabel(Seek)
        self.label_question.setObjectName(u"label_question")
        font1 = QFont()
        font1.setPointSize(12)
        self.label_question.setFont(font1)

        self.verticalLayout.addWidget(self.label_question)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_cancel = QPushButton(Seek)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")

        self.horizontalLayout.addWidget(self.pushButton_cancel)

        self.pushButton_ok = QPushButton(Seek)
        self.pushButton_ok.setObjectName(u"pushButton_ok")

        self.horizontalLayout.addWidget(self.pushButton_ok)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Seek)

        QMetaObject.connectSlotsByName(Seek)
    # setupUi

    def retranslateUi(self, Seek):
        Seek.setWindowTitle(QCoreApplication.translate("Seek", u"Form", None))
        self.label_static_eqn.setText(QCoreApplication.translate("Seek", u"Enter question number", None))
        self.label_question.setText(QCoreApplication.translate("Seek", u"Question: ", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Seek", u"Cancel", None))
        self.pushButton_ok.setText(QCoreApplication.translate("Seek", u"Ok", None))
    # retranslateUi

