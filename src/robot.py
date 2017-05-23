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

        self.av_mask_static = {
            'fl': 0,
            'fc': 0,
            'fr': 0,
            'bl': 0,
            'bc': 0,
            'br': 0,
        }

        self.av_mask_dynamic = {
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

        self.av_det_eff = {
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

    def set_avoidance_mask_static(self, val):
        self.av_mask_static['fl'] = (val >> 0) & 1
        self.av_mask_static['fc'] = (val >> 1) & 1
        self.av_mask_static['fr'] = (val >> 2) & 1
        self.av_mask_static['bl'] = (val >> 3) & 1
        self.av_mask_static['bc'] = (val >> 4) & 1
        self.av_mask_static['br'] = (val >> 5) & 1

    def set_avoidance_mask_dynamic(self, val):
        self.av_mask_dynamic['fl'] = (val >> 0) & 1
        self.av_mask_dynamic['fc'] = (val >> 1) & 1
        self.av_mask_dynamic['fr'] = (val >> 2) & 1
        self.av_mask_dynamic['bl'] = (val >> 3) & 1
        self.av_mask_dynamic['bc'] = (val >> 4) & 1
        self.av_mask_dynamic['br'] = (val >> 5) & 1

    def set_avoidance_detection(self, val):
        self.av_det['fl'] = (val >> 0) & 1
        self.av_det['fc'] = (val >> 1) & 1
        self.av_det['fr'] = (val >> 2) & 1
        self.av_det['bl'] = (val >> 3) & 1
        self.av_det['bc'] = (val >> 4) & 1
        self.av_det['br'] = (val >> 5) & 1

    def set_avoidance_effective_detection(self, val):
        self.av_det_eff['fl'] = (val >> 0) & 1
        self.av_det_eff['fc'] = (val >> 1) & 1
        self.av_det_eff['fr'] = (val >> 2) & 1
        self.av_det_eff['bl'] = (val >> 3) & 1
        self.av_det_eff['bc'] = (val >> 4) & 1
        self.av_det_eff['br'] = (val >> 5) & 1

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
            0: self.compute_state('fl'),
            1: self.compute_state('fc'),
            2: self.compute_state('fr'),
            3: self.compute_state('bl'),
            4: self.compute_state('bc'),
            5: self.compute_state('br'),
        }
        return states

    def compute_state(self, sensor):
        if self.av_mask_static[sensor] == 0:
            return 'inactive'
        elif self.av_mask_dynamic[sensor] == 0:
            return 'ignore'
        elif self.av_det_eff[sensor] == 1:
            return 'detection'
        else:
            return 'active'

