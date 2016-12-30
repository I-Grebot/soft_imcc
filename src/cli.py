#!/usr/bin/python3
# -*- coding: utf-8 -*-

import serial
import threading
import queue
import sys
import time

from PyQt5.QtCore import *

class Cli(QObject):

    # Default settings of the CLI
    BAUDRATE = 115200
    BYTESIZE = serial.EIGHTBITS
    PARITY = serial.PARITY_EVEN
    STOPBITS = serial.STOPBITS_ONE

    # Signals factory
    data_available = pyqtSignal(name='dataAvailable')


    def __init__(self):

        super(Cli, self).__init__()

        # Create the serial object that is used for the CLI
        self.serial = serial.Serial(baudrate=self.BAUDRATE,
                                    bytesize=self.BYTESIZE,
                                    parity=self.PARITY,
                                    stopbits=self.STOPBITS)

        # Initialize an RX queue that'll store everything we receive
        self.rx_queue = queue.Queue()

        # Initialize a thread that'll handle the reception
        self.state = threading.Condition()  # Notify threading changes safely
        self.alive = threading.Event()  # helps with locking
        self.rx_thread = threading.Thread(target=self._run)
        self.rx_thread.start()

    def __del__(self):
        self.close()
        self.rx_thread.join(0)  # Close the thread

    def open(self, port):
        self.serial.setPort(port)
        try:
            self.serial.open()
        except Exception as msg:
            print('[CLI] Error: %s ' % msg)
            return False

        with self.state:
            self.alive.set()
            self.state.notify()

        print('[CLI] Opened CLI on port %s' % port)

        time.sleep(1)
        self.send('sys reset\n')
        time.sleep(1)

        #self.probe_start()
        return True
    # end open

    def close(self):
        with self.state:
            self.alive.clear()
            self.state.notify()

            #self.probe_stop()
        self.serial.close()  # Close the serial port

        print('[CLI] Closed CLI')
    # end close

    @pyqtSlot(str)
    def send(self, str):
        if self.serial.isOpen():
            try:
                self.serial.write(str.encode())
            except Exception as msg:
                print('[CLI] Error: %s' % msg)

    def _run(self):
        while True:
            with self.state:
                if not self.alive.is_set():
                    self.state.wait()  # Port was closed, wait
            self.read()
    # end _run

    def read(self):
        data = bytes("", "ascii")
        try:
            data = self.serial.readline()
        except:
            pass
        else:
            self.process_read(data)
        return data  # if called directly
    # end read

    def process_read(self, data):
        data_str = data.decode('utf-8','ignore')
        clean_str = data_str.strip("/\r")
        #print(clean_str, end="")

        if self.rx_queue.full():
            self.rx_queue.get(0)  # remove the first item to free up space

        self.rx_queue.put(clean_str)
        self.data_available.emit()

    # end process_read

    def get_item(self):
        return self.rx_queue.get()


    def probe_start(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.probe_send_test)

        #self.send('set sys.shell.echo 0\n')

        self.timer.start(1000)

    def probe_stop(self):
        self.timer.stop()
        #self.send('set sys.shell.echo 1\n')

    def probe_send_test(self):
        #self.send('get robot.cs.pos\n')
        self.send('sys tasks\n')
