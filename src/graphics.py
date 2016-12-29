#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
from PIL import Image
from collections import deque

# Qt Libraries
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QDockWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QMainWindow
from PyQt5.QtCore import *

# PyQtGraph
import pyqtgraph as pg
from pyqtgraph.dockarea import *
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType

# Numpy
import numpy as np

from ui.graphics import Ui_Graphics

# Subclassing of pyqtgraph's AxisItem to display timed graphs
class TimeAxisItem(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        strns = []
        for x in values:
            try:
                strns.append(time.strftime("%H:%M:%S", time.localtime(x)))
            except ValueError:  # Windows can't handle dates before 1970
                strns.append('')
        return strns

# A single plot configuration
class PlotParameter(pTypes.GroupParameter):

    BUFFER_DEPTH = 200

    def __init__(self, **opts):
        opts['type'] = 'str'

        pTypes.GroupParameter.__init__(self, **opts)
        self.addChild({'name': 'Visible', 'type': 'bool', 'value': True, 'tip': "Toggle visibility on/off"})
        self.addChild({'name': 'Color', 'type': 'color', 'value': "FF0", 'tip': "Foreground color"})
        self.addChild({'name': 'Width', 'type': 'float', 'value': 2, 'limits': (0, 10), 'default': 2})
        self.addChild({'name': 'Style', 'type': 'list', 'values': {
                        "Solid"         : QtCore.Qt.SolidLine,
                        "Dash"          : QtCore.Qt.DashLine,
                        "Dot"           : QtCore.Qt.DotLine,
                        "Dash-Dot"      : QtCore.Qt.DashDotLine,
                        "Dash-Dot-Dot"  : QtCore.Qt.DashDotDotLine
                    }, 'value': QtCore.Qt.SolidLine})

        self.data = deque(maxlen=self.BUFFER_DEPTH)

        self.pen = pg.mkPen(color=self.param('Color').value(),
                            width=self.param('Width').value(),
                            style=self.param('Style').value())

        # Holder for the plotDataItem
        self.widget = pg.PlotWidget()
        self.plot = pg.PlotDataItem()

        # Slots Connections
        self.param('Color').sigValueChanged.connect(self.update_color)
        self.param('Width').sigValueChanged.connect(self.update_width)
        self.param('Style').sigValueChanged.connect(self.update_style)
        self.param('Visible').sigValueChanged.connect(self.update_visibility)
        self.sigRemoved.connect(self.remove_plot)

    def get_plot(self):
        return self.plot

    def setup_plot(self, widget):
        self.widget = widget
        self.plot = widget.plot(pen=self.pen, name=self.value())

    def update_color(self):
        self.pen.setColor(self.param('Color').value())
        self.plot.setPen(self.pen)

    def update_width(self):
        self.pen.setWidth(self.param('Width').value())
        self.plot.setPen(self.pen)

    def update_style(self):
        self.pen.setStyle(self.param('Style').value())
        self.plot.setPen(self.pen)

    def update_visibility(self):
        self.plot.setVisible(self.param('Visible').value())

    def remove_plot(self):
        self.widget.removeItem(self.plot)

    def add_data(self, timestamp, value):
        self.data.append({'x': timestamp, 'y': value})
        x = [item['x'] for item in self.data]
        y = [item['y'] for item in self.data]
        self.plot.setData(x=x, y=y)

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
        self.dock = Dock(self.name(), closable=False, autoOrientation=False)
        self.dock_area = DockArea()
        self.plot_widget = pg.PlotWidget(axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.plot_widget.addLegend()

        self.update_grid()
        self.dock.addWidget(self.plot_widget) # Separate plot_widget per dock todo

        # Slots connections
        self.sigNameChanged.connect(self.update_name)
        self.sigRemoved.connect(self.remove_dock)
        self.param('Grid').sigValueChanged.connect(self.update_grid)
        self.param('Visible').sigValueChanged.connect(self.update_visibility)

    def addNew(self, typ):
        nb_plots = len(self.childs)-2 # 2 statics
        new_kid = self.addChild(PlotParameter(name='Plot %s' %typ, value=typ, removable=True, renamable=False),
                                autoIncrementName=True)
        new_kid.param('Color').setValue(self.COLORS[nb_plots % len(self.COLORS)])
        new_kid.setup_plot(self.plot_widget)

    def get_dock(self):
        return self.dock

    def setup_dock(self, dock_area):
        self.dock_area = dock_area
        self.dock_area.addDock(self.dock, 'bottom')

    def update_name(self):
        self.dock.setTitle(self.name())

    def update_grid(self):
        self.plot_widget.showGrid(x=self.param('Grid').value(), y=self.param('Grid').value())

    def update_visibility(self):
        self.dock.setVisible(self.param('Visible').value())

    def remove_dock(self):
        self.dock.close()

# Custom group for grouping plots. Add an action button for adding a new plot
class PlotsGroup(pTypes.GroupParameter):

    plots_changed = pyqtSignal(PlotWindowParameter, PlotParameter, name="plotsChanged")

    def __init__(self, **opts):
        opts['addText'] = "Add Window"
        pTypes.GroupParameter.__init__(self, **opts)

    def addNew(self):
        new_kid = self.addChild(
            PlotWindowParameter(name="Plot Window %d" % (len(self.childs) + 1),
                                removable=True,
                                renamable=True),
            autoIncrementName=True)
        new_kid.sigChildAdded.connect(self.add_plot)

    def add_plot(self, child, index):
        self.plots_changed.emit(child, index)

class Graphics(Ui_Graphics):

    params = [
        {'name': 'General Parameters', 'type': 'group', 'children': [
            {'name': 'Integer', 'type': 'int', 'value': 10},
        ]},
        {'name': 'Table View', 'type': 'group', 'children': [
            {'name': 'Visible', 'type': 'bool', 'value': True, 'tip': "Toggle visibility on/off"}
        ]},
        PlotsGroup(name="Plots"),
    ]

    def __init__(self):
        self.win = QMainWindow()
        self.setupUi(self.win)

        # Set some PyQtGraph global options
        pg.setConfigOptions(antialias=True)
        pg.setConfigOptions(imageAxisOrder='row-major')

        self.dock_area = DockArea()
        self.graphics_parameter = ParameterTree(showHeader=False)

        self.p = Parameter.create(name='params', type='group', children=self.params)

        self.p.param('Plots').sigChildAdded.connect(self.add_plot_window)
        self.p.param('Plots').sigChildRemoved.connect(self.remove_plot_window)
        self.p.param('Plots').plots_changed.connect(self.add_plot)

        self.graphics_parameter.setParameters(self.p, showTop=False)

        self.setup_table_view()
        self.setup_layout()


    def setup_table_view(self):
        self.dock_table = Dock("Table View", closable=False, autoOrientation=False)
        self.dock_area.addDock(self.dock_table, 'top')

        self.table_widget = pg.GraphicsLayoutWidget()
        self.table_widget.setBackground('w')
        self.table_viewbox = self.table_widget.addViewBox(row=1, col=1)
        self.table_img = pg.ImageItem()
        self.table_viewbox.addItem(self.table_img)
        self.table_viewbox.setAspectLocked(True)

        self.dock_table.addWidget(self.table_widget)

        # imagedata = np.random.random((256, 256, 4))
        # ii = pg.ImageItem(imagedata)

        # self.table_viewbox.addItem(ii)


        try:
            self.table_image = Image.open("rc/table_2017.png", mode="r")
            print(self.table_image.format, self.table_image.size, self.table_image.mode)

            data = np.array(self.table_image)
            self.table_img = pg.ImageItem(data)
            self.table_viewbox.addItem(self.table_img)

        except IOError:
            print('Error: cannot open Table image file')

    def setup_layout(self):
        layout_parameters = QVBoxLayout()
        layout_parameters.addWidget(self.graphics_parameter)
        self.widget_parameters.setLayout(layout_parameters)

        layout_graphics = QVBoxLayout()
        layout_graphics.addWidget(self.dock_area)
        self.widget_graphics.setLayout(layout_graphics)

        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 0)

    def add_plot_window(self, child, index):
        index.setup_dock(self.dock_area)
        print('Added window ! # In list =', len(self.p.param('Plots').childs))
        print('Window name = ', index.name(), ' value = ', index.value())

    def remove_plot_window(self, child):
        print('Removed window ! # In list =', len(self.p.param('Plots').childs))

    def add_plot(self, child, index):
        print('Added plot', index.name(),'in win', child.name())
        self.get_probe_list()

    def get_probe_list(self):
        probe_set = set()
        windows = self.p.param('Plots').children()
        for i in range(len(windows)):
            plots = windows[i].children()
            for j in range(len(plots)):
                if plots[j].name().startswith('Plot '):
                    probe_set.add(plots[j].value())
        print(*probe_set)
        return probe_set

    def set_probe_value(self, probe, new_value):

        #TODO: proper signaling callback in PlotParameter class

        # Look for a probe that matches...
        windows = self.p.param('Plots').children()
        for i in range(len(windows)):
            plots = windows[i].children()
            for j in range(len(plots)):
                if plots[j].value() == probe:
                    plots[j].add_data(time.time(), new_value)

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



