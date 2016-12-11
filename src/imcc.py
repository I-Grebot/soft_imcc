#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Qt Libraries
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QDockWidget
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# User-Interface for this module
from ui.imcc import Ui_imcc

# Other modules dependencies
from stm32flash import Stm32Flash
from console import Console

class IMCC(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_imcc()
        self.ui.setupUi(self)

        self.create_dock_widgets()

    def create_dock_widgets(self):

        # Adding the STm32Flash widget
        dock = QDockWidget()
        dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.stm32flash = Stm32Flash(dock)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)

        # Adding the Console widget
        dock = QDockWidget()
        dock.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        self.console = Console(dock)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, dock)


    @pyqtSlot(str)
    def set_status_bar_message(self, str):
        self.ui.statusbar.showMessage(str)

    @pyqtSlot(str)
    def append_console(self, str):
        self.console.append_text(str)

