#!/usr/bin/python3
# -*- coding: utf-8 -*-

from collections import deque
from PyQt5.QtCore import *
import pyqtgraph as pg
from pyqtgraph.dockarea import *
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.parametertree.parameterTypes as pTypes
from .timeaxisitem import TimeAxisItem
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
        self.sigNameChanged.connect(lambda: self.dock.setTitle(self.name()))
        self.sigRemoved.connect(lambda: self.dock.close())
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

    def update_grid(self):
        self.plot_widget.showGrid(x=self.param('Grid').value(), y=self.param('Grid').value())

    def update_visibility(self):
        self.dock.setVisible(self.param('Visible').value())

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
