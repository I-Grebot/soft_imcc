#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import os
from PyQt5.QtWidgets import QVBoxLayout, QMainWindow
from pyqtgraph.parametertree import Parameter, ParameterTree
from .tableviewwidget import *
from .plots import *

from ui.graphics import Ui_Graphics

class Graphics(Ui_Graphics, QObject):

    goto_clicked = pyqtSignal([int, int], name='gotoClicked')

    params = [
        {'name': 'Table View', 'type': 'group', 'children': [
            {'name': 'Visible', 'type': 'bool', 'value': True, 'tip': "Toggle table-view visibility on/off"},
            {'name': 'Grid', 'type': 'bool', 'value': True, 'tip': "Toggle grid on/off"},
            {'name': 'CrossHair', 'type': 'bool', 'value': False, 'tip': "Toggle crosshair on/off"},
            {'name': 'Playground Image', 'type': 'group', 'children': [
                {'name': 'File', 'type': 'str', 'value': 'rc/table_2017.png'},
                {'name': 'Origin Coord. X', 'type': 'int', 'value': -41},
                {'name': 'Origin Coord. Y', 'type': 'int', 'value': -87},
                {'name': 'Scaling Factor', 'type': 'float', 'value': 3000/1146, 'decimals': 4, 'suffix': 'px/mm'},
                {'name': 'Update', 'type': 'action'}
            ]},

            {'name': 'Robot', 'type': 'group', 'children': [
                {'name': 'Visible', 'type': 'bool', 'value': True, 'tip': "Toggle visibility on/off"},
                {'name': 'History', 'type': 'bool', 'value': True, 'tip': "Toggle history on/off"},
                {'name': 'Color', 'type': 'color', 'value': (0, 0, 200, 150), 'tip': "Foreground color"}
            ]},

            {'name': 'Points Of Interest', 'type': 'group', 'children': [
                {'name': 'Visible', 'type': 'bool', 'value': True, 'tip': "Toggle visibility on/off"},
                {'name': 'Size', 'type': 'int', 'value': 50},
                {'name': 'Color', 'type': 'color', 'value': (200, 0, 0, 150), 'tip': "Foreground color"}
            ]},

            {'name': 'Path-finder', 'type': 'group', 'children': [
                {'name': 'Polygons visible', 'type': 'bool', 'value': True, 'tip': "Toggle PF polygons visibility on/off"},
                {'name': 'Paths visible', 'type': 'bool', 'value': True, 'tip': "Toggle PF polygons visibility on/off"},
            ]},
        ]},
        PlotsGroup(name="Plots"),
    ]

    def __init__(self):

        super(Graphics, self).__init__()

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
        self.pan_mode = True
        self.goto_mode = False

        # Bind slots
        self.connect()


    def setup_table_view(self):
        self.dock_table = Dock("Table View", closable=False, autoOrientation=False)
        self.dock_area.addDock(self.dock_table, 'top')

        self.table = TableViewWidget()
        self.dock_table.addWidget(self.table)

        # Load default settings
        self.update_table_playground()

        # Default states
        self.table.set_grid_visible(self.p.param('Table View').param('Grid').value())
        self.table.set_crosshair_visible(self.p.param('Table View').param('CrossHair').value())

        self.table.set_robot_visible(self.p.param('Table View').param('Robot').param('Visible').value())
        self.table.set_robot_history_visible(self.p.param('Table View').param('Robot').param('History').value())
        self.table.set_robot_color(self.p.param('Table View').param('Robot').param('Color').value())

        self.table.set_poi_visible(self.p.param('Table View').param('Points Of Interest').param('Visible').value())
        self.table.set_poi_color(self.p.param('Table View').param('Points Of Interest').param('Color').value())
        self.table.set_poi_size(self.p.param('Table View').param('Points Of Interest').param('Size').value())

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

        self.p.param('Table View').param('Grid').sigValueChanged.connect(
            lambda: self.table.set_grid_visible(self.p.param('Table View').param('Grid').value()))

        self.p.param('Table View').param('CrossHair').sigValueChanged.connect(
            lambda: self.table.set_crosshair_visible(self.p.param('Table View').param('CrossHair').value()))

        self.p.param('Table View').param('Robot').param('Visible').sigValueChanged.connect(
            lambda: self.table.set_robot_visible(self.p.param('Table View').param('Robot').param('Visible').value()))

        self.p.param('Table View').param('Robot').param('History').sigValueChanged.connect(
            lambda: self.table.set_robot_history_visible(self.p.param('Table View').param('Robot').param('History').value()))

        self.p.param('Table View').param('Robot').param('Color').sigValueChanged.connect(
            lambda: self.table.set_robot_color(self.p.param('Table View').param('Robot').param('Color').value()))

        self.p.param('Table View').param('Points Of Interest').param('Visible').sigValueChanged.connect(
            lambda: self.table.set_poi_visible(self.p.param('Table View').param('Points Of Interest').param('Visible').value()))

        self.p.param('Table View').param('Points Of Interest').param('Color').sigValueChanged.connect(
            lambda: self.table.set_poi_color(self.p.param('Table View').param('Points Of Interest').param('Color').value()))

        self.p.param('Table View').param('Points Of Interest').param('Size').sigValueChanged.connect(
            lambda: self.table.set_poi_size(self.p.param('Table View').param('Points Of Interest').param('Size').value()))

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



    # Show / Hide all graphs
    def action_view_graphs(self, state):

        windows = self.p.param('Plots').children()
        for i in range(len(windows)):

            # Force to hide
            if state is False:
                windows[i].dock.setVisible(False)

            # Restore parameter's visibility
            else:
                windows[i].update_visibility()

    def left_click_playground(self, x, y):
        if self.pan_mode:
            print('Mark', x, y)

        if self.goto_mode:
            self.table.update_target_pos(x, y)
            self.goto_clicked.emit(x, y)
