# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'variables.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Variables(object):
    def setupUi(self, Variables):
        Variables.setObjectName("Variables")
        Variables.resize(400, 300)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget_variables = QtWidgets.QTableWidget(self.dockWidgetContents)
        self.tableWidget_variables.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.tableWidget_variables.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget_variables.setAlternatingRowColors(True)
        self.tableWidget_variables.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget_variables.setColumnCount(6)
        self.tableWidget_variables.setObjectName("tableWidget_variables")
        self.tableWidget_variables.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_variables.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_variables.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_variables.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_variables.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_variables.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_variables.setHorizontalHeaderItem(5, item)
        self.tableWidget_variables.horizontalHeader().setDefaultSectionSize(50)
        self.tableWidget_variables.horizontalHeader().setMinimumSectionSize(30)
        self.tableWidget_variables.verticalHeader().setDefaultSectionSize(15)
        self.tableWidget_variables.verticalHeader().setMinimumSectionSize(10)
        self.verticalLayout.addWidget(self.tableWidget_variables)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_refresh = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButton_refresh.setObjectName("pushButton_refresh")
        self.horizontalLayout.addWidget(self.pushButton_refresh)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        Variables.setWidget(self.dockWidgetContents)

        self.retranslateUi(Variables)
        QtCore.QMetaObject.connectSlotsByName(Variables)

    def retranslateUi(self, Variables):
        _translate = QtCore.QCoreApplication.translate
        Variables.setWindowTitle(_translate("Variables", "Variables"))
        item = self.tableWidget_variables.horizontalHeaderItem(0)
        item.setText(_translate("Variables", "Name"))
        item = self.tableWidget_variables.horizontalHeaderItem(1)
        item.setText(_translate("Variables", "Type"))
        item = self.tableWidget_variables.horizontalHeaderItem(2)
        item.setText(_translate("Variables", "Access"))
        item = self.tableWidget_variables.horizontalHeaderItem(3)
        item.setText(_translate("Variables", "Value"))
        item = self.tableWidget_variables.horizontalHeaderItem(4)
        item.setText(_translate("Variables", "Unit"))
        item = self.tableWidget_variables.horizontalHeaderItem(5)
        item.setText(_translate("Variables", "Probe"))
        self.pushButton_refresh.setText(_translate("Variables", "Refresh"))

