#!/usr/bin/python3
# -*- coding: utf-8 -*-

from ui.digital_servos import Ui_DigitalServos

from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView

class DigitalServos(QObject, Ui_DigitalServos):

    # -------------------------------------------------------------------------
    # Constants
    # -------------------------------------------------------------------------
    COLUMN_SERVO_ID     = 0
    COLUMN_SERVO_MODEL  = 1
    COLUMN_SERVO_STATUS = 2

    COLUMN_REGISTER_AREA     = 0
    COLUMN_REGISTER_ACCESS   = 1
    COLUMN_REGISTER_ADDRESS  = 2
    COLUMN_REGISTER_SIZE     = 3
    COLUMN_REGISTER_NAME     = 4
    COLUMN_REGISTER_VALUE    = 5

    # Status value when no error occured
    STATUS_PASS = 0

    # -------------------------------------------------------------------------
    # Attributes
    # -------------------------------------------------------------------------

    # Signals factory
    register_changed = pyqtSignal([int, int, str, str, str], name='registerChanged')

    # -------------------------------------------------------------------------
    # Constructor
    # -------------------------------------------------------------------------
    def __init__(self, dockwidget, cli):
        super(DigitalServos, self).__init__()
        self.cli = cli
        self.setupUi(dockwidget)
        self.clear_servos_table()
        self.clear_registers_table()
        self.refresh_interfaces_list(0)  # Cleanup

        # Ensure that the "model" column of the servo table is stretched
        horiz_header = self.tableWidget_servos.horizontalHeader()
        horiz_header.setResizeMode(self.COLUMN_SERVO_MODEL, QHeaderView.Stretch)

        # Ensure that the "name" column of the registers table is stretched
        horiz_header = self.tableWidget_registers.horizontalHeader()
        horiz_header.setResizeMode(self.COLUMN_REGISTER_NAME, QHeaderView.Stretch)

        # Connections
        self.pushButton_scan.clicked.connect(self.scan)
        self.pushButton_ping.clicked.connect(self.ping)
        self.pushButton_reset.clicked.connect(self.reset)
        self.pushButton_dump.clicked.connect(self.dump)

        self.tableWidget_registers.itemChanged.connect(self.table_registers_item_changed)

        #self.tableWidget_variables.itemClicked.connect(self.table_item_clicked)
        #self.pushButton_refresh.clicked.connect(self.refresh_table)

    # -------------------------------------------------------------------------
    # Handlers
    # -------------------------------------------------------------------------

    def clear_servos_table(self):
        self.tableWidget_servos.setRowCount(0)

    def clear_registers_table(self):
        self.tableWidget_registers.setRowCount(0)

    def refresh_interfaces_list(self, nb_interfaces):
        self.comboBox_interfaces.clear()

        for itf in range(1, nb_interfaces+1):
            self.comboBox_interfaces.addItem("%d" % itf, userData=itf)

    def get_current_interface(self):
        return int(self.comboBox_interfaces.currentData())

    def get_current_servo_id(self):
        return 20

    def scan(self):
        self.clear_servos_table()
        self.cli.send('dsv scan %u\n' % self.get_current_interface())

    def ping(self):
        self.cli.send('dsv ping %u %u\n' % (self.get_current_interface(), self.get_current_servo_id()))

    def reset(self):
        print('RESET')

    def dump(self):
        self.clear_registers_table()
        self.cli.send('dsv dump %u %u\n' % (self.get_current_interface(), self.get_current_servo_id()))

    def add_servo(self, item):

        # Add at the bottom of the array
        row = self.tableWidget_servos.rowCount()
        self.tableWidget_servos.insertRow(row)

        item_id = QTableWidgetItem(item['id'])
        item_id.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.tableWidget_servos.setItem(row, self.COLUMN_SERVO_ID, item_id)

        item_model_name = QTableWidgetItem(item['model_name'])
        item_model_name.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.tableWidget_servos.setItem(row, self.COLUMN_SERVO_MODEL, item_model_name)

        item_status = QTableWidgetItem(item['status'])
        self.tableWidget_servos.setItem(row, self.COLUMN_SERVO_STATUS, item_status)
        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable

        if int(item['status']) == self.STATUS_PASS:
            item_color = QColor(0, 200, 0)
        else:
            item_color = QColor(200, 0, 0)

        item_status.setFlags(flags)
        item_status.setForeground(item_color)

    def add_register(self, item):

        # Add at the bottom of the array
        row = self.tableWidget_registers.rowCount()
        self.tableWidget_registers.insertRow(row)

        item_area = QTableWidgetItem(item['area'])
        item_area.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.tableWidget_registers.setItem(row, self.COLUMN_REGISTER_AREA, item_area)

        if item['area'] == "RAM":
            item_color = QColor(0, 0, 200)
        else:  # EEPROM
            item_color = QColor(200, 0, 0)

        item_area.setForeground(item_color)

        item_access = QTableWidgetItem(item['access'])
        item_access.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.tableWidget_registers.setItem(row, self.COLUMN_REGISTER_ACCESS, item_access)

        item_address = QTableWidgetItem(item['address'])
        item_address.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.tableWidget_registers.setItem(row, self.COLUMN_REGISTER_ADDRESS, item_address)

        item_size = QTableWidgetItem(item['size'])
        item_size.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.tableWidget_registers.setItem(row, self.COLUMN_REGISTER_SIZE, item_size)

        item_name = QTableWidgetItem(item['name'])
        item_name.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.tableWidget_registers.setItem(row, self.COLUMN_REGISTER_NAME, item_name)

        item_value = QTableWidgetItem(item['value'])
        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable

        if item['access'] != "R":
            flags |= Qt.ItemIsEditable
            item_color = QColor(200, 0, 0)
        else:
            item_color = QColor(0, 0, 200)

        item_value.setFlags(flags)
        item_value.setForeground(item_color)

        # Prevent signaling when modifying the value
        self.tableWidget_registers.blockSignals(True)
        self.tableWidget_registers.setItem(row, self.COLUMN_REGISTER_VALUE, item_value)
        self.tableWidget_registers.blockSignals(False)

    # -------------------------------------------------------------------------
    # Slots & Binds
    # -------------------------------------------------------------------------

    def table_registers_item_changed(self, item):

        if item.column() == self.COLUMN_REGISTER_VALUE:
            itf = self.get_current_interface()
            id = self.get_current_servo_id()
            address = self.tableWidget_registers.item(item.row(), self.COLUMN_REGISTER_ADDRESS).text()
            size = self.tableWidget_registers.item(item.row(), self.COLUMN_REGISTER_SIZE).text()
            value = self.tableWidget_registers.item(item.row(), self.COLUMN_REGISTER_VALUE).text()

            self.register_changed.emit(itf, id, address, size, value)
