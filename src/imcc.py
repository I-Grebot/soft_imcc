#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Qt Libraries
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QDockWidget, QTabWidget, QVBoxLayout, QGridLayout
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import numpy as np

# PyQtGraph
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import *
import pyqtgraph.console
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType


# User-Interface for this module
from ui.imcc import Ui_imcc

# Other modules dependencies
from stm32flash import Stm32Flash
from console import Console
from configuration import Configuration
from parameters import Parameters
from cli import Cli


class IMCC(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_imcc()
        self.ui.setupUi(self)

        self.center_dock_layout = None

        self.parameters = Parameters()
        self.cli = Cli()

        # Set some global options
        pg.setConfigOptions(antialias=True)

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
        self.center_dock = QDockWidget()
        self.center_dock.setAllowedAreas(QtCore.Qt.NoDockWidgetArea)
        self.center_dock.setWindowTitle("Main viewer")
        self.center_dock.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
        self.setCentralWidget(self.center_dock)
        self.center_dock_area = DockArea(self.center_dock)
        self.center_dock.setWidget(self.center_dock_area)

        # Test some plotting dock
        plot_dock = Dock("Plot", size=(500, 400), closable=True, autoOrientation=False)
        self.center_dock_area.addDock(plot_dock, 'top')
        plot_widget = pg.PlotWidget(title="This is a test")

        pen_act = pg.mkPen((0, 200, 0, 255), width=2)
        pen_des = pg.mkPen((200, 0, 0, 255), width=2)
        brush_fill = (100, 0, 100, 100)

        self.nb_points = 500
        self.step = 0.1
        self.cnt = 0
        # self.x = np.arange(0.0, self.nb_points, 1.0)

        #self.x = list()
        #self.y1 = list()
        self.x = np.arange(-self.nb_points*self.step, 0, self.step)
        self.y1 = np.zeros(self.nb_points)
        # self.y1 = np.sin(np.radians(self.x))
        # self.y2 = (3 / 4) * np.cos(np.radians(2 * self.x))

        self.plot1 = plot_widget.plot(x=self.x, y=self.y1, pen=pen_act)
        # self.plot2 = plot_widget.plot(x=self.x, y=self.y2, pen=pen_des)
        # self.fill = pg.FillBetweenItem(self.plot1, self.plot2, brush=brush_fill)
        #self.plot1.enableAutoRange(True)
        #self.plot2.enableAutoRange(True)
        # plot_widget.addItem(self.fill)

        plot_widget.showGrid(x=True, y=True)
        plot_dock.addWidget(plot_widget)

    #     self.timer = QtCore.QTimer()
    #     self.timer.timeout.connect(self.update_data)
    #     self.timer.start(50)
    #
    # def update_data(self):
    #
    #     self.y1 = np.roll(self.y1, -1)
    #     self.y2 = np.roll(self.y2, -3)
    #     self.plot1.setData(self.x, self.y1)
    #     self.plot2.setData(self.x, self.y2)


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

            # print(cmd_args[0], x, y, a)

            # if len(self.y1) >= self.nb_points:
            #     self.x.pop(0)
            #     self.y1.pop(0)
            #
            # self.x.append(self.cnt)
            # self.y1.append(x)
            #

            self.x = np.roll(self.x, -1)
            self.x[self.nb_points-1] = self.cnt

            self.y1 = np.roll(self.y1, -1)
            self.y1[self.nb_points - 1] = x

            print(self.cnt, x)
            self.plot1.setData(self.x, self.y1)

            self.cnt += self.step

        except:
            pass


    def save_layout(self):
        self.center_dock_layout = self.center_dock_area.saveState()

    def load_layout(self):
        self.center_dock_area.restoreState(self.center_dock_layout)

