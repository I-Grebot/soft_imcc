#!/usr/bin/python3
# -*- coding: utf-8 -*-

from collections import deque
from PIL import Image
from PyQt5.QtCore import *
import pyqtgraph as pg
from pyqtgraph.Point import Point
import numpy as np

class TableViewWidget(pg.GraphicsLayoutWidget):

    # Constants
    ROBOT_POS_BUFFER_SIZE = 200

    # Attributes
    playground_size_px = tuple()

    left_click_playground = pyqtSignal(int, int)

    def __init__(self):
        super(TableViewWidget, self).__init__()

        # Define general settings and the main viewbox
        self.setBackground('w')
        self.viewbox = self.addViewBox()
        self.viewbox.setAspectLocked(True)
        self.viewbox.disableAutoRange()
        # self.viewbox.setMenuEnabled(False)

        # Playground image
        self.playground_img = pg.ImageItem()
        self.playground_img_data = pg.ImageItem()
        self.viewbox.addItem(self.playground_img_data)

        # Plot Widget for overlayed markings
        self.plot_widget = pg.PlotWidget(lockAspect=True)
        self.plot_widget.disableAutoRange()

        # Constant from image - default dummies value (not working ~ need to be defined externaly)
        self.playground_filename = "table.png"
        self.playground_origin_coord_px = QPoint(0, 0)
        self.px_to_mm = 1.0
        self.image_size_px = (0, 0)
        self.playground_size_mm = [0, 0]

        # Parameters/Variables
        self.robot_radius = 10
        self.robot_pos = deque(maxlen=self.ROBOT_POS_BUFFER_SIZE)
        self.crosshair_visible = False

        # Draw all table view items
        # self.draw_playground()
        self.draw_table_outline()
        self.draw_grid()
        self.draw_crosshair()
        self.draw_robot()
        self.draw_target()

        # Proxys (connection) for mouse moves/clicks
        self.mouse_move_proxy = pg.SignalProxy(self.scene().sigMouseMoved, rateLimit=60,
                                               slot=self.mouse_moved)
        self.mouse_click_proxy = pg.SignalProxy(self.scene().sigMouseClicked, rateLimit=60,
                                                slot=self.mouse_clicked)

    def draw_playground(self):
        try:
            self.playground_img = Image.open(self.playground_filename, mode="r")
            self.playground_img_data.setImage(np.array(self.playground_img), opacity=1.0)
            self.playground_img_data.setScale(self.px_to_mm)
            self.playground_img_data.setPos(self.playground_origin_coord_px * self.px_to_mm)
            self.image_size_px = self.playground_img.size
            self.update_range()

        except IOError:
            print('Error: cannot open Table image file %s' %self.playground_filename)

    def draw_table_outline(self):

        self.outline_plot = self.plot_widget.plot(pen=pg.mkPen(color='k', width=2),
                                                  pxMode=False, name="Outline")
        self.viewbox.addItem(self.outline_plot)
        self.update_table_outline()

    def draw_grid(self):
        self.grid = pg.GridItem()
        self.viewbox.addItem(self.grid)

    def update_table_outline(self):

        orig = [0, 0]
        size = self.playground_size_mm

        # Calculate table boundaries
        x = [orig[0], orig[0] + size[0], orig[0] + size[0], orig[0], orig[0]]
        y = [orig[1], orig[1], orig[1] + size[1], orig[1] + size[1], orig[1]]

        # Update data
        self.outline_plot.setData(x, y)

    def update_range(self):

        # Calculate range (playground image must fit)
        image_origin_mm = QPoint(self.playground_origin_coord_px.x() * self.px_to_mm,
                                 self.playground_origin_coord_px.x() * self.px_to_mm)

        image_end_mm = QPoint(image_origin_mm.x() + (self.image_size_px[0] * self.px_to_mm),
                              image_origin_mm.y() + (self.image_size_px[1] * self.px_to_mm))

        self.viewbox.setXRange(min=image_origin_mm.x(), max=image_end_mm.x(), padding=None)
        self.viewbox.setYRange(min=image_origin_mm.y(), max=image_end_mm.y(), padding=None)

    def draw_crosshair(self):

        self.cross_v_line = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen(color='r', width=1))
        self.cross_h_line = pg.InfiniteLine(angle=0, movable=False, pen=pg.mkPen(color='r', width=1))

        self.viewbox.addItem(self.cross_v_line, ignoreBounds=True)
        self.viewbox.addItem(self.cross_h_line, ignoreBounds=True)

        # Coordinate label
        self.mouse_coord_label = pg.LabelItem(justify='left')
        self.addItem(self.mouse_coord_label)

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

        # Coordinate label
        self.robot_coord_label = pg.LabelItem(justify='left')
        self.addItem(self.robot_coord_label)

    def set_playground_size(self, width, height):
        self.playground_size_mm[0] = width
        self.playground_size_mm[1] = height

        self.update_table_outline()

    def set_crosshair_visible(self, visible):
        self.crosshair_visible = visible

        if not visible:
            self.cross_v_line.setVisible(visible)
            self.cross_h_line.setVisible(visible)

    def set_grid_visible(self, visible):
        self.grid.setVisible(visible)

    def set_robot_visible(self, visible):
        self.robot_pos_plot.setVisible(visible)
        self.robot_angle_arrow.setVisible(visible)

    def set_robot_history_visible(self, visible):
        self.robot_pos_hist_plot.setVisible(visible)

    def set_robot_color(self, color):
        self.robot_pos_plot.setSymbolBrush(color)
        color.setAlpha(210)
        self.robot_angle_arrow.setBrush(color)
        color.setAlpha(200)
        self.robot_pos_hist_plot.setPen(pg.mkPen(color=color, width=5))

    def set_robot_radius(self, radius):
        self.robot_radius = radius
        self.robot_pos_plot.setSymbolSize(self.robot_radius*2)

        # Redraw the arrow
        self.robot_angle_arrow.setStyle(headLen=self.robot_radius)
        self.update_arrow()

    def draw_target(self):
        self.target_pos_plot = self.plot_widget.plot(pen=None,
                                                     symbol='+', symbolPen=None, symbolSize=100, pxMode=False,
                                                     symbolBrush=(200, 0, 0, 220),
                                                     name='Target position')
        self.viewbox.addItem(self.target_pos_plot)

    def add_robot_pos(self, pos):
        self.robot_pos.append(pos)
        x = [item['x'] for item in self.robot_pos]
        y = [item['y'] for item in self.robot_pos]
        a = [item['a'] for item in self.robot_pos]

        last_x = x[-1]
        last_y = y[-1]

        # Plot the current location (big plot) with the latest entry
        self.robot_pos_plot.setData(x=[last_x], y=[last_y])

        # Plot the history location
        self.robot_pos_hist_plot.setData(x=x, y=y)

        # Redraw the orientation arrow
        self.update_arrow()

        # Update label
        self.robot_coord_label.setText(
            "<span style='color: red;font-weight:bold'>Robot:</span><br />"
            "X = %+05d<br />"
            "Y = %+05d<br />"
            "A = %+03d" % (
                pos['x'], pos['y'], pos['a']))

    def update_arrow(self):
        if len(self.robot_pos) > 0:
            last_pos = self.robot_pos[-1]
            self.robot_angle_arrow.setPos(QPoint(last_pos['x'] + self.robot_radius * np.cos(np.radians(last_pos['a'])),
                                                 last_pos['y'] + self.robot_radius * np.sin(np.radians(last_pos['a']))))
            self.robot_angle_arrow.setRotation(last_pos['a'])  # Bug in the setStyle of ArrowItem() class

    def update_target_pos(self, x, y):
        self.target_pos_plot.setData(x=[x], y=[y])

    def mouse_moved(self, evt):

        # Retrieve mouse coordinates
        mouse_point = self.viewbox.mapSceneToView(evt[0])
        x = mouse_point.x()
        y = mouse_point.y()

        # Update Mouse Coordinate label
        self.mouse_coord_label.setText(
            "<span style='color: red;font-weight:bold'>Mouse:</span><br />"
            "X = %+05d<br />"
            "Y = %+05d" % (x, y))

        # Update crosshair drawing if there are within image bounds
        # Even if not visible, this needs to be updated because the crosshair is used for X;Y position of the mouse
        if (x >= 0) and (x <= self.playground_size_mm[0]) and (y >= 0) and (y <= self.playground_size_mm[1]):
            self.cross_v_line.setPos(x)
            self.cross_h_line.setPos(y)

        # Display it only if requested
        self.cross_v_line.setVisible(self.crosshair_visible)
        self.cross_h_line.setVisible(self.crosshair_visible)


    def mouse_clicked(self, evt):

        # Not very elegant but easy to use
        x = int(self.cross_v_line.getPos()[0])
        y = int(self.cross_h_line.getPos()[1])

        # Left click
        if evt[0].button() == Qt.LeftButton:
            if (x >= 0) and (x <= self.playground_size_mm[0]) and (y >= 0) and (y <= self.playground_size_mm[1]):
                self.left_click_playground.emit(x, y)
