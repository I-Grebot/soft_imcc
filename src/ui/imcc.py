# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'imcc.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_imcc(object):
    def setupUi(self, imcc):
        imcc.setObjectName("imcc")
        imcc.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(imcc)
        self.centralwidget.setObjectName("centralwidget")
        imcc.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(imcc)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuSession = QtWidgets.QMenu(self.menubar)
        self.menuSession.setObjectName("menuSession")
        imcc.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(imcc)
        self.statusbar.setObjectName("statusbar")
        imcc.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuSession.menuAction())

        self.retranslateUi(imcc)
        QtCore.QMetaObject.connectSlotsByName(imcc)

    def retranslateUi(self, imcc):
        _translate = QtCore.QCoreApplication.translate
        imcc.setWindowTitle(_translate("imcc", "MainWindow"))
        self.menuSession.setTitle(_translate("imcc", "Session"))

