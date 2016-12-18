#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
import glob
import serial
from serial.tools import list_ports
from multiprocessing import Process

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QFileDialog

from ui.stm32flash import Ui_stm32flash

class Stm32Flash(Ui_stm32flash):

    # -------------------------------------------------------------------------
    # Constants
    # -------------------------------------------------------------------------

    BINARY_PATH = '..\\bin\\stm32flash.exe'

    MODES = ['8e1', '8n1']
    BAUDRATES = ['1200',
                 '1800',
                 '2400',
                 '4800',
                 '9600',
                 '19200',
                 '38400',
                 '57600',
                 '115200']

    DEFAULT_MODE = '8e1'
    DEFAULT_BAUDRATE = '115200'

    # -------------------------------------------------------------------------
    # Constructor
    # -------------------------------------------------------------------------
    def __init__(self, dockwidget):
        self.setupUi(dockwidget)

        # Define sub-process that'll be used for calling the stm32flash executable
        self.process = QProcess()
        self.process.setProcessChannelMode(QProcess.MergedChannels)

        # Fillup GUI
        self.fill_com_ports()
        self.fill_modes()
        self.fill_baudrates()

        # Connect slots
        self.connect()

    # -------------------------------------------------------------------------
    # Bind & Slots connection
    # -------------------------------------------------------------------------
    def connect(self):

        # Push-buttons
        self.pushButton_infos.clicked.connect(self.action_infos)
        self.pushButton_write.clicked.connect(self.action_write)
        self.pushButton_erase.clicked.connect(self.action_erase)
        self.pushButton_read.clicked.connect(self.action_read)
        self.pushButton_browse.clicked.connect(self.action_browse)
        self.pushButton_abort.clicked.connect(self.action_abort)

        # Output
        self.process.readyReadStandardOutput.connect(self.data_is_ready)

        # Prevent multiple runs
        self.process.started.connect(lambda: self.pushButton_infos.setEnabled(False))
        self.process.started.connect(lambda: self.pushButton_write.setEnabled(False))
        self.process.started.connect(lambda: self.pushButton_erase.setEnabled(False))
        self.process.started.connect(lambda: self.pushButton_read.setEnabled(False))
        self.process.finished.connect(lambda: self.pushButton_infos.setEnabled(True))
        self.process.finished.connect(lambda: self.pushButton_write.setEnabled(True))
        self.process.finished.connect(lambda: self.pushButton_erase.setEnabled(True))
        self.process.finished.connect(lambda: self.pushButton_read.setEnabled(True))

    # -------------------------------------------------------------------------
    # Internal handlers
    # -------------------------------------------------------------------------

    def get_mode(self):
        return self.comboBox_mode.currentText()

    def get_port(self):
        return self.comboBox_port.currentText()

    def get_baudrate(self):
        return self.comboBox_baudrate.currentText()

    def get_verify(self):
        return self.checkBox_verify.isChecked()

    def get_reset(self):
        return self.checkBox_reset.isChecked()

    def get_start(self):
        return self.checkBox_start.isChecked()

    def fill_com_ports(self):
        self.comboBox_port.clear()
        for port in serial.tools.list_ports.comports():
            self.comboBox_port.addItem(port.device)


    def fill_modes(self):
        self.comboBox_mode.clear()
        self.comboBox_mode.addItems(self.MODES)
        self.comboBox_mode.setCurrentIndex(self.comboBox_mode.findText(self.DEFAULT_MODE))

    def fill_baudrates(self):
        self.comboBox_baudrate.clear()
        self.comboBox_baudrate.addItems(self.BAUDRATES)
        self.comboBox_baudrate.setCurrentIndex(self.comboBox_baudrate.findText(self.DEFAULT_BAUDRATE))

    def set_basic_args(self):
        self.args = list()
        self.args.append('-b')
        self.args.append(self.get_baudrate())
        self.args.append('-m')
        self.args.append(self.get_mode())

    # -------------------------------------------------------------------------
    # Slots
    # -------------------------------------------------------------------------

    def data_is_ready(self):
        output_string = str(self.process.readAllStandardOutput(), encoding='utf-8')
        print(output_string, end='')

    # -------------------------------------------------------------------------
    # Actions triggered by push-buttons
    # -------------------------------------------------------------------------

    def action_browse(self):
        filename, _ = QFileDialog.getOpenFileName(caption='Open Hex file to write', filter='*.hex *.bin')
        self.lineEdit_filename.setText(filename)

    def action_abort(self):
        self.process.kill()

    def action_infos(self):
        self.set_basic_args()
        self.args.append(self.get_port())
        self.process.start(self.BINARY_PATH, self.args)

    def action_write(self):

        file = self.lineEdit_filename.text()
        if file:
            self.set_basic_args()
            self.args.append('-w')
            self.args.append(file)

            if self.get_verify():
                self.args.append('-v')
            if self.get_start():
                self.args.append('-g')
                self.args.append('0x0')
            elif self.get_reset():
                self.args.append('-R')

            self.args.append(self.get_port())
            self.process.start(self.BINARY_PATH, self.args)

        else:
            print('Error: ' + file + ' does not exist!')

    def action_erase(self):
        self.set_basic_args()
        self.args.append('-o')
        self.args.append(self.get_port())
        self.process.start(self.BINARY_PATH, self.args)

    def action_read(self):
        file, _ = QFileDialog.getSaveFileName(caption='Save Hex file', filter='*.bin')
        self.set_basic_args()
        self.args.append('-r')
        self.args.append(file)
        self.args.append(self.get_port())
        self.process.start(self.BINARY_PATH, self.args)
