#!/usr/bin/python3
# -*- coding: utf-8 -*-

from ui.variables import Ui_Variables

from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView

class Variables(QObject, Ui_Variables):

    # -------------------------------------------------------------------------
    # Constants
    # -------------------------------------------------------------------------
    COLUMN_NAME     = 0
    COLUMN_TYPE     = 1
    COLUMN_ACCESS   = 2
    COLUMN_VALUE    = 3
    COLUMN_UNIT     = 4
    COLUMN_PROBE    = 5

    # -------------------------------------------------------------------------
    # Attributes
    # -------------------------------------------------------------------------
    # Signals factory
    probe_list_changed = pyqtSignal(name='probeListChanged')

    # -------------------------------------------------------------------------
    # Constructor
    # -------------------------------------------------------------------------
    def __init__(self, dockwidget, cli):
        super(Variables, self).__init__()
        self.cli = cli
        self.setupUi(dockwidget)
        self.clear_table()

        # Ensure that the "name" column is stretched
        horiz_header = self.tableWidget_variables.horizontalHeader()
        horiz_header.setResizeMode(self.COLUMN_NAME, QHeaderView.Stretch)

        # Connections
        self.tableWidget_variables.itemClicked.connect(self.table_item_clicked)
        self.pushButton_refresh.clicked.connect(self.refresh_table)

    # -------------------------------------------------------------------------
    # Handlers
    # -------------------------------------------------------------------------

    def clear_table(self):
        self.tableWidget_variables.setRowCount(0)

    def refresh_table(self):

        # Start to clear previous rows
        self.clear_table()

        # Request new values from the CLI
        self.cli.send('var\n')

    def add_item(self, item):

        # Add at the bottom of the array
        row = self.tableWidget_variables.rowCount()
        self.tableWidget_variables.insertRow(row)

        # Label the Vertical header with the ID
        self.tableWidget_variables.setVerticalHeaderItem(row, QTableWidgetItem(item['id']))

        item_name = QTableWidgetItem(item['name'])
        item_name.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.tableWidget_variables.setItem(row, self.COLUMN_NAME, item_name)

        item_type = QTableWidgetItem(item['type'])
        item_type.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.tableWidget_variables.setItem(row, self.COLUMN_TYPE, item_type)

        item_access = QTableWidgetItem(item['access'])
        item_access.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.tableWidget_variables.setItem(row, self.COLUMN_ACCESS, item_access)

        item_value = QTableWidgetItem(item['value'])
        item_value.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item_value.setForeground(QColor(0, 0, 200))
        self.tableWidget_variables.setItem(row, self.COLUMN_VALUE, item_value)

        item_unit = QTableWidgetItem(item['unit'])
        item_unit.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.tableWidget_variables.setItem(row, self.COLUMN_UNIT, item_unit)

        item_probe = QTableWidgetItem()
        item_probe.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
        item_probe.setCheckState(Qt.Unchecked)
        self.tableWidget_variables.setItem(row, self.COLUMN_PROBE, item_probe)

    def get_probe_list(self):

        probe_list = list()

        for i in range(self.tableWidget_variables.rowCount()):
            if self.tableWidget_variables.item(i, self.COLUMN_PROBE).checkState() == Qt.Checked:
                name = self.tableWidget_variables.item(i, self.COLUMN_NAME).text()
                probe_id = int(self.tableWidget_variables.verticalHeaderItem(i).text())
                probe_list.append({'id': probe_id, 'name': name})

        return probe_list

    # -------------------------------------------------------------------------
    # Slots & Binds
    # -------------------------------------------------------------------------

    def table_item_clicked(self, item):

        if item.column() == self.COLUMN_PROBE:
            self.probe_list_changed.emit()




