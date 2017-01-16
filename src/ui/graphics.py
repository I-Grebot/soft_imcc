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
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.widget_graphics = QtWidgets.QWidget(self.splitter)
        self.widget_graphics.setObjectName("widget_graphics")
        self.widget_parameters = QtWidgets.QWidget(self.splitter)
        self.widget_parameters.setObjectName("widget_parameters")
        self.verticalLayout.addWidget(self.splitter)
        Graphics.setCentralWidget(self.centralwidget)
        self.toolBar_actions = QtWidgets.QToolBar(Graphics)
        self.toolBar_actions.setMovable(False)
        self.toolBar_actions.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolBar_actions.setFloatable(False)
        self.toolBar_actions.setObjectName("toolBar_actions")
        Graphics.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_actions)
        self.actionCursor = QtWidgets.QAction(Graphics)
        self.actionCursor.setCheckable(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/silk/cursor.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCursor.setIcon(icon)
        self.actionCursor.setObjectName("actionCursor")
        self.actionGoto = QtWidgets.QAction(Graphics)
        self.actionGoto.setCheckable(True)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/silk/car.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGoto.setIcon(icon1)
        self.actionGoto.setObjectName("actionGoto")
        self.toolBar_actions.addAction(self.actionCursor)
        self.toolBar_actions.addAction(self.actionGoto)

        self.retranslateUi(Graphics)
        QtCore.QMetaObject.connectSlotsByName(Graphics)

    def retranslateUi(self, Graphics):
        _translate = QtCore.QCoreApplication.translate
        Graphics.setWindowTitle(_translate("Graphics", "graphics"))
        self.toolBar_actions.setWindowTitle(_translate("Graphics", "Graphics toolbar"))
        self.actionCursor.setText(_translate("Graphics", "Cursor"))
        self.actionGoto.setText(_translate("Graphics", "Goto"))
