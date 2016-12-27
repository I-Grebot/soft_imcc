#!/usr/bin/python3
# -*- coding: utf-8 -*-

import colorsys

# Qt Libraries
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QDockWidget, QTabWidget, QHBoxLayout, QGridLayout
from PyQt5.QtCore import *

# PyQtGraph
import pyqtgraph as pg
from pyqtgraph.dockarea import *
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType

# Numpy
import numpy as np

# A single plot configuration
class PlotParameter(pTypes.GroupParameter):
    def __init__(self, **opts):
        opts['type'] = 'str'

        pTypes.GroupParameter.__init__(self, **opts)
        self.addChild({'name': 'Color', 'type': 'color', 'value': "FF0", 'tip': "Foreground color"})
        self.addChild({'name': 'Width', 'type': 'float', 'value': 2, 'limits': (1, 10), 'default': 2})
        self.addChild({'name': 'Style', 'type': 'list', 'values': {
                        "Solid"         : QtCore.Qt.SolidLine,
                        "Dash"          : QtCore.Qt.DashLine,
                        "Dot"           : QtCore.Qt.DotLine,
                        "Dash-Dot"      : QtCore.Qt.DashDotLine,
                        "Dash-Dot-Dot"  : QtCore.Qt.DashDotDotLine
                    }, 'default': "Solid"})

        # Data
        self.nb_points = 500
        self.step = 0.1
        self.cnt = 0

        self.x = np.arange(-self.nb_points * self.step, 0, self.step)
        self.y = np.zeros(self.nb_points)

        self.pen = pg.mkPen(color=self.param('Color').value(),
                            width=self.param('Width').value(),
                            style=self.param('Style').value())

        # Holder for the plotDataItem
        self.plot = pg.PlotDataItem()

        # Slots Connections
        self.param('Color').sigValueChanged.connect(self.update_color)
        self.param('Width').sigValueChanged.connect(self.update_width)
        self.param('Style').sigValueChanged.connect(self.update_style)

    def setup_plot(self, widget):
        self.plot = widget.plot(x=self.x, y=self.y, pen=self.pen)

    def update_color(self):
        self.pen.setColor(self.param('Color').value())
        self.plot.setPen(self.pen)

    def update_width(self):
        self.pen.setWidth(self.param('Width').value())
        self.plot.setPen(self.pen)

    def update_style(self):
        self.pen.setStyle(self.param('Style').value())
        self.plot.setPen(self.pen)


# A plot window, that can hold multiple plots
class PlotWindowParameter(pTypes.GroupParameter):

    # Default colors
    COLORS = ["C00", "0C0", "00C",
              "CC0", "C0C", "0CC"]

    def __init__(self, **opts):
        opts['type'] = 'group'
        opts['addText'] = "Add Plot"
        opts['addList'] = ['robot.cs.pos.x', 'robot.cs.pos.y', 'robot.cs.pos.a']

        pTypes.GroupParameter.__init__(self, **opts)
        self.addChild({'name': 'Visible', 'type': 'bool', 'value': True, 'tip': "Toggle visibility on/off"})
        self.addChild({'name': 'Grid', 'type': 'bool', 'value': True, 'tip': "Toggle grid on/off"})

        # Actual dock & plot widget
        self.dock = Dock(self.name(), size=(500, 400), closable=True, autoOrientation=False)
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.showGrid(x=True, y=True) # Parameters TODO
        self.dock.addWidget(self.plot_widget) # Separate plot_widget per dock todo

        # Slots connections
        self.sigNameChanged.connect(self.update_name)

    # TODO: Prevent adding twice the same plot (this is stupid)
    def addNew(self, typ):
        nb_plots = len(self.childs)-2 # 2 statics

        new_kid = self.addChild(PlotParameter(name=typ, value=typ, removable=True, renamable=False),
                                autoIncrementName=True)
        new_kid.param('Color').setValue(self.COLORS[nb_plots % len(self.COLORS)])
        new_kid.setup_plot(self.plot_widget)


    def getDock(self):
        return self.dock

    def update_name(self):
        self.dock.setTitle(self.name())

