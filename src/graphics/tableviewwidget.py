#!/usr/bin/python3
# -*- coding: utf-8 -*-

from collections import deque
from PIL import Image
from PyQt5.QtCore import *
import pyqtgraph as pg
import numpy as np

class TableViewWidget(pg.GraphicsLayoutWidget):

    # Constants
    ROBOT_POS_BUFFER_SIZE = 200

    # Attributes
    playground_size_px = tuple()

    def __init__(self):
        super(TableViewWidget, self).__init__()

        # Constants from rules TODO
        self.playground_size_mm = [3000, 2000]

        # Define general settings and the main viewbox
        self.setBackground('w')
        self.viewbox = self.addViewBox(row=2, col=1)
        self.viewbox.setAspectLocked(True)

        # Playground image
        self.playground_img = pg.ImageItem()
        self.playground_img_data = pg.ImageItem()
        self.viewbox.addItem(self.playground_img_data)

        # Plot Widget for overlayed markings
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setXRange(0, self.playground_size_mm[0], 0)
        self.plot_widget.setYRange(0, self.playground_size_mm[1], 0)

        # Constant from image - default dummies value (not working ~ need to be defined externaly)
        self.playground_filename = "table.png"
        self.playground_origin_coord_px = QPoint(0, 0)
        self.px_to_mm = 1.0
        self.image_size_px = (0, 0)

        # Parameters/Variables
        self.robot_radius = 300
        self.robot_pos = deque(maxlen=self.ROBOT_POS_BUFFER_SIZE)

        # Draw all table view items
        # self.draw_playground()
        self.draw_table_outline()
        self.draw_robot()
        self.draw_target()

    def draw_playground(self):
        try:
            self.playground_img = Image.open(self.playground_filename, mode="r")
            self.playground_img_data.setImage(np.array(self.playground_img), opacity=1.0)
            self.playground_img_data.setScale(self.px_to_mm)
            self.playground_img_data.setPos(self.playground_origin_coord_px * self.px_to_mm)
            self.image_size_px = self.playground_img.size

        except IOError:
            print('Error: cannot open Table image file %s' %self.playground_filename)

    def draw_table_outline(self):

        orig = [0, 0]
        size = self.playground_size_mm

        # Table boundaries
        x = [orig[0], orig[0]+size[0], orig[0]+size[0], orig[0], orig[0]]
        y = [orig[1], orig[1], orig[1]+size[1], orig[1]+size[1], orig[1]]

        self.outline_plot = self.plot_widget.plot(pen=pg.mkPen(color='k', width=2),
                                                  pxMode=False, name="Outline",
                                                  x=x, y=y)

        self.viewbox.addItem(self.outline_plot)

    def draw_robot(self):

        # Plot for the current position
        self.robot_pos_plot = self.plot_widget.plot(pen=None,
                                                    symbol='o', symbolPen=None, symbolSize=self.robot_radius, pxMode=False,
                                                    symbolBrush=(0, 0, 200, 150),
                                                    name='Robot position')
        self.viewbox.addItem(self.robot_pos_plot)

        # Plot for the positions history
        self.robot_pos_hist_plot = self.plot_widget.plot(pen=pg.mkPen(color=(0, 0, 200, 200), width=5),
                                                         symbol=None,
                                                         pxMode=True,
                                                         name='Robot position history')
        self.viewbox.addItem(self.robot_pos_hist_plot)

        # Plot arrow for the current orientation (angle)
        self.robot_angle_arrow = pg.ArrowItem(angle=180, # Required so it points outwards
                                              pen=(200, 200, 200, 255),
                                              brush=(0, 0, 200, 210),
                                              tipAngle=30, baseAngle=-30,
                                              headLen=self.robot_radius/2,
                                              tailLen=None,
                                              pxMode=False)
        self.viewbox.addItem(self.robot_angle_arrow)

    def draw_target(self):
        self.target_pos_plot = self.plot_widget.plot(pen=None,
                                                     symbol='+', symbolPen=None, symbolSize=100, pxMode=False,
                                                     symbolBrush=(200, 0, 0, 220),
                                                     name='Target position')
        self.viewbox.addItem(self.target_pos_plot)

    def add_robot_pos(self, x, y, a):
        self.robot_pos.append({'x': x, 'y': y, 'a': a})
        x = [item['x'] for item in self.robot_pos]
        y = [item['y'] for item in self.robot_pos]
        a = [item['a'] for item in self.robot_pos]

        last_x = x[len(x)-1]
        last_y = y[len(y)-1]
        last_a = a[len(a)-1]

        # Plot the current location (big plot) with the latest entry
        self.robot_pos_plot.setData(x=[last_x], y=[last_y])

        # Plot the history location
        self.robot_pos_hist_plot.setData(x=x, y=y)

        # Plot the arrow displaying the current orientation
        self.robot_angle_arrow.setPos(QPoint(last_x + self.robot_radius/2*np.cos(np.radians(last_a)),
                                             last_y + self.robot_radius/2*np.sin(np.radians(last_a))))
        self.robot_angle_arrow.setRotation(last_a) # Bug in the setStyle of ArrowItem() class

    def update_target_pos(self, x, y):
        self.target_pos_plot.setData(x=[x], y=[y])

