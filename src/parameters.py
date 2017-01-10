#!/usr/bin/python3
# -*- coding: utf-8 -*-

# PyQtGraph
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType


class Parameters(ParameterTree):

    params = [
        {'name': 'Probing', 'type': 'group', 'children': [
            {'name': 'Frequency', 'type': 'float', 'value': 10, 'dec': True, 'step': 1, 'siPrefix': True,
             'limits': (1,20), 'suffix': 'Hz'}
         ]}
    ]

    def __init__(self, *args, **kwargs):
        super(Parameters, self).__init__(*args, **kwargs)
        self.p = Parameter.create(name='params', type='group', children=self.params)
        self.setParameters(self.p, showTop=False)