# Custom group for grouping plots. Add an action button for adding a new plot
class PlotsGroup(pTypes.GroupParameter):

    plots_changed = pyqtSignal(PlotWindowParameter, PlotParameter, name="plotsChanged")

    def __init__(self, **opts):
        opts['addText'] = "Add Window"
        pTypes.GroupParameter.__init__(self, **opts)

    def addNew(self):
        new_kid = self.addChild(
            PlotWindowParameter(name="Plot Window %d" % (len(self.childs) + 1),
                                removable=True, renamable=True),
            autoIncrementName=True)
        new_kid.sigChildAdded.connect(self.add_plot)

    def add_plot(self, child, index):
        self.plots_changed.emit(child, index)


class Graphics(QDockWidget):

    params = [
        {'name': 'General Parameters', 'type': 'group', 'children': [
            {'name': 'Integer', 'type': 'int', 'value': 10},
        ]},
        PlotsGroup(name="Plots"),
    ]

    def __init__(self):
        super(Graphics, self).__init__()

        # Set some PyQtGraph global options
        pg.setConfigOptions(antialias=True)

        self.dock_area = DockArea(self)
        self.graphics_parameter = ParameterTree()

        self.p = Parameter.create(name='params', type='group', children=self.params)

        self.p.param('Plots').sigChildAdded.connect(self.add_plot_window)
        self.p.param('Plots').sigChildRemoved.connect(self.remove_plot_window)

        self.p.param('Plots').plots_changed.connect(self.add_plot)

        self.graphics_parameter.setParameters(self.p, showTop=False)

        # Dock Widget options
        self.setAllowedAreas(QtCore.Qt.NoDockWidgetArea)
        self.setWindowTitle("Graphics viewer")
        self.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)


        self.setWidget(self.dock_area)

        self.plot_docks = list()

        new_plot_dock = Dock("Plot", size=(500, 400), closable=True, autoOrientation=False)
        self.plot_docks.append(new_plot_dock)

        self.parameters_dock = Dock("Graphics", size=(100, 400), closable=False)

        self.dock_area.addDock(new_plot_dock, 'top')
        self.dock_area.addDock(self.parameters_dock, 'right')

        # Parameters dock
        self.parameters_dock.addWidget(self.graphics_parameter)

        self.plot_widgets = list()



        # Plot widget test
        new_plot_widget = pg.PlotWidget(title="This is a test")

        pen_act = pg.mkPen((0, 200, 0, 255), width=2)
        pen_des = pg.mkPen((200, 0, 0, 255), width=2)
        brush_fill = (100, 0, 100, 100)

        self.nb_points = 500
        self.step = 0.1
        self.cnt = 0

        self.x = np.arange(-self.nb_points * self.step, 0, self.step)
        self.y1 = np.zeros(self.nb_points)
        self.y2 = np.zeros(self.nb_points)

        self.plot1 = new_plot_widget.plot(x=self.x, y=self.y1, pen=pen_act)
        self.plot2 = new_plot_widget.plot(x=self.x, y=self.y2, pen=pen_des)
        self.fill = pg.FillBetweenItem(self.plot1, self.plot2, brush=brush_fill)
        new_plot_widget.addItem(self.fill)

        new_plot_widget.showGrid(x=True, y=True)

        self.plot_widgets.append(new_plot_widget)

        new_plot_dock.addWidget(new_plot_widget)

        # self.plot_widgets[0].clear()

    def add_plot_window(self, child, index):
        print('Added window ! # In list = ', len(self.p.param('Plots').childs))
        print('Window name = ', index.name(), ' value = ', index.value())

        # new_plot_dock = Dock(index.name(), size=(500, 400), closable=True, autoOrientation=False)
        # self.plot_docks.append(new_plot_dock)
        # self.dock_area.addDock(new_plot_dock, 'bottom', self.plot_docks[0])
        self.dock_area.addDock(index.getDock())

        # new_plot_widget = pg.PlotWidget(title=index.name())

    def remove_plot_window(self, child):
        print('Removed window ! # In list = ', len(self.p.param('Plots').childs))

    def add_plot(self, child, index):
        print('Added plot ', index.name(),' in win ', child.name())

    def append_value(self, new_value):

        self.x = np.roll(self.x, -1)
        self.x[self.nb_points - 1] = self.cnt

        self.y1 = np.roll(self.y1, -1)
        self.y1[self.nb_points - 1] = new_value

        self.y2 = self.y1 + 5

        self.plot1.setData(self.x, self.y1)
        self.plot2.setData(self.x, self.y2)

        self.cnt += self.step

    # def save_layout(self):
    #     self.center_dock_layout = self.center_dock_area.saveState()
    #
    # def load_layout(self):
    #     self.center_dock_area.restoreState(self.center_dock_layout)



