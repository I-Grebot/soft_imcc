#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import time
import re

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
from variables import Variables
from cli import Cli
from graphics.graphics import Graphics

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

        # Default states
        self.ui.action_viewBootload.trigger() # Hidden

        # Variables for probe
        self.probe_list = list()
        self.probe_started = False
        self.timer = QTimer()

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

        # Add the Variables dock
        self.variables_dock = QDockWidget()
        self.variables_dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.variables = Variables(self.variables_dock, self.cli)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.variables_dock)

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

        self.graphics.actionReset.triggered[bool].connect(self.reset)
        self.graphics.actionProbe.triggered[bool].connect(self.probe_start_stop)

        self.variables.probe_list_changed.connect(self.probe_list_update)


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

        ret_str = self.cli.get_item()

        if self.probe_started:
            try:
                if ret_str.startswith('[GET]'):

                    # Clean the string
                    ret_str = ret_str[5:]
                    ret_str = re.sub('\s+', ' ', ret_str)
                    ret_str = re.sub('\A\s', '', ret_str)
                    ret_str = re.sub('\s\Z', '', ret_str)
                    ret_str = re.sub('[^a-zA-Z0-9=_\-. ]+', '', ret_str)

                    cmd_args = ret_str.split("=")

                    if len(cmd_args) == 2:
                        self.graphics.set_probe_value(cmd_args[0], int(cmd_args[1]))

                        # TODO: move robot(x,y,a) into dedicated holder
                        # args_val = cmd_args[1].split(":")
                        #
                        # x = int(args_val[0])
                        # y = int(args_val[1])
                        # a = int(args_val[2])
                        #
                        # # self.graphics_dock.append_value(x)
                        # self.graphics.set_probe_value("robot.cs.pos.x", x)
                        # self.graphics.set_probe_value("robot.cs.pos.y", y)
                        # self.graphics.set_probe_value("robot.cs.pos.a", a)
                        #
                        # self.graphics.table.add_robot_pos(x, y, a)

                if ret_str.startswith('[PRB]'):

                    # Clean the string
                    ret_str = ret_str[5:]
                    ret_str = re.sub('\s+', ' ', ret_str)
                    ret_str = re.sub('\A\s', '', ret_str)
                    ret_str = re.sub('\s\Z', '', ret_str)
                    ret_str = re.sub('[^0-9\-. ]+', '', ret_str)

                    values = ret_str.split(" ")

                    if len(values) == len(self.probe_list):
                        for i in range(len(values)):
                            self.graphics.set_probe_value(self.probe_list[i]['name'], int(values[i]))

            except:
                pass

        else:
            self.console.append_text(ret_str)

            # Decode returned strings
            if ret_str.startswith('[VAR]'):

                # Clean the string
                ret_str = ret_str[5:]
                ret_str = re.sub('\s+', ' ',     ret_str)
                ret_str = re.sub('\A\s', '', ret_str)
                ret_str = re.sub('\s\Z', '', ret_str)
                ret_str = re.sub('[^a-zA-Z0-9_. ]+', '', ret_str)

                # Split items, add it to the variable list if it matches the format
                var_items = ret_str.split(' ')
                if len(var_items) == 6:
                    var = {'id': var_items[0],
                           'name': var_items[3],
                           'type': var_items[1],
                           'access': var_items[2],
                           'value': var_items[5],
                           'unit': var_items[4]}
                    self.variables.add_item(var)

    def reset(self):
        self.cli.flush()
        self.cli.send('sys reset\n')

    def probe_list_update(self):
        self.probe_list = self.variables.get_probe_list()
        self.graphics.set_probe_list(self.probe_list)

        print(self.probe_list)

    def probe_start_stop(self, state):

        if state:
            print('Starting probe...')
            self.cli.flush()
            self.timer.timeout.connect(self.probe_send_test)
            self.timer.start(100)
            self.probe_started = True
        else:
            print('Stopping probe...')
            self.probe_started = False
            self.timer.stop()

    def probe_send_test(self):
        probe_str = 'prb '
        for i in range(len(self.probe_list)):
            probe_str += '%s ' % self.probe_list[i]['id']

        probe_str += '\n'
        self.cli.send(probe_str)

        # Old-school with 'get'
        # for i in range(len(self.probe_list)):
        #     self.cli.send('get %s\n' % self.probe_list[i])

