#!/usr/bin/python3
# -*- coding: utf-8 -*-


import subprocess
from queue import Queue
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from ui.stm32flash import Ui_stm32flash

class Stm32Flash(Ui_stm32flash):

    # -------------------------------------------------------------------------
    # Constructor
    # -------------------------------------------------------------------------
    def __init__(self, dockwidget):
        self.setupUi(dockwidget)
        self.process = QProcess()
        self.connect()

    # -------------------------------------------------------------------------
    # Bind & Slots connection
    # -------------------------------------------------------------------------
    def connect(self):
        self.pushButton_write.clicked.connect(self.action_write)
        self.pushButton_erase.clicked.connect(self.action_erase)
        self.pushButton_read.clicked.connect(self.action_read)

        self.process.readyRead.connect(self.data_is_ready)

        # Prevent multiple runs
        self.process.started.connect(lambda: self.pushButton_write.setEnabled(False))
        self.process.started.connect(lambda: self.pushButton_erase.setEnabled(False))
        self.process.started.connect(lambda: self.pushButton_read.setEnabled(False))
        self.process.finished.connect(lambda: self.pushButton_write.setEnabled(True))
        self.process.finished.connect(lambda: self.pushButton_erase.setEnabled(True))
        self.process.finished.connect(lambda: self.pushButton_read.setEnabled(True))

    # -------------------------------------------------------------------------
    # Slots
    # -------------------------------------------------------------------------

    def data_is_ready(self):
        output_string = str(self.process.readAll(), encoding='utf-8')
        print(output_string, end='')

    def action_write(self):
        self.process.start('ping', ['127.0.0.1'])

    def action_erase(self):
        self.process.start('..\\bin\\stm32flash.exe', ['-h'])

    def action_read(self):
        print('Read!')
