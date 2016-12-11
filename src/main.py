#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from queue import Queue
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread
from imcc import IMCC
from console import ConsoleStream, ConsoleReceiver

if __name__ == '__main__':

    # Create application and initialize all windows
    app = QApplication(sys.argv)
    imcc = IMCC()

    # Redirect stdout to a dedicated queue (in a ConsoleStream object)
    stdoutQueue = Queue()
    sys.stdout = ConsoleStream(stdoutQueue)

    # Create thread that will listen on the other end of the queue, and send the text to the textedit in our application
    consoleReceiverThread = QThread()
    consoleReceiver = ConsoleReceiver(stdoutQueue)
    consoleReceiver.mysignal.connect(imcc.append_console)
    consoleReceiver.moveToThread(consoleReceiverThread)
    consoleReceiverThread.started.connect(consoleReceiver.run)
    consoleReceiverThread.start()

    # Welcome message
    imcc.append_console('------------------------------\n')
    imcc.append_console('IgreBot Mission Control Center\n')
    imcc.append_console('------------------------------\n')
    imcc.set_status_bar_message('Initialized')

    # Show everything and run the app!
    imcc.show()
    sys.exit(app.exec_())
