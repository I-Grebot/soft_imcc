#!/usr/bin/python3
# -*- coding: utf-8 -*-

# PyQtGraph
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType

# test subclassing parameters
# This parameter automatically generates two child parameters which are always reciprocals of each other
class ComplexParameter(pTypes.GroupParameter):
    def __init__(self, **opts):
        opts['type'] = 'bool'
        opts['value'] = True
        pTypes.GroupParameter.__init__(self, **opts)

        self.addChild({'name': 'A = 1/B', 'type': 'float', 'value': 7, 'suffix': 'Hz', 'siPrefix': True})
        self.addChild({'name': 'B = 1/A', 'type': 'float', 'value': 1 / 7., 'suffix': 's', 'siPrefix': True})
        self.a = self.param('A = 1/B')
        self.b = self.param('B = 1/A')
        self.a.sigValueChanged.connect(self.aChanged)
        self.b.sigValueChanged.connect(self.bChanged)

    def aChanged(self):
        self.b.setValue(1.0 / self.a.value(), blockSignal=self.bChanged)

    def bChanged(self):
        self.a.setValue(1.0 / self.b.value(), blockSignal=self.aChanged)


# test add/remove
# this group includes a menu allowing the user to add new parameters into its child list
class ScalableGroup(pTypes.GroupParameter):
    def __init__(self, **opts):
        opts['type'] = 'group'
        opts['addText'] = "Add"
        opts['addList'] = ['str', 'float', 'int']
        pTypes.GroupParameter.__init__(self, **opts)

    def addNew(self, typ):
        val = {
            'str': '',
            'float': 0.0,
            'int': 0
        }[typ]
        self.addChild(
            dict(name="ScalableParam %d" % (len(self.childs) + 1), type=typ, value=val, removable=True, renamable=True))


class Parameters(ParameterTree):

    params = [
        {'name': 'Basic parameter data types', 'type': 'group', 'children': [
            {'name': 'Integer', 'type': 'int', 'value': 10},
            {'name': 'Float', 'type': 'float', 'value': 10.5, 'step': 0.1},
            {'name': 'String', 'type': 'str', 'value': "hi"},
            {'name': 'List', 'type': 'list', 'values': [1, 2, 3], 'value': 2},
            {'name': 'Named List', 'type': 'list', 'values': {"one": 1, "two": "twosies", "three": [3, 3, 3]},
             'value': 2},
            {'name': 'Boolean', 'type': 'bool', 'value': True, 'tip': "This is a checkbox"},
            {'name': 'Color', 'type': 'color', 'value': "FF0", 'tip': "This is a color button"},
            {'name': 'Gradient', 'type': 'colormap'},
            {'name': 'Subgroup', 'type': 'group', 'children': [
                {'name': 'Sub-param 1', 'type': 'int', 'value': 10},
                {'name': 'Sub-param 2', 'type': 'float', 'value': 1.2e6},
            ]},
            {'name': 'Text Parameter', 'type': 'text', 'value': 'Some text...'},
            {'name': 'Action Parameter', 'type': 'action'},
        ]},
        {'name': 'Numerical Parameter Options', 'type': 'group', 'children': [
            {'name': 'Units + SI prefix', 'type': 'float', 'value': 1.2e-6, 'step': 1e-6, 'siPrefix': True,
             'suffix': 'V'},
            {'name': 'Limits (min=7;max=15)', 'type': 'int', 'value': 11, 'limits': (7, 15), 'default': -6},
            {'name': 'DEC stepping', 'type': 'float', 'value': 1.2e6, 'dec': True, 'step': 1, 'siPrefix': True,
             'suffix': 'Hz'},

        ]},
        {'name': 'Save/Restore functionality', 'type': 'group', 'children': [
            {'name': 'Save State', 'type': 'action'},
            {'name': 'Restore State', 'type': 'action', 'children': [
                {'name': 'Add missing items', 'type': 'bool', 'value': True},
                {'name': 'Remove extra items', 'type': 'bool', 'value': True},
            ]},
        ]},
        {'name': 'Extra Parameter Options', 'type': 'group', 'children': [
            {'name': 'Read-only', 'type': 'float', 'value': 1.2e6, 'siPrefix': True, 'suffix': 'Hz', 'readonly': True},
            {'name': 'Renamable', 'type': 'float', 'value': 1.2e6, 'siPrefix': True, 'suffix': 'Hz', 'renamable': True},
            {'name': 'Removable', 'type': 'float', 'value': 1.2e6, 'siPrefix': True, 'suffix': 'Hz', 'removable': True},
        ]},
        ComplexParameter(name='Custom parameter group (reciprocal values)'),
        ScalableGroup(name="Expandable Parameter Group", children=[
            {'name': 'ScalableParam 1', 'type': 'str', 'value': "default param 1"},
            {'name': 'ScalableParam 2', 'type': 'str', 'value': "default param 2"},
        ]),
    ]

    def __init__(self, *args, **kwargs):
        super(Parameters, self).__init__(*args, **kwargs)
        self.p = Parameter.create(name='params', type='group', children=self.params)
        self.setParameters(self.p, showTop=False)
