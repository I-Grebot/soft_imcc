#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Robot:

    # -------------------------------------------------------------------------
    # Attributes
    # -------------------------------------------------------------------------

    pos = dict()

    # -------------------------------------------------------------------------
    # Constructor
    # -------------------------------------------------------------------------

    def __init__(self):

        self.pos = {'x': 0, 'y': 0, 'a': 0}


    def set_x(self, x):
        self.pos['x'] = x

    def set_y(self, y):
        self.pos['y'] = y

    def set_a(self, a):
        self.pos['a'] = a

    def get_pos(self):
        return self.pos
