# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configuration.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_configuration(object):
    def setupUi(self, configuration):
        configuration.setObjectName("configuration")
        configuration.resize(350, 300)
        self.tab_serial = QtWidgets.QWidget()
        self.tab_serial.setObjectName("tab_serial")
        self.formLayout = QtWidgets.QFormLayout(self.tab_serial)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.groupBox = QtWidgets.QGroupBox(self.tab_serial)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setHorizontalSpacing(20)
        self.formLayout_2.setObjectName("formLayout_2")
        self.labelSerialPortText = QtWidgets.QLabel(self.groupBox)
        self.labelSerialPortText.setObjectName("labelSerialPortText")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelSerialPortText)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBox_port = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_port.setObjectName("comboBox_port")
        self.horizontalLayout.addWidget(self.comboBox_port)
        self.pushButton_refreshPorts = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_refreshPorts.sizePolicy().hasHeightForWidth())
        self.pushButton_refreshPorts.setSizePolicy(sizePolicy)
        self.pushButton_refreshPorts.setMinimumSize(QtCore.QSize(40, 0))
        self.pushButton_refreshPorts.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButton_refreshPorts.setObjectName("pushButton_refreshPorts")
        self.horizontalLayout.addWidget(self.pushButton_refreshPorts)
        self.formLayout_2.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.labelDescriptionText = QtWidgets.QLabel(self.groupBox)
        self.labelDescriptionText.setObjectName("labelDescriptionText")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelDescriptionText)
        self.label_descriptionValue = QtWidgets.QLabel(self.groupBox)
        self.label_descriptionValue.setObjectName("label_descriptionValue")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label_descriptionValue)
        self.horizontalLayout_2.addLayout(self.formLayout_2)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.groupBox)
        configuration.addTab(self.tab_serial, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        configuration.addTab(self.tab, "")

        self.retranslateUi(configuration)
        configuration.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(configuration)

    def retranslateUi(self, configuration):
        _translate = QtCore.QCoreApplication.translate
        configuration.setWindowTitle(_translate("configuration", "Configuration"))
        self.groupBox.setTitle(_translate("configuration", "Connection Settings"))
        self.labelSerialPortText.setText(_translate("configuration", "Serial Port :"))
        self.pushButton_refreshPorts.setText(_translate("configuration", "R"))
        self.labelDescriptionText.setText(_translate("configuration", "Description :"))
        self.label_descriptionValue.setText(_translate("configuration", "-"))
        configuration.setTabText(configuration.indexOf(self.tab_serial), _translate("configuration", "Serial"))
        configuration.setTabText(configuration.indexOf(self.tab), _translate("configuration", "Graphs"))

