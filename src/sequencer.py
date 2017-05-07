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

    # -------------------------------------------------------------------------
    # Handlers
    # -------------------------------------------------------------------------

    def clear_tasks_table(self):
        self.tableWidget_tasks.setRowCount(0)


    # -------------------------------------------------------------------------
    # Slots & Binds
    # -------------------------------------------------------------------------

