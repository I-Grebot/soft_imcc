# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'console.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_console(object):
    def setupUi(self, console):
        console.setObjectName("console")
        console.resize(836, 460)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.dockWidgetContents)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.South)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_serial = QtWidgets.QWidget()
        self.tab_serial.setObjectName("tab_serial")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab_serial)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit_output = QtWidgets.QTextEdit(self.tab_serial)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(9)
        self.textEdit_output.setFont(font)
        self.textEdit_output.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.textEdit_output.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit_output.setObjectName("textEdit_output")
        self.verticalLayout.addWidget(self.textEdit_output)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_input = QtWidgets.QLineEdit(self.tab_serial)
        self.lineEdit_input.setObjectName("lineEdit_input")
        self.horizontalLayout.addWidget(self.lineEdit_input)
        self.pushButton_send = QtWidgets.QPushButton(self.tab_serial)
        self.pushButton_send.setObjectName("pushButton_send")
        self.horizontalLayout.addWidget(self.pushButton_send)
        self.pushButton_clear = QtWidgets.QPushButton(self.tab_serial)
        self.pushButton_clear.setObjectName("pushButton_clear")
        self.horizontalLayout.addWidget(self.pushButton_clear)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tabWidget.addTab(self.tab_serial, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        console.setWidget(self.dockWidgetContents)

        self.retranslateUi(console)
        self.tabWidget.setCurrentIndex(0)
        self.lineEdit_input.returnPressed.connect(self.pushButton_send.click)
        QtCore.QMetaObject.connectSlotsByName(console)

    def retranslateUi(self, console):
        _translate = QtCore.QCoreApplication.translate
        console.setWindowTitle(_translate("console", "Console and Logs"))
        self.pushButton_send.setText(_translate("console", "Send"))
        self.pushButton_clear.setText(_translate("console", "Clear"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_serial), _translate("console", "Serial"))

