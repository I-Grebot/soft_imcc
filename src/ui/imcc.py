# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'imcc.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import *

class Ui_imcc(object):
    def setupUi(self, imcc):
        imcc.setObjectName("imcc")
        imcc.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(imcc)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.graphicsView = DockArea(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)
        imcc.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(imcc)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuSession = QtWidgets.QMenu(self.menubar)
        self.menuSession.setObjectName("menuSession")
        self.menuConfig = QtWidgets.QMenu(self.menubar)
        self.menuConfig.setObjectName("menuConfig")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        imcc.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(imcc)
        self.statusbar.setObjectName("statusbar")
        imcc.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(imcc)
        self.toolBar.setMovable(False)
        self.toolBar.setObjectName("toolBar")
        imcc.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionConnect = QtWidgets.QAction(imcc)
        self.actionConnect.setCheckable(True)
        self.actionConnect.setObjectName("actionConnect")
        self.action_configLoad = QtWidgets.QAction(imcc)
        self.action_configLoad.setObjectName("action_configLoad")
        self.action_configSave = QtWidgets.QAction(imcc)
        self.action_configSave.setObjectName("action_configSave")
        self.action_openConfiguration = QtWidgets.QAction(imcc)
        self.action_openConfiguration.setObjectName("action_openConfiguration")
        self.action_viewConsole = QtWidgets.QAction(imcc)
        self.action_viewConsole.setCheckable(True)
        self.action_viewConsole.setChecked(True)
        self.action_viewConsole.setObjectName("action_viewConsole")
        self.action_viewBootload = QtWidgets.QAction(imcc)
        self.action_viewBootload.setCheckable(True)
        self.action_viewBootload.setChecked(True)
        self.action_viewBootload.setObjectName("action_viewBootload")
        self.menuConfig.addAction(self.action_configLoad)
        self.menuConfig.addAction(self.action_configSave)
        self.menuSettings.addAction(self.action_openConfiguration)
        self.menuView.addAction(self.action_viewConsole)
        self.menuView.addAction(self.action_viewBootload)
        self.menubar.addAction(self.menuConfig.menuAction())
        self.menubar.addAction(self.menuSession.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.toolBar.addAction(self.actionConnect)

        self.retranslateUi(imcc)
        QtCore.QMetaObject.connectSlotsByName(imcc)

    def retranslateUi(self, imcc):
        _translate = QtCore.QCoreApplication.translate
        imcc.setWindowTitle(_translate("imcc", "MainWindow"))
        self.menuSession.setTitle(_translate("imcc", "Session"))
        self.menuConfig.setTitle(_translate("imcc", "Config"))
        self.menuSettings.setTitle(_translate("imcc", "Settings"))
        self.menuView.setTitle(_translate("imcc", "View"))
        self.toolBar.setWindowTitle(_translate("imcc", "toolBar"))
        self.actionConnect.setText(_translate("imcc", "Connect"))
        self.actionConnect.setToolTip(_translate("imcc", "Connect"))
        self.action_configLoad.setText(_translate("imcc", "Load"))
        self.action_configSave.setText(_translate("imcc", "Save"))
        self.action_openConfiguration.setText(_translate("imcc", "Configuration"))
        self.action_viewConsole.setText(_translate("imcc", "Console"))
        self.action_viewBootload.setText(_translate("imcc", "STm32 Bootload"))
