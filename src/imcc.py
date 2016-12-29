#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Qt Libraries
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow, QDockWidget, QTabWidget, QVBoxLayout, QGridLayout

# PyQtGraph
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import *
import pyqtgraph.console

# User-Interface for this module
from ui.imcc import Ui_imcc

# Other modules dependencies
from stm32flash import Stm32Flash
from console import Console
from configuration import Configuration
from parameters import Parameters
from cli import Cli
from graphics import Graphics


class IMCC(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_imcc()
        self.ui.setupUi(self)

        self.center_dock_layout = None

        self.parameters = Parameters()
        self.cli = Cli()

        self.create_widgets()

        self.connect()


    def create_widgets(self):

        # Adding the Configuration widget
        self.configuration_widget = QTabWidget()
        self.configuration = Configuration(self.configuration_widget)

        # Adding the STm32Flash widget
        self.stm32flash_dock = QDockWidget()
        self.stm32flash_dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.stm32flash = Stm32Flash(self.stm32flash_dock)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.stm32flash_dock)

        # Adding the Console dock with serial and python console widgets
        self.console_dock = QDockWidget()
        self.console_dock.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        self.console = Console(self.console_dock, self.cli)
        self.python_console = pg.console.ConsoleWidget()
        self.console.tabWidget.addTab(self.python_console, "Python Console")
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.console_dock)

        # Add the Parameters dock
        self.parameters_dock = QDockWidget()
        self.parameters_dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.parameters_dock.setWidget(self.parameters)
        self.parameters_dock.setWindowTitle("Parameters")
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.parameters_dock)

        # Create and place the main central widget
        self.graphics = Graphics()
        self.setCentralWidget(self.graphics.win)

    def connect(self):
        self.ui.actionConnect.triggered[bool].connect(self.action_connect)

        self.ui.action_openConfiguration.triggered.connect(self.configuration_widget.show)

        self.ui.action_viewConsole.triggered[bool].connect(self.console_dock.setVisible)
        self.console_dock.visibilityChanged[bool].connect(self.ui.action_viewConsole.setChecked)

        self.ui.action_viewBootload.triggered[bool].connect(self.stm32flash_dock.setVisible)
        self.stm32flash_dock.visibilityChanged[bool].connect(self.ui.action_viewBootload.setChecked)

        self.cli.data_available.connect(self.cli_process)

    # -------------------------------------------------------------------------
    # Bind & Slots connection
    # -------------------------------------------------------------------------
    @pyqtSlot(str)
    def set_status_bar_message(self, str):
        self.ui.statusbar.showMessage(str)

    @pyqtSlot(str)
    def append_console(self, str):
        self.console.append_text(str)

    @pyqtSlot(bool)
    def action_connect(self, checked):

        if checked:
            self.ui.actionConnect.setChecked(self.cli.open(self.configuration.port))
        else:
            self.cli.close()

    @pyqtSlot()
    def cli_process(self):

        try:
            item = self.cli.get_item()
            cmd_args = item.split("=")

            args_val = cmd_args[1].split(":")

            x = int(args_val[0])
            y = int(args_val[1])
            a = int(args_val[2])

            self.graphics_dock.append_value(x)

        except:
            pass
