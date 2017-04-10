#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Standard python libraries
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

# User-Interface
from ui.imcc import Ui_imcc
from ui import imcc_rc

# Other modules dependencies
from stm32flash import Stm32Flash
from console import Console
from parameters import Parameters
from variables import Variables
from cli import Cli
from robot import Robot
from graphics.graphics import Graphics

class IMCC(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_imcc()
        self.ui.setupUi(self)

        self.center_dock_layout = None

        self.parameters = Parameters(showHeader=False)
        self.cli = Cli()
        self.connect_first_time = False

        self.robot = Robot()

        self.create_widgets()

        self.connect()

        # Default states
        self.ui.actionViewBootload.trigger()

        # Variables for probe
        self.probe_list = list()
        self.probe_started = False
        self.timer = QTimer()

    # -------------------------------------------------------------------------
    # UI
    # -------------------------------------------------------------------------

    def create_widgets(self):

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

        # Some default loads
        self.update_playground_size()
        self.update_robot()

        self.graphics.table.add_robot_pos({'x': 0, 'y': 0, 'a': 0})
        self.graphics.table.update_target_pos(1500, 1000)

    def connect(self):

        # Connect ToolBar items
        self.ui.actionConnect.triggered[bool].connect(self.connect_com)
        self.ui.actionReset.triggered[bool].connect(self.reset)
        self.ui.actionProbe.triggered[bool].connect(self.probe_start_stop)

        self.ui.actionViewConsole.triggered[bool].connect(self.console_dock.setVisible)
        self.console_dock.visibilityChanged[bool].connect(self.ui.actionViewConsole.setChecked)

        self.ui.actionViewBootload.triggered[bool].connect(self.stm32flash_dock.setVisible)
        self.stm32flash_dock.visibilityChanged[bool].connect(self.ui.actionViewBootload.setChecked)

        self.ui.actionViewParameters.triggered[bool].connect(self.parameters_dock.setVisible)
        self.parameters_dock.visibilityChanged[bool].connect(self.ui.actionViewParameters.setChecked)

        self.ui.actionViewVariables.triggered[bool].connect(self.variables_dock.setVisible)
        self.variables_dock.visibilityChanged[bool].connect(self.ui.actionViewVariables.setChecked)

        self.ui.actionPan.triggered[bool].connect(self.pan_mode)
        self.ui.actionZoom.triggered[bool].connect(self.zoom_mode)
        self.ui.actionGoto.triggered[bool].connect(self.goto_mode)
        self.ui.actionStop.triggered.connect(self.stop)
        self.ui.actionViewSettings.triggered[bool].connect(self.graphics.widget_parameters.setVisible)
        self.ui.actionViewGraphs.triggered[bool].connect(self.graphics.action_view_graphs)

        self.parameters.robot_setting_changed.connect(self.update_robot)
        self.parameters.playground_size_changed.connect(self.update_playground_size)
        self.parameters.bootloader_path_changed.connect(self.update_bootload_path)

        self.cli.data_available.connect(self.cli_process)

        self.variables.probe_list_changed.connect(self.probe_list_update)
        self.variables.variable_changed[str, str].connect(self.variable_updated)

        self.graphics.goto_clicked[int, int].connect(self.goto)

    def set_status_bar_message(self, str):
        self.ui.statusbar.showMessage(str)

    def append_console(self, str):
        self.console.append_text(str)

    def update_playground_size(self):
        width = self.parameters.get_playground_width()
        height = self.parameters.get_playground_height()
        self.graphics.update_table_playground()
        self.graphics.table.set_playground_size(width, height)
        self.graphics.table.update_table_outline()

    def update_robot(self):
        robot_radius = self.parameters.get_robot_radius()
        self.graphics.table.set_robot_radius(robot_radius)

    def update_bootload_path(self):
        self.stm32flash.set_binary_path(self.parameters.get_bootloader_path())

    # -------------------------------------------------------------------------
    # Static methods
    # -------------------------------------------------------------------------

    @staticmethod
    def cleanup_spaces(in_str):
        ret_str = re.sub('\s+', ' ', in_str)
        ret_str = re.sub('\A\s', '', ret_str)
        ret_str = re.sub('\s\Z', '', ret_str)
        return ret_str

    # -------------------------------------------------------------------------
    # Main Actions management
    # -------------------------------------------------------------------------

    def reset(self):
        self.cli.flush()
        self.cli.send('sys reset\n')

    def pan_mode(self, val):
        if val:

            if self.ui.actionZoom.isChecked():
                self.ui.actionZoom.setChecked(False)

            if self.ui.actionGoto.isChecked():
                self.ui.actionGoto.setChecked(False)

            self.graphics.table.viewbox.setMouseMode(pg.ViewBox.PanMode)
            self.graphics.goto_mode = False

        self.graphics.pan_mode = val

    def zoom_mode(self, val):
        if val:

            if self.ui.actionPan.isChecked():
                self.ui.actionPan.setChecked(False)

            if self.ui.actionGoto.isChecked():
                self.ui.actionGoto.setChecked(False)

            self.graphics.table.viewbox.setMouseMode(pg.ViewBox.RectMode)

    def goto_mode(self, val):
        if val:
            if self.ui.actionPan.isChecked():
                self.ui.actionPan.setChecked(False)

            if self.ui.actionZoom.isChecked():
                self.ui.actionZoom.setChecked(False)

            self.graphics.pan_mode = False

        self.graphics.goto_mode = val

    def goto(self, x, y):
        print('Goto %d %d' %(x, y))
        self.cli.send('mot goto %d %d\n' % (x, y))

    def stop(self):
        print('Stopping motion')
        self.cli.send('mot stop\n')

    def probe_list_update(self):
        self.probe_list = self.variables.get_probe_list()
        self.graphics.set_probe_list(self.probe_list)

    def probe_start_stop(self, state):

        if state:
            print('Starting probe...')
            self.cli.flush()
            self.timer.timeout.connect(self.probe_send)
            self.timer.start(1000 / self.parameters.get_probing_frequency())
            self.probe_started = True
        else:
            print('Stopping probe...')
            self.probe_started = False
            self.timer.stop()

    def probe_send(self):
        probe_str = 'prb '
        for i in range(len(self.probe_list)):
            probe_str += '%s ' % self.probe_list[i]['id']

        probe_str += '\n'
        self.cli.send(probe_str)

    @pyqtSlot(bool)
    def connect_com(self, checked):

        if checked:
            open_success = self.cli.open(self.parameters.get_serial_port())
            self.ui.actionConnect.setChecked(open_success)

            if open_success:

                # Auto-refresh only the first time
                if self.connect_first_time is False:
                    self.variables.refresh_table()

                self.variables.set_table_enabled(True)
                self.connect_first_time = True
                self.set_status_bar_message("Opened")

            else:
                self.set_status_bar_message("Error")

        else:
            self.cli.close()
            self.variables.set_table_enabled(False)
            self.set_status_bar_message("Closed")

    @pyqtSlot(str, str)
    def variable_updated(self, name, value):
        set_str = 'set ' + name + ' ' + value + '\n'
        self.cli.send(set_str)

    @pyqtSlot()
    def cli_process(self):

        ret_str = self.cli.get_item()

        try:
            if ret_str.startswith('[GET]'):

                # Clean the string
                ret_str = ret_str[5:]
                ret_str = self.cleanup_spaces(ret_str)
                ret_str = re.sub('[^a-zA-Z0-9=_\-. ]+', '', ret_str)

                cmd_args = ret_str.split("=")

                if len(cmd_args) == 2:
                    var = cmd_args[0]
                    val = int(cmd_args[1])
                    self.graphics.set_probe_value(var, val)

            elif ret_str.startswith('[PRB]'):

                # Clean the string
                ret_str = ret_str[5:]
                ret_str = self.cleanup_spaces(ret_str)
                ret_str = re.sub('[^0-9\-. ]+', '', ret_str)

                values = ret_str.split(" ")

                if len(values) == len(self.probe_list):
                    for i in range(len(values)):
                        var = self.probe_list[i]['name']
                        val = int(values[i])

                        self.graphics.set_probe_value(var, val)

                        if var == self.parameters.get_robot_x_variable():
                            self.robot.set_x(val)
                        elif var == self.parameters.get_robot_y_variable():
                            self.robot.set_y(val)
                        elif var == self.parameters.get_robot_a_variable():
                            self.robot.set_a(val)

                if self.parameters.get_robot_update_data():
                    self.graphics.table.add_robot_pos(self.robot.get_pos())

            elif ret_str.startswith('[VAR]'):

                # Display, it is not spammed on screen and would look odd with the header only
                # TODO: remove echo mode from target, put instead interactive mode which does not echo nor
                # display headers
                self.console.append_text(ret_str)

                # Clean the string
                ret_str = ret_str[5:]
                ret_str = self.cleanup_spaces(ret_str)
                ret_str = re.sub('[^a-zA-Z0-9_./ ]+', '', ret_str)

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

            # Default: print string
            else:
                self.console.append_text(ret_str)

        except:
            pass

