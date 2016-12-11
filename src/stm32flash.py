#!/usr/bin/python3
# -*- coding: utf-8 -*-

from ui.stm32flash import Ui_stm32flash


class Stm32Flash(Ui_stm32flash):

    # -------------------------------------------------------------------------
    # Constructor
    # -------------------------------------------------------------------------
    def __init__(self, dockwidget):
        self.setupUi(dockwidget)
        self.connect()

    # -------------------------------------------------------------------------
    # Bind & Slots connection
    # -------------------------------------------------------------------------
    def connect(self):
        self.pushButton_write.clicked.connect(self.action_write)
        self.pushButton_erase.clicked.connect(self.action_erase)
        self.pushButton_read.clicked.connect(self.action_read)

    # -------------------------------------------------------------------------
    # Actions
    # -------------------------------------------------------------------------

    def action_write(self):
        print('Write!')

    def action_erase(self):
        print('Erase!')

    def action_read(self):
        print('Read!')
