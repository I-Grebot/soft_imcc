# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'graphics.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Graphics(object):
    def setupUi(self, Graphics):
        Graphics.setObjectName("Graphics")
        Graphics.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(Graphics)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setObjectName("splitter")
        self.widget_graphics = QtWidgets.QWidget(self.splitter)
        self.widget_graphics.setObjectName("widget_graphics")
        self.widget_parameters = QtWidgets.QWidget(self.splitter)
        self.widget_parameters.setObjectName("widget_parameters")
        self.verticalLayout.addWidget(self.splitter)
        Graphics.setCentralWidget(self.centralwidget)
        self.toolBar = QtWidgets.QToolBar(Graphics)
        self.toolBar.setObjectName("toolBar")
        Graphics.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionTest = QtWidgets.QAction(Graphics)
        self.actionTest.setObjectName("actionTest")
        self.toolBar.addAction(self.actionTest)

        self.retranslateUi(Graphics)
        QtCore.QMetaObject.connectSlotsByName(Graphics)

    def retranslateUi(self, Graphics):
        _translate = QtCore.QCoreApplication.translate
        Graphics.setWindowTitle(_translate("Graphics", "graphics"))
        self.toolBar.setWindowTitle(_translate("Graphics", "toolBar"))
        self.actionTest.setText(_translate("Graphics", "test"))

