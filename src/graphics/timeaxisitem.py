#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import pyqtgraph as pg

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
