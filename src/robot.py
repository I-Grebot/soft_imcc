#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Robot:

    # -------------------------------------------------------------------------
    # Attributes
    # -------------------------------------------------------------------------

    pos = dict()
    av_pos = dict()
    av_mask = dict()
    av_det = dict()

    # -------------------------------------------------------------------------
    # Constructor
    # -------------------------------------------------------------------------

    def __init__(self):

        self.pos = {'x': 0, 'y': 0, 'a': 0}

        # TODO: remove explicit naming. Handle complete generic number of sensors
        # Positions around the robot
        self.av_pos = {
            'fl': -45,
            'fc': 0,
            'fr': 45,
            'bl': -135,
            'bc': 180,
            'br': 135,
        }

        self.av_mask = {
            'fl': 0,
            'fc': 0,
            'fr': 0,
            'bl': 0,
            'bc': 0,
            'br': 0,
        }

        self.av_det = {
            'fl': 0,
            'fc': 0,
            'fr': 0,
            'bl': 0,
            'bc': 0,
            'br': 0,
        }


    def set_x(self, x):
        self.pos['x'] = x

    def set_y(self, y):
        self.pos['y'] = y

    def set_a(self, a):
        self.pos['a'] = a

    def set_avoidance_mask(self, val):
        self.av_mask['fl'] = (val >> 0) & 1
        self.av_mask['fc'] = (val >> 1) & 1
        self.av_mask['fr'] = (val >> 2) & 1
        self.av_mask['bl'] = (val >> 3) & 1
        self.av_mask['bc'] = (val >> 4) & 1
        self.av_mask['br'] = (val >> 5) & 1

    def set_avoidance_detection(self, val):
        self.av_det['fl'] = (val >> 0) & 1
        self.av_det['fc'] = (val >> 1) & 1
        self.av_det['fr'] = (val >> 2) & 1
        self.av_det['bl'] = (val >> 3) & 1
        self.av_det['bc'] = (val >> 4) & 1
        self.av_det['br'] = (val >> 5) & 1

    def get_pos(self):
        return self.pos

    def get_av_positions(self):
        positions = {
            0: self.av_pos['fl'],
            1: self.av_pos['fc'],
            2: self.av_pos['fr'],
            3: self.av_pos['bl'],
            4: self.av_pos['bc'],
            5: self.av_pos['br'],
        }
        return positions


    def get_av_states(self):
        states = {
            0: self.compute_state(self.av_mask['fl'], self.av_det['fl']),
            1: self.compute_state(self.av_mask['fc'], self.av_det['fc']),
            2: self.compute_state(self.av_mask['fr'], self.av_det['fr']),
            3: self.compute_state(self.av_mask['bl'], self.av_det['bl']),
            4: self.compute_state(self.av_mask['bc'], self.av_det['bc']),
            5: self.compute_state(self.av_mask['br'], self.av_det['br']),
        }

        return states

    def compute_state(self, mask, det):
        if mask == 0:
            return 'inactive'
        elif det == 1:
            return 'detection'
        else:
            return 'active'

