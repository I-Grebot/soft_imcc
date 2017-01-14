#!/usr/bin/python3
# -*- coding: utf-8 -*-

# PyQtGraph
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType
import serial
from serial.tools import list_ports

class Parameters(ParameterTree):

    params = [
        {'name': 'Communication', 'type': 'group', 'children': [
            {'name': 'Port', 'type': 'list', 'values': {'COM12': 'COM12'},
             'value': "COM12"},
            {'name': 'Description', 'type': 'str', 'value': '', 'readonly': True},
            {'name': 'Refresh', 'type': 'action'},
        ]},
        {'name': 'Probing', 'type': 'group', 'children': [
            {'name': 'Frequency', 'type': 'float', 'value': 10, 'dec': True, 'step': 1, 'siPrefix': True,
             'limits': (1,20), 'suffix': 'Hz'}
         ]},
        {'name': 'Robot', 'type': 'group', 'children': [
            {'name': 'Update data', 'type': 'bool', 'value': True, 'tip': "Update table-view data when probing"},
            {'name': 'X Variable', 'type': 'str', 'value': 'robot.cs.pos.x'},
            {'name': 'Y Variable', 'type': 'str', 'value': 'robot.cs.pos.y'},
            {'name': 'A Variable', 'type': 'str', 'value': 'robot.cs.pos.a'}
        ]}
    ]

    def __init__(self, *args, **kwargs):
        super(Parameters, self).__init__(*args, **kwargs)
        self.p = Parameter.create(name='params', type='group', children=self.params)
        self.setParameters(self.p, showTop=False)

        self.default_port = 'COM12' # TODO: move me

        self.connect()

        self.refresh_serial_ports()

    def connect(self):
        self.p.param("Communication").param("Port").sigValueChanged.connect(self.update_port_description)
        self.p.param("Communication").param("Refresh").sigActivated.connect(self.refresh_serial_ports)

    # -------------------------------------------------------------------------
    # Getters
    # -------------------------------------------------------------------------

    def get_probing_frequency(self):
        return self.p.param("Probing").param("Frequency").value()

    def get_robot_update_data(self):
        return self.p.param("Robot").param("Update data").value()

    def get_robot_x_variable(self):
        return self.p.param("Robot").param("X Variable").value()

    def get_robot_y_variable(self):
        return self.p.param("Robot").param("Y Variable").value()

    def get_robot_a_variable(self):
        return self.p.param("Robot").param("A Variable").value()

    def get_serial_port(self):
        return self.p.param("Communication").param("Port").value()

    # -------------------------------------------------------------------------
    # Actions
    # -------------------------------------------------------------------------

    def refresh_serial_ports(self):
        com_ports = dict()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            com_ports[port.device] = port.device

        self.p.param("Communication").param("Port").setOpts(limits=com_ports)
        self.p.param("Communication").param("Port").setValue(self.default_port)
        self.update_port_description()

    def update_port_description(self):
        port_name = str(self.p.param("Communication").param("Port").value())
        port = list(serial.tools.list_ports.grep(port_name))[0]
        self.p.param("Communication").param("Description").setValue(port.description)
