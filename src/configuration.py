#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import glob
import serial
from serial.tools import list_ports
from queue import Queue
from PyQt5.QtCore import *
from PyQt5.QtGui import *


from ui.configuration import Ui_configuration

class Configuration(Ui_configuration):

    # -------------------------------------------------------------------------
    # Constants
    # -------------------------------------------------------------------------

    BINARY_PATH = '..\\bin\\stm32flash.exe'

    # -------------------------------------------------------------------------
    # Constructor
    # -------------------------------------------------------------------------
    def __init__(self, tabwidget):
        self.setupUi(tabwidget)
        self.connect()
        self.port = ''
        self.refresh_serial_ports()

    # -------------------------------------------------------------------------
    # Bind & Slots connection
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # Internal Handlers
    # -------------------------------------------------------------------------

    def connect(self):
        self.pushButton_refreshPorts.clicked.connect(self.refresh_serial_ports)
        self.comboBox_port.currentTextChanged.connect(self.refresh_port_infos)

    # -------------------------------------------------------------------------
    # Actions
    # -------------------------------------------------------------------------

    def refresh_serial_ports(self):

        self.comboBox_port.clear()
        for port in serial.tools.list_ports.comports():
            self.comboBox_port.addItem(port.device)

    def refresh_port_infos(self):
        self.port = self.comboBox_port.currentText()

        for port in serial.tools.list_ports.comports():
            if self.port == port.device:
                self.label_descriptionValue.setText(port.description)
