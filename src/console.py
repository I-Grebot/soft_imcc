#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from queue import Queue
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from ui.console import Ui_console

# Stream object that simply put incoming data in a queue
class ConsoleStream(object):
    def __init__(self, queue):
        self.queue = queue

    def write(self, text):
        self.queue.put(text)

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

# An example QObject (to be run in a QThread) which outputs information with print
class LongRunningThing(QObject):
    @pyqtSlot()
    def run(self):
        for i in range(1000):
            print(i)

class Console(Ui_console):

    # -------------------------------------------------------------------------
    # Constructor
    # -------------------------------------------------------------------------
    def __init__(self, dockwidget):
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
        if len(self.lineEdit_input.text()) > 0:
            self.append_text('> ')
            self.append_text(self.lineEdit_input.text())
            self.append_text('\n')
            self.lineEdit_input.clear()

        #self.thread = QThread()
        #self.long_running_thing = LongRunningThing()
        #self.long_running_thing.moveToThread(self.thread)
        #self.thread.started.connect(self.long_running_thing.run)
        #self.thread.start()
