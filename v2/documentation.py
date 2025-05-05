# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'documentation.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QTabWidget,
    QVBoxLayout, QWidget)

class Ui_documentation(object):
    def setupUi(self, documentation):
        if not documentation.objectName():
            documentation.setObjectName(u"documentation")
        documentation.resize(734, 647)
        font = QFont()
        font.setPointSize(12)
        documentation.setFont(font)
        self.verticalLayout = QVBoxLayout(documentation)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(documentation)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_quickstart_2 = QWidget()
        self.tab_quickstart_2.setObjectName(u"tab_quickstart_2")
        self.verticalLayout_17 = QVBoxLayout(self.tab_quickstart_2)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.scrollArea_8 = QScrollArea(self.tab_quickstart_2)
        self.scrollArea_8.setObjectName(u"scrollArea_8")
        self.scrollArea_8.setWidgetResizable(True)
        self.scrollAreaWidgetContents_9 = QWidget()
        self.scrollAreaWidgetContents_9.setObjectName(u"scrollAreaWidgetContents_9")
        self.scrollAreaWidgetContents_9.setGeometry(QRect(0, 0, 684, 3591))
        self.verticalLayout_18 = QVBoxLayout(self.scrollAreaWidgetContents_9)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.label_11 = QLabel(self.scrollAreaWidgetContents_9)
        self.label_11.setObjectName(u"label_11")
        font1 = QFont()
        font1.setPointSize(20)
        self.label_11.setFont(font1)
        self.label_11.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.label_11.setWordWrap(True)
        self.label_11.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_18.addWidget(self.label_11)

        self.label_12 = QLabel(self.scrollAreaWidgetContents_9)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font)
        self.label_12.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.label_12.setWordWrap(True)
        self.label_12.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_18.addWidget(self.label_12)

        self.tabWidget_examples_2 = QTabWidget(self.scrollAreaWidgetContents_9)
        self.tabWidget_examples_2.setObjectName(u"tabWidget_examples_2")
        self.tabWidget_examples_2.setMinimumSize(QSize(0, 400))
        self.tabWidget_examples_2.setMaximumSize(QSize(16777215, 400))
        self.tabWidget_examples_2.setFont(font)
        self.tab_examples_csv_default_2 = QWidget()
        self.tab_examples_csv_default_2.setObjectName(u"tab_examples_csv_default_2")
        self.verticalLayout_19 = QVBoxLayout(self.tab_examples_csv_default_2)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.scrollArea_9 = QScrollArea(self.tab_examples_csv_default_2)
        self.scrollArea_9.setObjectName(u"scrollArea_9")
        self.scrollArea_9.setFont(font)
        self.scrollArea_9.setWidgetResizable(True)
        self.scrollAreaWidgetContents_10 = QWidget()
        self.scrollAreaWidgetContents_10.setObjectName(u"scrollAreaWidgetContents_10")
        self.scrollAreaWidgetContents_10.setGeometry(QRect(0, 0, 634, 420))
        self.verticalLayout_20 = QVBoxLayout(self.scrollAreaWidgetContents_10)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.label_13 = QLabel(self.scrollAreaWidgetContents_10)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.label_13.setWordWrap(True)
        self.label_13.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_20.addWidget(self.label_13, 0, Qt.AlignmentFlag.AlignTop)

        self.scrollArea_9.setWidget(self.scrollAreaWidgetContents_10)

        self.verticalLayout_19.addWidget(self.scrollArea_9)

        self.tabWidget_examples_2.addTab(self.tab_examples_csv_default_2, "")
        self.tab_examples_json_2 = QWidget()
        self.tab_examples_json_2.setObjectName(u"tab_examples_json_2")
        self.verticalLayout_21 = QVBoxLayout(self.tab_examples_json_2)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.scrollArea_10 = QScrollArea(self.tab_examples_json_2)
        self.scrollArea_10.setObjectName(u"scrollArea_10")
        self.scrollArea_10.setWidgetResizable(True)
        self.scrollAreaWidgetContents_11 = QWidget()
        self.scrollAreaWidgetContents_11.setObjectName(u"scrollAreaWidgetContents_11")
        self.scrollAreaWidgetContents_11.setGeometry(QRect(0, 0, 406, 1372))
        self.verticalLayout_22 = QVBoxLayout(self.scrollAreaWidgetContents_11)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.label_14 = QLabel(self.scrollAreaWidgetContents_11)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setFont(font)
        self.label_14.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.label_14.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_22.addWidget(self.label_14)

        self.scrollArea_10.setWidget(self.scrollAreaWidgetContents_11)

        self.verticalLayout_21.addWidget(self.scrollArea_10)

        self.tabWidget_examples_2.addTab(self.tab_examples_json_2, "")

        self.verticalLayout_18.addWidget(self.tabWidget_examples_2)

        self.label_15 = QLabel(self.scrollAreaWidgetContents_9)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.label_15.setWordWrap(True)
        self.label_15.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_18.addWidget(self.label_15)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_18.addItem(self.verticalSpacer_7)

        self.scrollArea_8.setWidget(self.scrollAreaWidgetContents_9)

        self.verticalLayout_17.addWidget(self.scrollArea_8)

        self.tabWidget.addTab(self.tab_quickstart_2, "")
        self.tab_pairs = QWidget()
        self.tab_pairs.setObjectName(u"tab_pairs")
        self.verticalLayout_2 = QVBoxLayout(self.tab_pairs)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.scrollArea = QScrollArea(self.tab_pairs)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 684, 4041))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(self.scrollAreaWidgetContents_2)
        self.label.setObjectName(u"label")
        self.label.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.label.setWordWrap(True)
        self.label.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_3.addWidget(self.label, 0, Qt.AlignmentFlag.AlignTop)

        self.label_2 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.label_2.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_3.addWidget(self.label_2)

        self.label_3 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.label_3.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_3.addWidget(self.label_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout_2.addWidget(self.scrollArea)

        self.tabWidget.addTab(self.tab_pairs, "")
        self.tab_main_menu_2 = QWidget()
        self.tab_main_menu_2.setObjectName(u"tab_main_menu_2")
        self.verticalLayout_23 = QVBoxLayout(self.tab_main_menu_2)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.scrollArea_11 = QScrollArea(self.tab_main_menu_2)
        self.scrollArea_11.setObjectName(u"scrollArea_11")
        self.scrollArea_11.setWidgetResizable(True)
        self.scrollAreaWidgetContents_12 = QWidget()
        self.scrollAreaWidgetContents_12.setObjectName(u"scrollAreaWidgetContents_12")
        self.scrollAreaWidgetContents_12.setGeometry(QRect(0, 0, 684, 1341))
        self.verticalLayout_24 = QVBoxLayout(self.scrollAreaWidgetContents_12)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.label_16 = QLabel(self.scrollAreaWidgetContents_12)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.label_16.setWordWrap(True)
        self.label_16.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_24.addWidget(self.label_16, 0, Qt.AlignmentFlag.AlignTop)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_24.addItem(self.verticalSpacer_8)

        self.scrollArea_11.setWidget(self.scrollAreaWidgetContents_12)

        self.verticalLayout_23.addWidget(self.scrollArea_11)

        self.tabWidget.addTab(self.tab_main_menu_2, "")
        self.tab_play_normal_2 = QWidget()
        self.tab_play_normal_2.setObjectName(u"tab_play_normal_2")
        self.verticalLayout_25 = QVBoxLayout(self.tab_play_normal_2)
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.scrollArea_12 = QScrollArea(self.tab_play_normal_2)
        self.scrollArea_12.setObjectName(u"scrollArea_12")
        self.scrollArea_12.setWidgetResizable(True)
        self.scrollAreaWidgetContents_13 = QWidget()
        self.scrollAreaWidgetContents_13.setObjectName(u"scrollAreaWidgetContents_13")
        self.scrollAreaWidgetContents_13.setGeometry(QRect(0, -537, 684, 1792))
        self.verticalLayout_26 = QVBoxLayout(self.scrollAreaWidgetContents_13)
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.label_17 = QLabel(self.scrollAreaWidgetContents_13)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.label_17.setWordWrap(True)
        self.label_17.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_26.addWidget(self.label_17, 0, Qt.AlignmentFlag.AlignTop)

        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_26.addItem(self.verticalSpacer_9)

        self.scrollArea_12.setWidget(self.scrollAreaWidgetContents_13)

        self.verticalLayout_25.addWidget(self.scrollArea_12)

        self.tabWidget.addTab(self.tab_play_normal_2, "")
        self.tab_settings_2 = QWidget()
        self.tab_settings_2.setObjectName(u"tab_settings_2")
        self.verticalLayout_27 = QVBoxLayout(self.tab_settings_2)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.scrollArea_15 = QScrollArea(self.tab_settings_2)
        self.scrollArea_15.setObjectName(u"scrollArea_15")
        self.scrollArea_15.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 684, 785))
        self.verticalLayout_32 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_32.setObjectName(u"verticalLayout_32")
        self.label_18 = QLabel(self.scrollAreaWidgetContents)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.label_18.setWordWrap(True)
        self.label_18.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_32.addWidget(self.label_18)

        self.verticalSpacer_10 = QSpacerItem(20, 33, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_32.addItem(self.verticalSpacer_10)

        self.scrollArea_15.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_27.addWidget(self.scrollArea_15)

        self.tabWidget.addTab(self.tab_settings_2, "")
        self.tab_inspector_2 = QWidget()
        self.tab_inspector_2.setObjectName(u"tab_inspector_2")
        self.verticalLayout_28 = QVBoxLayout(self.tab_inspector_2)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.scrollArea_13 = QScrollArea(self.tab_inspector_2)
        self.scrollArea_13.setObjectName(u"scrollArea_13")
        self.scrollArea_13.setWidgetResizable(True)
        self.scrollAreaWidgetContents_14 = QWidget()
        self.scrollAreaWidgetContents_14.setObjectName(u"scrollAreaWidgetContents_14")
        self.scrollAreaWidgetContents_14.setGeometry(QRect(0, 0, 684, 976))
        self.verticalLayout_29 = QVBoxLayout(self.scrollAreaWidgetContents_14)
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.label_19 = QLabel(self.scrollAreaWidgetContents_14)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.label_19.setWordWrap(True)
        self.label_19.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_29.addWidget(self.label_19)

        self.verticalSpacer_11 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_29.addItem(self.verticalSpacer_11)

        self.scrollArea_13.setWidget(self.scrollAreaWidgetContents_14)

        self.verticalLayout_28.addWidget(self.scrollArea_13)

        self.tabWidget.addTab(self.tab_inspector_2, "")
        self.tab_menubar_2 = QWidget()
        self.tab_menubar_2.setObjectName(u"tab_menubar_2")
        self.verticalLayout_30 = QVBoxLayout(self.tab_menubar_2)
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.scrollArea_14 = QScrollArea(self.tab_menubar_2)
        self.scrollArea_14.setObjectName(u"scrollArea_14")
        self.scrollArea_14.setWidgetResizable(True)
        self.scrollAreaWidgetContents_15 = QWidget()
        self.scrollAreaWidgetContents_15.setObjectName(u"scrollAreaWidgetContents_15")
        self.scrollAreaWidgetContents_15.setGeometry(QRect(0, 0, 684, 1980))
        self.verticalLayout_31 = QVBoxLayout(self.scrollAreaWidgetContents_15)
        self.verticalLayout_31.setObjectName(u"verticalLayout_31")
        self.label_20 = QLabel(self.scrollAreaWidgetContents_15)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.label_20.setWordWrap(True)
        self.label_20.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_31.addWidget(self.label_20)

        self.verticalSpacer_12 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_31.addItem(self.verticalSpacer_12)

        self.scrollArea_14.setWidget(self.scrollAreaWidgetContents_15)

        self.verticalLayout_30.addWidget(self.scrollArea_14)

        self.tabWidget.addTab(self.tab_menubar_2, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton = QPushButton(documentation)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(documentation)

        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_examples_2.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(documentation)
    # setupUi

    def retranslateUi(self, documentation):
        documentation.setWindowTitle(QCoreApplication.translate("documentation", u"Documentation", None))
        self.label_11.setText(QCoreApplication.translate("documentation", u"<html><head/><body><p><span style=\" font-size:24pt;\">The documentation (that nobody reads) for the game.</span></p><p><span style=\" font-size:24pt;\">Click the tab to chose the category.</span></p></body></html>", None))
        self.label_12.setText(QCoreApplication.translate("documentation", u"<html><head/><body><p><br/></p><p><span style=\" font-size:20pt;\">EVERYTHING IMPORTANT SHOULD HAVE TOOLTIPS AND STATUS TIPS!</span></p><p><span style=\" font-size:16pt;\">They should give you general understanding. If you're confused about a tooltip, please submit an issue to the GitHub page.</span></p><p><span style=\" font-size:20pt;\">Creating pair files</span></p><p>For the game to be useful you need pairs. You can create a pair file externally or by using the simple built-in inspector.</p><p><span style=\" font-size:20pt;\">Formats<br/></span>SPECIAL FORMATS ARE CONSIDERED LEGACY SINCE THEY DON'T SERVE A PURPOSE AFTER MULTIPLE PAIR FILES CAN BE LOADED.</p><p>There are 2 main formats, some special formats and a Nihongo Quest import. You can see all of them in File -&gt; Open (Advanced).</p><p>The two modes you should be aware of are Default CSV and Default JSON. You should write your pairs in Default CSV or in the inspector since those are the easiest to use. The inspector will create JSON files.</p><p>A "
                        "pair can have as many questions or answers as you want. The reason why it can have many questions is because you can flip questions and answers so that answers are questions and questions are answers.</p></body></html>", None))
        self.label_13.setText(QCoreApplication.translate("documentation", u"<html><head/><body><p>Question1<br/>Answer1<br/>Question2a,Question2b,Question2c<br/>Answer2a<br/>What is the capital of Japan?<br/>Tokyo<br/>What is the tallest mountain in the world?<br/>Mount Everest,Everest<br/>What is 5 + 3?<br/>8<br/>What is the currency of the United States?<br/>Dollar,US Dollar,USD</p></body></html>", None))
        self.tabWidget_examples_2.setTabText(self.tabWidget_examples_2.indexOf(self.tab_examples_csv_default_2), QCoreApplication.translate("documentation", u"Default CSV", None))
        self.label_14.setText(QCoreApplication.translate("documentation", u"{\n"
"    \"This title doesn't matter for now.\": [\n"
"        {\n"
"            \"question\": [\n"
"                \"What is 5 + 3?\"\n"
"            ],\n"
"            \"answer\": [\n"
"                \"8\"\n"
"            ]\n"
"        },\n"
"        {\n"
"            \"question\": [\n"
"                \"What is the tallest mountain in the world?\"\n"
"            ],\n"
"            \"answer\": [\n"
"                \"Mount Everest\",\n"
"                \"Everest\"\n"
"            ]\n"
"        },\n"
"        {\n"
"            \"question\": [\n"
"                \"What is the capital of Japan?\"\n"
"            ],\n"
"            \"answer\": [\n"
"                \"Tokyo\"\n"
"            ]\n"
"        },\n"
"        {\n"
"            \"question\": [\n"
"                \"What is the currency of the United States?\"\n"
"            ],\n"
"            \"answer\": [\n"
"                \"Dollar\",\n"
"                \"US Dollar\",\n"
"                \"USD\"\n"
"            ]\n"
"        }\n"
"    ]\n"
""
                        "}\n"
"", None))
        self.tabWidget_examples_2.setTabText(self.tabWidget_examples_2.indexOf(self.tab_examples_json_2), QCoreApplication.translate("documentation", u"Default JSON", None))
        self.label_15.setText(QCoreApplication.translate("documentation", u"<html><head/><body><p>As you can see, it follows a format where uneven lines are questions and even lines are answers.</p><p><span style=\" font-size:20pt;\">Importing pairs</span></p><p>This is really easy. Just go File -&gt; Open or Open (Advanced) and choose the file or files you have made. Advanced gives more control over what do you want to import, but normal open should work 99.9% of the time.</p><p>After you have imported the pairs you can see on the bottom of the main menu screen that &quot;Loaded [Amount of pairs] pairs from [Filename].&quot; or &quot;Loaded [Amount of pairs] pairs from multiple files. That means you have successfully imported the pairs.</p><p><br/></p><p><span style=\" font-size:20pt;\">Playing the game</span></p><p>You can choose from 3 modes, 3 question orders and whether to flip the questions and answers.</p><p><br/></p><p><span style=\" font-size:16pt;\">Modes:</span></p><p>Normal: This is a generic mode where a question is asked and you have to input the answer.</p><p>Multiple C"
                        "hoice: In this you can choose from answer candidates taken from the pairs.</p><p>Survive!: This is like Normal, but you can fail only a specified amount of times.<br/></p><p><span style=\" font-size:16pt;\">Question orders:</span></p><p>Forward: Go forward from question 1 to the last question. After that returns back to question one etc.</p><p>Reverse: Go backwards from last question to question 1. After that returns back to the last question etc.</p><p>Random: Goes through the questions in a random order with a simple never repeat way.</p><p><span style=\" font-size:16pt;\">Other:</span></p><p>Flip questions and answers: This flips questions and answers so that now questions are answers and answers are questions.</p><p><br/></p><p>After selecting the wanted modes you can press the &quot;Play&quot; button at the bottom of the screen. That throws you into the gameplay section.</p><p><br/></p><p><span style=\" font-size:20pt;\">Gameplay tricks</span></p><p>There are some neat things you can do in gameplay. Other"
                        " than answerring the question.</p><p>&quot;c&quot; or &quot;correct&quot;: Shows the correct answer. Breaks your streak.</p><p>&quot;seek NUMBER&quot;: Seeks to the specified number. Does not break your streak.</p><p>&quot;q&quot; or &quot;quit&quot;: Quits back to main menu. Breaks your streak (For now)</p><p>You can also just go back to the Main Menu tab by clicking it and start a new game.</p><p><br/></p><p>In Multiple Choice to quit the game you have to just click the Main Menu tab.</p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_quickstart_2), QCoreApplication.translate("documentation", u"Quick Start", None))
        self.label.setText(QCoreApplication.translate("documentation", u"<html><head/><body><p><span style=\" font-size:20pt;\">All about pairs</span></p><p>There's no use of the game without pairs.</p><p>Every format has the same end result; the pairs appear. There are still quite a lot of pair import methods for some reason. (Most of them will be considered legacy since they aren't needed anymore, I'll not be going through them here.)</p><p>The game supports only UTF 8 files. In most cases the files are UTF 8, but it will likely throw an error if the file is not UTF 8 encoded.</p><p><span style=\" font-size:16pt;\">Flags and Tooltips</span></p><p>You can make your own tooltips by putting it as a question or answer in the following format. (It will not become a question or an answer)</p><p>{tooltip=&quot;This is a tooltip.&quot;}<br/>{tooltip = 'This is also a tooltip.'}</p><p>These will show the text inside the quotes and remove the question or answer they are in. So your question answer pair could look something like this:</p><p>Question,{tooltip=&quot;This is a tooltip.&quot;}<"
                        "br/>Answer,{tooltip = 'Hint: There's an answer.'}<br/>Question2,This text will not appear {tooltip=&quot;This is a tooltip.&quot;}<br/>Answer2,This text will also not appear {tooltip=&quot;This is also a tooltip.&quot;}</p><p>In this example the text inside second cells is not visible because they are in the same cell as the tooltip.</p><p><span style=\" font-weight:600;\">RegEx flag</span>: You can set a RegEx flag to force RegEx matching on or off like following: {regex=True} or {regex=False} The matching is as lenient as in the tooltip. THE REGEX FLAG GOES ONLY TO THE ANSWER ROW!</p><p>The matching simply works like this (This is also explained in the menu bar regex support section):<br/>- `match = re.search(regex_answer, user_input)`<br/>Here we're checking if the user input is matching with the regex_answer.</p><p>Let's say we have an answer like this one:<br/>`answer \\(?the first one\\)?`<br/>This means that both of these are correct: `answer (the first one)` or `answer the first one`. If you're using t"
                        "his feature you should have knowledge over RegEx so you know those aren't the only 2 correct answers.</p><p>If there are multiple answers the they is put inside a non-capturing group to encapsulate them since the app also uses RegEx when user inputs all the answers. (Read Play -&gt; Normal -&gt; Multiple Answer Choices)</p><p>If &quot;Invalid RegEx! (re.PatternError)&quot; shows up it means the there's a problem with the RegEx.</p><p><span style=\" font-size:16pt;\">CSV</span></p><p>This will be the format you will be writing in. It's fairly straight forward and the easiest of them all.</p><p>-----<br/>Question1<br/>Answer1<br/>Question2a,Question2b,Question2c<br/>Answer2a<br/>What is the capital of Japan?<br/>Tokyo<br/>What is the tallest mountain in the world?<br/>Mount Everest,Everest<br/>What is 5 + 3?<br/>8<br/>What is the currency of the United States?<br/>Dollar,US Dollar,USD<br/>-----</p><p>On the 3rd line you can see 3 questions. This is because you can flip the questions and answers, but that questio"
                        "n will appear followingly: &quot;Question2a / Question2b / Question2c&quot; in the game.</p><p>To write in this format you can use something like LibreOffice Calc, Exel or Google Sheets. <span style=\" font-weight:600;\">When saving the file remember to choose CSV as the format.</span> After that you can just drag and drop the file onto the game window.</p><p><span style=\" font-size:16pt;\">JSON</span></p><p>The game saves its files in JSON. You don't need to know anything about it if you don't want.</p><p>Here's a simple example of a file in JSON format.</p><p>-----</p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("documentation", u"{\n"
"    \"This title doesn't matter for now.\": [\n"
"        {\n"
"            \"question\": [\n"
"                \"What is 5 + 3?\"\n"
"            ],\n"
"            \"answer\": [\n"
"                \"8\"\n"
"            ]\n"
"        },\n"
"        {\n"
"            \"question\": [\n"
"                \"What is the tallest mountain in the world?\"\n"
"            ],\n"
"            \"answer\": [\n"
"                \"Mount Everest\",\n"
"                \"Everest\"\n"
"            ]\n"
"        },\n"
"        {\n"
"            \"question\": [\n"
"                \"What is the capital of Japan?\"\n"
"            ],\n"
"            \"answer\": [\n"
"                \"Tokyo\"\n"
"            ]\n"
"        },\n"
"        {\n"
"            \"question\": [\n"
"                \"What is the currency of the United States?\"\n"
"            ],\n"
"            \"answer\": [\n"
"                \"Dollar\",\n"
"                \"US Dollar\",\n"
"                \"USD\"\n"
"            ]\n"
"        }\n"
"    ]\n"
""
                        "}\n"
"", None))
        self.label_3.setText(QCoreApplication.translate("documentation", u"<html><head/><body><p>-----<br/>There are some other fields, but most of them are considered legacy as of version 2.0.</p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_pairs), QCoreApplication.translate("documentation", u"Pairs", None))
        self.label_16.setText(QCoreApplication.translate("documentation", u"<html><head/><body><p><span style=\" font-size:20pt;\">Main Menu</span></p><p>Here you select the wanted game mode and go play it.</p><p>You can choose from 3 modes, 3 question orders and whether to flip the questions and answers.</p><p><br/></p><p><span style=\" font-size:16pt;\">Modes:</span></p><p>Normal: This is a generic mode where a question is asked and you have to input the answer.</p><p>Multiple Choice: In this you can choose from answer candidates taken from the pairs.</p><p>Survive!: This is like Normal, but you can fail only a specified amount of times.<br/></p><p><span style=\" font-size:16pt;\">Question orders:</span></p><p>Forward: Go forward from question 1 to the last question. After that returns back to question one etc.</p><p>Reverse: Go backwards from last question to question 1. After that returns back to the last question etc.</p><p>Random: Goes through the questions in a random order with a simple never repeat way.</p><p><span style=\" font-size:16pt;\">Other:</span></p><p>Flip questions"
                        " and answers: This flips questions and answers so that now questions are answers and answers are questions.</p><p><br/></p><p>After selecting the wanted modes you can press the &quot;Play&quot; button at the bottom of the screen. That throws you into the gameplay section.</p><p><br/></p><p><span style=\" font-size:20pt;\">The Quit Button</span></p><p>This button simply closes the game.</p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_main_menu_2), QCoreApplication.translate("documentation", u"Main Menu", None))
        self.label_17.setText(QCoreApplication.translate("documentation", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Noto Sans Arabic'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:20pt;\">Play (Normal)</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">Play tab has a couple of items to it.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -q"
                        "t-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">On the top left corner there's an info field. This displays current information such as if you answerred correctly or not.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">On the top right there's streak. If you hover over it you can see your all time streak. This is saved across sessions.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">On the middle you can see the question.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">Under that there's the input field.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; mar"
                        "gin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">On the bottom right corner there's a check button which can be pressed to check if what you wrote was correct. You can also press enter while typing.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">If you don't give an answer nothing will happen if the Check button is pressed.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:16pt;\">Multiple answer choices</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">If you have multiple answer choices you can put them all on the answer field. You just have to make sure that these"
                        " criteria is met:</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">1. the separator is one of these &quot; /|;,&quot; yes, they can also be separated by just a space</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">2. They must be in the same order as you've put them.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">If you're interested more deeply in the matching here's how it's done:<br /></span><span style=\" font-family:'Sans Serif'; font-style:italic;\">match = re.search(r&quot; ?[ /|;,]+ ?| ?or ?&quot;.join(correct_answers), user_input)</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px;"
                        " margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:16pt;\">Commands</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">Instead of typing the answer you can also type these commands to the input field and press check.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">&quot;c&quot; or &quot;correct&quot;: Shows the correct answer. Breaks your streak.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">&quot;seek NUMBER&quot;: Seeks to the specified number. Does not break your streak. (Replace NUMBER with an actual number)</span></p>\n"
"<p style=\" margin-top:12px; margin-"
                        "bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">&quot;seek +/-NUMBER&quot;: This is relative seek and for example if you are on question 10 the command &quot;seek +3&quot; moves you to question 13. And &quot;seek -5&quot; would move you to the question 5.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">&quot;q&quot; or &quot;quit&quot;: Quits back to main menu. Breaks your streak (For now)</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">You can also just go back to the Main Menu tab by clicking it. If you want to start a new game you just press play again.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-inden"
                        "t:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:16pt;\">Survive!</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">In this mode you can see your &quot;lives&quot; at the bottom left corner of the window.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\"><br /></span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:20pt;\">Play (Multiple Choice)</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">There's also a multiple choice mode.</span></p>\n"
"<p style=\" margin-top"
                        ":12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">In this you have a bit different layout. I'll still go through every item on the layout though.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">On the top left corner there's an info field. This displays current information such as if you answerred correctly or not.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">On the top right there's streak. If you hover over it you can see your all time streak. This is saved across sessions.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">"
                        "On the middle you can see the question.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">Under that there are the answer options. They are on the right side for less mouse movement from an answer to the check button.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">On the bottom right corner there's a check button which can be pressed to check if what you wrote was correct.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">On the bottom left corner there are two buttons:</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" f"
                        "ont-family:'Sans Serif';\">Correct: This shows the correct answer in the info field on top left corner.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">Seek: This shows a widget where you can choose question number you want to go. You cannot enter an incorrect value to it.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\"><br /></span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:20pt;\">Big mode (Font)</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">You can go to Misc -&gt; Big mode to"
                        " enable a bigger font for certain gameplay items.</span></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_play_normal_2), QCoreApplication.translate("documentation", u"Play", None))
        self.label_18.setText(QCoreApplication.translate("documentation", u"<html><head/><body><p><span style=\" font-size:20pt;\">Settings</span></p><p>This will cover every single setting in the settings tab.</p><p>All time streak: Shows your all time streak</p><p>All time survival streak: Shows you all time streak on Survive! mode.</p><p>Reset all time streak: Resets your all time streak. You have to first check the box and save.</p><p>Reset all time survival streak: Resets your all time survival streak. You have to first check the box and save.</p><p>Min question: The lowest question number to be asked <span style=\" font-weight:600;\">in random mode</span>.</p><p>Max question: The highest question number to be asked <span style=\" font-weight:600;\">in random mode</span>.</p><p>Show current question number: Whether to show the current question number before the question.</p><p>Multiple choice max options: How many candidates to show in multiple choice.</p><p>Lives: Choose the amount of lives you want to have in Survive! mode.</p><p>Fuzzy select percent: ONLY WORKS IF THEFUZZ IS I"
                        "NTALLED! How many percent of error can the answer have for it to be counted as &quot;almost correct&quot;. <br/>100% = The answer has to be 100% correct. No mistakes.<br/>80% = The answer has to be 90% correct for it to count as &quot;almost correct&quot;.</p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_settings_2), QCoreApplication.translate("documentation", u"Settings", None))
        self.label_19.setText(QCoreApplication.translate("documentation", u"<html><head/><body><p><span style=\" font-size:20pt;\">Inspector</span></p><p>The inspector is probably the most advanced feature of the game although it's still really simple.</p><p>You can create, remove and inspect pairs with it.</p><p>The format on it is a bit different than the Default CSV format. This format uses only the &quot;;&quot; character as a separator.</p><p><br/></p><p>-- Question --</p><p>What currency does the United States use?</p><p>-- Answer --</p><p>US Dollar;USD;United States Dollar</p><p><br/></p><p>Here there are 3 answer options separated by the &quot;;&quot; character.</p><p><br/><span style=\" font-size:20pt;\">Inspector Tools</span></p><p>There's an Inspector section on the top bar.</p><p>This section has all the tools you can use in the inspector. I suggest you to use the shortcuts that are provided for more convenience. If the shorcuts don't feel intuitive please make a GitHub issue and suggest better ones.</p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_inspector_2), QCoreApplication.translate("documentation", u"Inspector", None))
        self.label_20.setText(QCoreApplication.translate("documentation", u"<html><head/><body><p><span style=\" font-size:20pt;\">Menu Bar options</span></p><p>This section goes through every single option in the menu bar.</p><p>The menu bar is the bar on top of the window. It has the sections File, Inspector, Misc and Help.</p><p><span style=\" font-size:16pt;\">File</span></p><p>This section has 5 items.</p><p>Open: This opens a file selector that you can open a pair file with.</p><p>Open (Advanced): Clicking this opens a small widget where you can choose what kind of import methods you want to use. (Hover to see examples on the tooltip.)</p><p>New: This use clears current pairs from the game memory. <span style=\" font-weight:600;\">There is no check for unsaved files.</span></p><p>Save: This is the same as the &quot;Save to file&quot; button in the inspector. It opens a file dialog where you can save the current pair file as a JSON.</p><p>Quit: Quits the game.</p><p><span style=\" font-size:16pt;\">Inspector</span></p><p>This has all the tools for the inspector.</p><p>New Row: Cr"
                        "eates a new row at the end of the list.</p><p>New Row after selected: Creates a new row after the one you have a selected box in it.</p><p>Delete Last Row: Deletes the last row...</p><p>Delete Selected Row: Deletes the row you have a selected box in it.</p><p><span style=\" font-size:16pt;\">Misc</span></p><p>Big mode: Increases the size of certain gameplay elements.<br/>Show only the first question: Whether to show only the first question or all the questions in the question field. (Default: enabled)</p><p>RegEx support: Allows you to write answers in Python RegEx. This is an advanced feature for those who want to really take control over answer matching.</p><p>There's also a force RegEx on or off flag. It's explained in Pairs -&gt; Flags and Tooltips -&gt; RegEx flag</p><p>The matching simply works like this (this is also explained in the pairs' regex flag section):<br/>- `match = re.search(regex_answer, user_input)`<br/>Here we're checking if the user input is matching with the regex_answer.</p><p>Let's say"
                        " we have an answer like this one:<br/>`answer \\(?the first one\\)?`<br/>This means that both of these are correct: `answer (the first one)` or `answer the first one`. If you're using this feature you should have knowledge over RegEx so you know those aren't the only 2 correct answers.</p><p>If there are multiple answers the they is put inside a non-capturing group to encapsulate them since the app also uses RegEx when user inputs all the answers. (Read Play -&gt; Normal -&gt; Multiple Answer Choices)</p><p>If &quot;Invalid RegEx! (re.PatternError)&quot; shows up it means the there's a problem with the RegEx.</p><p>Test trigger: This is used for testing things. It should not do anything if you press it.</p><p><span style=\" font-size:16pt;\">Help</span></p><p>Help!: Shows this documentation.</p><p>Info: Shows information about the game.</p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_menubar_2), QCoreApplication.translate("documentation", u"Menu Bar", None))
        self.pushButton.setText(QCoreApplication.translate("documentation", u"Close", None))
    # retranslateUi

