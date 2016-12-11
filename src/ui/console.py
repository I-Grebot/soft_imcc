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
        console.resize(400, 300)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit_output = QtWidgets.QTextEdit(self.dockWidgetContents)
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
        self.label = QtWidgets.QLabel(self.dockWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit_input = QtWidgets.QLineEdit(self.dockWidgetContents)
        self.lineEdit_input.setObjectName("lineEdit_input")
        self.horizontalLayout.addWidget(self.lineEdit_input)
        self.pushButton_send = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButton_send.setObjectName("pushButton_send")
        self.horizontalLayout.addWidget(self.pushButton_send)
        self.pushButton_clear = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButton_clear.setObjectName("pushButton_clear")
        self.horizontalLayout.addWidget(self.pushButton_clear)
        self.verticalLayout.addLayout(self.horizontalLayout)
        console.setWidget(self.dockWidgetContents)

        self.retranslateUi(console)
        self.lineEdit_input.returnPressed.connect(self.pushButton_send.click)
        QtCore.QMetaObject.connectSlotsByName(console)

    def retranslateUi(self, console):
        _translate = QtCore.QCoreApplication.translate
        console.setWindowTitle(_translate("console", "Console"))
        self.label.setText(_translate("console", ">"))
        self.pushButton_send.setText(_translate("console", "Send"))
        self.pushButton_clear.setText(_translate("console", "Clear"))

