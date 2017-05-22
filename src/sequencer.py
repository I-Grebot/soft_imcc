#!/usr/bin/python3
# -*- coding: utf-8 -*-

from ui.sequencer import Ui_Sequencer

from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView

class Sequencer(QObject, Ui_Sequencer):

    # -------------------------------------------------------------------------
    # Constants
    # -------------------------------------------------------------------------

    COLUMN_TASK_NAME         = 0
    COLUMN_TASK_STATE        = 1
    COLUMN_TASK_NB_DEP       = 2
    COLUMN_TASK_VALUE        = 3
    COLUMN_TASK_PRIORITY     = 4
    COLUMN_TASK_TRIALS       = 5

    # -------------------------------------------------------------------------
    # Attributes
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # Constructor
    # -------------------------------------------------------------------------
    def __init__(self, dockwidget, cli):
        super(Sequencer, self).__init__()
        self.cli = cli
        self.setupUi(dockwidget)
        self.clear_tasks_table()

        # Ensure that the "name" column of the task table is stretched
        horiz_header = self.tableWidget_tasks.horizontalHeader()
        horiz_header.setResizeMode(self.COLUMN_TASK_NAME, QHeaderView.Stretch)

        # Connections

        # Default values
        self.state = "UNKNOWN"
        self.color = "UNKNOWN"
        self.task = "UNKNOWN"
        self.timer = 0
        self.points = 0

        self.update_match()

    # -------------------------------------------------------------------------
    # Handlers
    # -------------------------------------------------------------------------

    def clear_tasks_table(self):
        self.tableWidget_tasks.setRowCount(0)


    def is_task_present(self, task_id):
        # TODO...
        return False

    def update_task(self, task):

        # Check to see if task is already present (id lookup)
        if ~self.is_task_present(task['id']):

            # Add at the bottom of the array
            row = self.tableWidget_tasks.rowCount()
            self.tableWidget_tasks.insertRow(row)

            # Label the Vertical header with the ID
            self.tableWidget_tasks.setVerticalHeaderItem(row, QTableWidgetItem(task['id']))

            task_name = QTableWidgetItem(task['name'])
            task_name.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tableWidget_tasks.setItem(row, self.COLUMN_TASK_NAME, task_name)

            task_state = QTableWidgetItem(task['state'])

            # Default colors
            fg_color = QColor(0, 0, 0)
            bg_color = QColor(255, 255, 255)

            # Differentiate few cases
            if task['state'] == "SUCCESS":
                bg_color = QColor(0, 200, 0)
            elif task['state'] == "SUSPENDED":
                fg_color = QColor(200, 200, 0)
            elif task['state'] == "RUNNING":
                fg_color = QColor(0, 200, 0)
            elif task['state'] == "FAILED":
                bg_color = QColor(200, 0, 0)

            task_state.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            task_state.setForeground(fg_color)
            task_state.setBackground(bg_color)

            self.tableWidget_tasks.setItem(row, self.COLUMN_TASK_STATE, task_state)

            task_nb_dep = QTableWidgetItem(task['nb_dep'])
            task_nb_dep.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tableWidget_tasks.setItem(row, self.COLUMN_TASK_NB_DEP, task_nb_dep)

            task_value = QTableWidgetItem(task['value'])
            task_value.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tableWidget_tasks.setItem(row, self.COLUMN_TASK_VALUE, task_value)

            task_priority = QTableWidgetItem(task['priority'])
            task_priority.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tableWidget_tasks.setItem(row, self.COLUMN_TASK_PRIORITY, task_priority)

            task_trials = QTableWidgetItem(task['trials'])

            # Highlight when more than 1 trial
            if int(task['trials']) > 1:
                task_trials.setForeground(QColor(255, 0, 0))

            task_trials.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tableWidget_tasks.setItem(row, self.COLUMN_TASK_TRIALS, task_trials)

            # Always resize to content at the end
            self.tableWidget_tasks.resizeColumnsToContents()
            self.tableWidget_tasks.resizeRowsToContents()

    def set_match(self, match):
        self.state = match['state']
        self.color = match['color']
        self.task = match['task']
        self.timer = int(match['timer'])
        self.points = int(match['points'])

        self.update_match()

    def update_match(self):

        self.lineEdit_match_state.setText(self.state)

        if self.state == "READY":
            self.lineEdit_match_state.setStyleSheet(
                """QLineEdit { background-color: grey; color: black }""")

        elif self.state == "INIT" or self.state == "SELF-TEST":
            self.lineEdit_match_state.setStyleSheet(
                """QLineEdit { background-color: blue; color: white }""")

        elif self.state == "WAIT-START":
            self.lineEdit_match_state.setStyleSheet(
                """QLineEdit { background-color: orange; color: white }""")

        elif self.state == "RUN":
            self.lineEdit_match_state.setStyleSheet(
                """QLineEdit { background-color: green; color: white }""")

        elif self.state == "STOPPED":
            self.lineEdit_match_state.setStyleSheet(
                """QLineEdit { background-color: red; color: white }""")

        else:
            self.lineEdit_match_state.setStyleSheet(
                """QLineEdit { background-color: white; color: black }""")

        self.lineEdit_match_color.setText(self.color)

        if self.color != "UNKNOWN":
            self.lineEdit_match_color.setStyleSheet(
                """QLineEdit { background-color: %s; color: black }""" % self.color)

        self.lineEdit_match_task.setText(self.task)

        self.lineEdit_match_timer.setText("%u" % self.timer)

        if self.timer >= 90:
            self.lineEdit_match_timer.setStyleSheet(
                """QLineEdit { color: red }""")

        elif self.timer > 80:
            self.lineEdit_match_timer.setStyleSheet(
                """QLineEdit { color: orange }""")

        elif self.timer > 45:
            self.lineEdit_match_timer.setStyleSheet(
                """QLineEdit { color: yellow }""")

        self.lineEdit_match_points.setText("%u" % self.points)


    # -------------------------------------------------------------------------
    # Slots & Binds
    # -------------------------------------------------------------------------

