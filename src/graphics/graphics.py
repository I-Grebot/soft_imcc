#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import os
from PyQt5.QtWidgets import QVBoxLayout, QMainWindow
from pyqtgraph.parametertree import Parameter, ParameterTree
from .tableviewwidget import *
from .plots import *

from ui.graphics import Ui_Graphics

class Graphics(Ui_Graphics):

    params = [
        {'name': 'General Parameters', 'type': 'group', 'children': [
            {'name': 'Integer', 'type': 'int', 'value': 10},
        ]},
        {'name': 'Table View', 'type': 'group', 'children': [
            {'name': 'Visible', 'type': 'bool', 'value': True, 'tip': "Toggle visibility on/off"},
            {'name': 'Playground Image', 'type': 'group', 'children': [
                {'name': 'File', 'type': 'str', 'value': os.path.dirname(__file__) + '/../rc/table_2017.png'},
                {'name': 'Origin Coord. X', 'type': 'int', 'value': -40},
                {'name': 'Origin Coord. Y', 'type': 'int', 'value': -40},
                {'name': 'Scaling Factor', 'type': 'float', 'value': 3000/1146, 'decimals': 4, 'suffix': 'px/mm'},
                {'name': 'Update', 'type': 'action'}
            ]}
        ]},
        PlotsGroup(name="Plots"),
    ]

    def __init__(self):
        self.win = QMainWindow()
        self.setupUi(self.win)

        # Set some PyQtGraph global options
        pg.setConfigOptions(antialias=True)
        pg.setConfigOptions(imageAxisOrder='row-major')

        # Setup dock area and graphics parameter view
        self.dock_area = DockArea()
        self.graphics_parameter = ParameterTree(showHeader=False)
        self.p = Parameter.create(name='params', type='group', children=self.params)
        self.graphics_parameter.setParameters(self.p, showTop=False)

        # Setup other stuffs
        self.setup_table_view()
        self.setup_layout()

        # Bind slots
        self.connect()


    def setup_table_view(self):
        self.dock_table = Dock("Table View", closable=False, autoOrientation=False)
        self.dock_area.addDock(self.dock_table, 'top')

        self.table = TableViewWidget()
        self.dock_table.addWidget(self.table)

        # Load default settings
        self.update_table_playground()

        # Some default states
        self.table.add_robot_pos(0, 0, 90)
        self.table.update_target_pos(1500, 1000)

    def update_table_playground(self):

        self.table.playground_filename = \
            self.p.param('Table View').param('Playground Image').param('File').value()

        self.table.playground_origin_coord_px = \
            QPoint(self.p.param('Table View').param('Playground Image').param('Origin Coord. X').value(),
                   self.p.param('Table View').param('Playground Image').param('Origin Coord. Y').value())

        self.table.px_to_mm = \
            self.p.param('Table View').param('Playground Image').param('Scaling Factor').value()

        self.table.draw_playground()

    def setup_layout(self):
        layout_parameters = QVBoxLayout()
        layout_parameters.addWidget(self.graphics_parameter)
        self.widget_parameters.setLayout(layout_parameters)

        layout_graphics = QVBoxLayout()
        layout_graphics.addWidget(self.dock_area)
        self.widget_graphics.setLayout(layout_graphics)

        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 0)

    def connect(self):

        # TableView
        self.p.param('Table View').param('Visible').sigValueChanged.connect(
            lambda: self.dock_table.setVisible(self.p.param('Table View').param('Visible').value()))

        self.p.param('Table View').param('Playground Image').param('Update').sigActivated.connect(
            self.update_table_playground)

        # Plots
        self.p.param('Plots').sigChildAdded.connect(self.add_plot_window)
        self.p.param('Plots').sigChildRemoved.connect(self.remove_plot_window)
        self.p.param('Plots').plots_changed.connect(self.add_plot)

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



