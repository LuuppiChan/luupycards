# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'import.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QHBoxLayout, QLabel, QPushButton, QRadioButton,
    QScrollArea, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_DialogImport(object):
    def setupUi(self, DialogImport):
        if not DialogImport.objectName():
            DialogImport.setObjectName(u"DialogImport")
        DialogImport.resize(488, 431)
        font = QFont()
        font.setPointSize(16)
        DialogImport.setFont(font)
        self.verticalLayout_2 = QVBoxLayout(DialogImport)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.scrollArea = QScrollArea(DialogImport)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 458, 975))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")
        self.label.setScaledContents(False)
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.comboBox_import = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_import.addItem("")
        self.comboBox_import.addItem("")
        self.comboBox_import.setObjectName(u"comboBox_import")

        self.verticalLayout.addWidget(self.comboBox_import)

        self.verticalLayout_csv = QVBoxLayout()
        self.verticalLayout_csv.setObjectName(u"verticalLayout_csv")
        self.radioButton_csv = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_csv.setObjectName(u"radioButton_csv")
        self.radioButton_csv.setChecked(True)

        self.verticalLayout_csv.addWidget(self.radioButton_csv)

        self.radioButton_alternative = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_alternative.setObjectName(u"radioButton_alternative")

        self.verticalLayout_csv.addWidget(self.radioButton_alternative)

        self.radioButton_nq = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_nq.setObjectName(u"radioButton_nq")

        self.verticalLayout_csv.addWidget(self.radioButton_nq)


        self.verticalLayout.addLayout(self.verticalLayout_csv)

        self.verticalLayout_json = QVBoxLayout()
        self.verticalLayout_json.setObjectName(u"verticalLayout_json")
        self.checkBox_json = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_json.setObjectName(u"checkBox_json")
        self.checkBox_json.setChecked(True)

        self.verticalLayout_json.addWidget(self.checkBox_json)

        self.checkBox_jp = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_jp.setObjectName(u"checkBox_jp")

        self.verticalLayout_json.addWidget(self.checkBox_jp)

        self.checkBox_sentences = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_sentences.setObjectName(u"checkBox_sentences")

        self.verticalLayout_json.addWidget(self.checkBox_sentences)


        self.verticalLayout.addLayout(self.verticalLayout_json)

        self.verticalSpacer = QSpacerItem(50, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.verticalLayout_nq = QVBoxLayout()
        self.verticalLayout_nq.setObjectName(u"verticalLayout_nq")
        self.label_nq = QLabel(self.scrollAreaWidgetContents)
        self.label_nq.setObjectName(u"label_nq")

        self.verticalLayout_nq.addWidget(self.label_nq)

        self.checkBox_nq_hiragana = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_nq_hiragana.setObjectName(u"checkBox_nq_hiragana")
        self.checkBox_nq_hiragana.setChecked(False)

        self.verticalLayout_nq.addWidget(self.checkBox_nq_hiragana)

        self.checkBox_nq_katakana = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_nq_katakana.setObjectName(u"checkBox_nq_katakana")
        self.checkBox_nq_katakana.setChecked(False)

        self.verticalLayout_nq.addWidget(self.checkBox_nq_katakana)

        self.checkBox_nq_radical = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_nq_radical.setObjectName(u"checkBox_nq_radical")
        self.checkBox_nq_radical.setChecked(False)

        self.verticalLayout_nq.addWidget(self.checkBox_nq_radical)

        self.checkBox_nq_kanji = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_nq_kanji.setObjectName(u"checkBox_nq_kanji")
        self.checkBox_nq_kanji.setChecked(False)

        self.verticalLayout_nq.addWidget(self.checkBox_nq_kanji)

        self.checkBox_nq_vocabulary_meaning = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_nq_vocabulary_meaning.setObjectName(u"checkBox_nq_vocabulary_meaning")
        self.checkBox_nq_vocabulary_meaning.setChecked(True)

        self.verticalLayout_nq.addWidget(self.checkBox_nq_vocabulary_meaning)

        self.checkBox_nq_vocabulary = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_nq_vocabulary.setObjectName(u"checkBox_nq_vocabulary")
        self.checkBox_nq_vocabulary.setChecked(True)

        self.verticalLayout_nq.addWidget(self.checkBox_nq_vocabulary)

        self.checkBox_nq_pronunciation = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_nq_pronunciation.setObjectName(u"checkBox_nq_pronunciation")
        self.checkBox_nq_pronunciation.setChecked(True)

        self.verticalLayout_nq.addWidget(self.checkBox_nq_pronunciation)


        self.verticalLayout.addLayout(self.verticalLayout_nq)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_2.addWidget(self.scrollArea)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_cancel = QPushButton(DialogImport)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")

        self.horizontalLayout.addWidget(self.pushButton_cancel)

        self.pushButton_ok = QPushButton(DialogImport)
        self.pushButton_ok.setObjectName(u"pushButton_ok")

        self.horizontalLayout.addWidget(self.pushButton_ok)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(DialogImport)

        QMetaObject.connectSlotsByName(DialogImport)
    # setupUi

    def retranslateUi(self, DialogImport):
        DialogImport.setWindowTitle(QCoreApplication.translate("DialogImport", u"Choose Import Method", None))
        self.label.setText(QCoreApplication.translate("DialogImport", u"Choose an import method (Hover to see an example or go to the help on main window)", None))
        self.comboBox_import.setItemText(0, QCoreApplication.translate("DialogImport", u"CSV", None))
        self.comboBox_import.setItemText(1, QCoreApplication.translate("DialogImport", u"JSON", None))

#if QT_CONFIG(tooltip)
        self.radioButton_csv.setToolTip(QCoreApplication.translate("DialogImport", u"question1\n"
"answer1,answer1a,answer1b\n"
"question2\n"
"answer2", None))
#endif // QT_CONFIG(tooltip)
        self.radioButton_csv.setText(QCoreApplication.translate("DialogImport", u"Default", None))
#if QT_CONFIG(tooltip)
        self.radioButton_alternative.setToolTip(QCoreApplication.translate("DialogImport", u"<html><head/><body><p>This is a more common alternative csv format:<br/>question1,answer1a,answer1b,answer1c<br/>question2,answer2</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.radioButton_alternative.setText(QCoreApplication.translate("DialogImport", u"Alternative", None))
#if QT_CONFIG(tooltip)
        self.radioButton_nq.setToolTip(QCoreApplication.translate("DialogImport", u"<html><head/><body><p>Take the vocabulary.csv from the game files and choose it.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.radioButton_nq.setText(QCoreApplication.translate("DialogImport", u"Nihongo Quest (W.I.P.)", None))
#if QT_CONFIG(tooltip)
        self.checkBox_json.setToolTip(QCoreApplication.translate("DialogImport", u"\"some pairs\" doesn't matter, it's a placeholder and there can be any name or even multiple lists\n"
"You'll have to implement the \"question\" and \"answer\" fields accordingly.\n"
"{\n"
"    \"some pairs\": [\n"
"        {\n"
"            \"question\": [\"question1\"],\n"
"            \"answer\": [\"answer1\", \"answer1a\", \"answer1b\"]\n"
"        },\n"
"        {\n"
"            \"question\": [\"question2\"],\n"
"            \"answer\": [\"answer2\"]\n"
"        }\n"
"    ]\n"
"}", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_json.setText(QCoreApplication.translate("DialogImport", u"Default", None))
#if QT_CONFIG(tooltip)
        self.checkBox_jp.setToolTip(QCoreApplication.translate("DialogImport", u"\"some pairs\" doesn't matter, it's a placeholder and there can be any name or even multiple lists\n"
"This will create a question for meaning and pronunciation\n"
"You will have to create \"question\", \"answer\" and \"pronunciation\" fields accordingly.\n"
"{\n"
"    \"some pairs\": [\n"
"        {\n"
"            \"question\": [\"\u4e00\"],\n"
"            \"answer\": [\"one\", \"1\"],\n"
"            \"pronunciation\": [\"\u3044\u3061\"]\n"
"        },\n"
"        {\n"
"            \"question\": [\"\u56db\"],\n"
"            \"answer\": [\"two\", \"2\"],\n"
"            \"pronunciation\": [\"\u3057\", \"\u3088\u3093\"]\n"
"        }\n"
"    ]\n"
"}", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_jp.setText(QCoreApplication.translate("DialogImport", u"Japan", None))
#if QT_CONFIG(tooltip)
        self.checkBox_sentences.setToolTip(QCoreApplication.translate("DialogImport", u"\"some pairs\" doesn't matter, it's a placeholder and there can be any name or even multiple lists\n"
"This will create a question for meaning and pronunciation\n"
"You will have to create a sentence block and the fields in it, other fields don't have to be implemented unless you check them on the menu.\n"
"{\n"
"    \"some pairs\": [\n"
"        {\n"
"            {\n"
"                \"sentence\": \"\u304a\u7236\u3055\u3093\u306f\u60aa\u304f\u306a\u304b\u3063\u305f\u3002\",\n"
"                \"answer\": \"As for Father, he was not bad.\"\n"
"            }\n"
"        },\n"
"        {\n"
"            \"sentences\": [\n"
"                {\n"
"                    \"sentence\": \"\u6628\u65e5\u306f\u697d\u3057\u304f\u306a\u3063\u305f\u3002\",\n"
"                    \"answer\": \"As for yesterday, it was not fun.\"\n"
"                }\n"
"            ]\n"
"        }\n"
"    ]\n"
"}", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_sentences.setText(QCoreApplication.translate("DialogImport", u"Sentences", None))
        self.label_nq.setText(QCoreApplication.translate("DialogImport", u"What categories to add?", None))
#if QT_CONFIG(tooltip)
        self.checkBox_nq_hiragana.setToolTip(QCoreApplication.translate("DialogImport", u"Add all of Hiragana.\n"
"Example: \u3042 - a", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.checkBox_nq_hiragana.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.checkBox_nq_hiragana.setText(QCoreApplication.translate("DialogImport", u"Hiragana", None))
#if QT_CONFIG(tooltip)
        self.checkBox_nq_katakana.setToolTip(QCoreApplication.translate("DialogImport", u"Add all of Katakana.\n"
"Example: \u30a2 - a", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_nq_katakana.setText(QCoreApplication.translate("DialogImport", u"Katakana", None))
#if QT_CONFIG(tooltip)
        self.checkBox_nq_radical.setToolTip(QCoreApplication.translate("DialogImport", u"Add all of radicals.\n"
"Example: \u4e00 - one", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_nq_radical.setText(QCoreApplication.translate("DialogImport", u"Radical", None))
#if QT_CONFIG(tooltip)
        self.checkBox_nq_kanji.setToolTip(QCoreApplication.translate("DialogImport", u"Add all of kanji.\n"
"Example: \u4e01 - street", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_nq_kanji.setText(QCoreApplication.translate("DialogImport", u"Kanji", None))
#if QT_CONFIG(tooltip)
        self.checkBox_nq_vocabulary_meaning.setToolTip(QCoreApplication.translate("DialogImport", u"Add all of vocabulary meaning.\n"
"Example: \u4e00 - one - \u3044\u3061", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_nq_vocabulary_meaning.setText(QCoreApplication.translate("DialogImport", u"Vocab Meaning", None))
#if QT_CONFIG(tooltip)
        self.checkBox_nq_vocabulary.setToolTip(QCoreApplication.translate("DialogImport", u"Add all of vocabulary.\n"
"Example: \u304f\u3093 - casual male suffix", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_nq_vocabulary.setText(QCoreApplication.translate("DialogImport", u"Vocabulary", None))
#if QT_CONFIG(tooltip)
        self.checkBox_nq_pronunciation.setToolTip(QCoreApplication.translate("DialogImport", u"Includes the reading of items that have a reading.", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_nq_pronunciation.setText(QCoreApplication.translate("DialogImport", u"Pronunciation", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("DialogImport", u"Cancel", None))
        self.pushButton_ok.setText(QCoreApplication.translate("DialogImport", u"Ok", None))
    # retranslateUi

