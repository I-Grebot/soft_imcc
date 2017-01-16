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
            ]},
            {'name': 'Robot', 'type': 'group', 'children': [
                {'name': 'Visible', 'type': 'bool', 'value': True, 'tip': "Toggle visibility on/off"},
                {'name': 'History', 'type': 'bool', 'value': True, 'tip': "Toggle history on/off"},
                {'name': 'Color', 'type': 'color', 'value': (0, 0, 200, 150), 'tip': "Foreground color"}
            ]},
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
        self.probe_list = list()
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
        self.table.add_robot_pos({'x': 0, 'y': 0, 'a': 0})
        self.table.update_target_pos(1500, 1000)
        self.table.set_crosshair_visible(False)

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

        # Toolbar
        self.actionCursor.triggered.connect(self.action_cursor)
        self.actionGoto.triggered.connect(self.action_goto)

        # TableView
        self.p.param('Table View').param('Visible').sigValueChanged.connect(
            lambda: self.dock_table.setVisible(self.p.param('Table View').param('Visible').value()))

        self.p.param('Table View').param('Playground Image').param('Update').sigActivated.connect(
            self.update_table_playground)

        self.p.param('Table View').param('Robot').param('Visible').sigValueChanged.connect(
            lambda: self.table.set_robot_visible(self.p.param('Table View').param('Robot').param('Visible').value()))

        self.p.param('Table View').param('Robot').param('History').sigValueChanged.connect(
            lambda: self.table.set_robot_history_visible(self.p.param('Table View').param('Robot').param('History').value()))

        self.p.param('Table View').param('Robot').param('Color').sigValueChanged.connect(
            lambda: self.table.set_robot_color(self.p.param('Table View').param('Robot').param('Color').value()))

        self.table.left_click_playground[int, int].connect(self.left_click_playground)

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
        # print(*probe_set)
        return probe_set

    def set_probe_list(self, probe_list):
        self.probe_list = probe_list
        windows = self.p.param('Plots').children()
        self.p.param('Plots').set_probe_list(self.probe_list)

        for i in range(len(windows)):
            windows[i].set_probe_list(self.probe_list)


    def set_probe_value(self, probe, new_value):

        #TODO: proper signaling callback in PlotParameter class

        # Look for a probe that matches...
        windows = self.p.param('Plots').children()
        for i in range(len(windows)):
            plots = windows[i].children()
            for j in range(len(plots)):
                if plots[j].value() == probe:
                    plots[j].add_data(time.time(), new_value)

    def action_cursor(self, val):
        if val:
            if self.actionGoto.isChecked():
                self.actionGoto.setChecked(False)

        self.table.set_crosshair_visible(val)

    def action_goto(self, val):
        if val:
            if self.actionCursor.isChecked():
                self.actionCursor.setChecked(False)

        self.table.set_crosshair_visible(val)

    def left_click_playground(self, x, y):
        if self.actionCursor.isChecked():
            print('Mark', x, y)

        if self.actionGoto.isChecked():
            print('Goto', x, y)



