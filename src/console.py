#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from queue import Queue
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from ui.console import Ui_console
from cli import Cli

# Stream object that simply put incoming data in a queue
class ConsoleStream(object):
    def __init__(self, queue):
        self.queue = queue

    def write(self, text):
        self.queue.put(text)

    def flush(self):
        pass

# A QObject (to be run in a QThread) which sits waiting for data to come through a Queue.Queue().
# It blocks until data is available, and one it has got something from the queue, it sends
# it to the "MainThread" by emitting a Qt Signal
class ConsoleReceiver(QObject):
    mysignal = pyqtSignal(str)

    def __init__(self, queue, *args, **kwargs):
        QObject.__init__(self, *args, **kwargs)
        self.queue = queue

    @pyqtSlot()
    def run(self):
        while True:
            text = self.queue.get()
            self.mysignal.emit(text)

class Console(Ui_console):

    # -------------------------------------------------------------------------
    # Constructor
    # -------------------------------------------------------------------------
    def __init__(self, dockwidget, cli):
        self.cli = cli
        self.setupUi(dockwidget)
        self.connect()

    # -------------------------------------------------------------------------
    # Bind & Slots connection
    # -------------------------------------------------------------------------
    def connect(self):
        self.pushButton_send.clicked.connect(self.send)
        self.pushButton_clear.clicked.connect(self.clear)

    # -------------------------------------------------------------------------
    # Slots
    # -------------------------------------------------------------------------

    @pyqtSlot(str)
    def append_text(self, text):
        self.textEdit_output.moveCursor(QTextCursor.End)
        self.textEdit_output.insertPlainText(text)

    def clear(self):
        self.textEdit_output.clear()

    def send(self):
        cmd_str = self.lineEdit_input.text()
        if len(cmd_str) > 0:

            # Add line terminator
            cmd_str += '\n'

            # Append testEdit display and flush lineEdit
            self.append_text('> ')
            self.append_text(cmd_str)
            self.lineEdit_input.clear()

            # Send command
            self.cli.send(cmd_str)

