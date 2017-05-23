#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Standard python libraries
import re

# Qt Libraries
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow, QDockWidget, QTabWidget, QVBoxLayout, QGridLayout, QLabel, QComboBox

# PyQtGraph
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import *
import pyqtgraph.console

# User-Interface
from ui.imcc import Ui_imcc
from ui import imcc_rc

# Other modules dependencies
from stm32flash import Stm32Flash
from console import Console
from parameters import Parameters
from variables import Variables
from digital_servos import DigitalServos
from sequencer import Sequencer
from cli import Cli
from robot import Robot
from graphics.graphics import Graphics

class IMCC(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_imcc()
        self.ui.setupUi(self)

        self.center_dock_layout = None

        self.parameters = Parameters(showHeader=False)
        self.cli = Cli()
        self.connect_first_time = False

        self.robot = Robot()

        self.create_widgets()

        self.connect()

        # Default states
        self.ui.actionViewBootload.trigger()
        self.ui.actionViewDigital_Servos.trigger()
        self.ui.actionViewSettings.trigger()
        self.ui.actionViewParameters.trigger()

        # Variables for probe
        self.probe_list = list()
        self.probe_started = False
        self.timer = QTimer()

    # Override close event for proper exit with frozen appli
    def closeEvent(self, *args, **kwargs):
        self.deleteLater()

    # -------------------------------------------------------------------------
    # UI
    # -------------------------------------------------------------------------

    def create_widgets(self):

        # Adding the STm32Flash widget
        self.stm32flash_dock = QDockWidget()
        self.stm32flash_dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.stm32flash = Stm32Flash(self.stm32flash_dock)

        # Adding the Console dock with serial and python console widgets
        self.console_dock = QDockWidget()
        self.console_dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea |
                                          QtCore.Qt.RightDockWidgetArea |
                                          QtCore.Qt.BottomDockWidgetArea |
                                          QtCore.Qt.TopDockWidgetArea)
        self.console = Console(self.console_dock, self.cli)
        self.python_console = pg.console.ConsoleWidget()
        self.console.tabWidget.addTab(self.python_console, "Python Console")

        # Add the Parameters dock
        self.parameters_dock = QDockWidget()
        self.parameters_dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.parameters_dock.setWidget(self.parameters)
        self.parameters_dock.setWindowTitle("Parameters")

        # Add the Variables dock
        self.variables_dock = QDockWidget()
        self.variables_dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea |
                                            QtCore.Qt.RightDockWidgetArea |
                                            QtCore.Qt.BottomDockWidgetArea |
                                            QtCore.Qt.TopDockWidgetArea)
        self.variables = Variables(self.variables_dock, self.cli)

        # Add the DigitalServos dock
        self.digital_servos_dock = QDockWidget()
        self.digital_servos_dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea |
                                                 QtCore.Qt.RightDockWidgetArea |
                                                 QtCore.Qt.BottomDockWidgetArea |
                                                 QtCore.Qt.TopDockWidgetArea)
        self.digital_servos = DigitalServos(self.digital_servos_dock, self.cli)

        # Add the Sequencer dock
        self.sequencer_dock = QDockWidget()
        self.sequencer_dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea |
                                            QtCore.Qt.RightDockWidgetArea |
                                            QtCore.Qt.BottomDockWidgetArea |
                                            QtCore.Qt.TopDockWidgetArea)
        self.sequencer = Sequencer(self.sequencer_dock, self.cli)

        # Create and place the main central widget
        self.graphics = Graphics()

        # Widgets Layout
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.parameters_dock)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.stm32flash_dock)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.sequencer_dock)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.variables_dock)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.digital_servos_dock)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.console_dock)
        self.setCentralWidget(self.graphics.win)

        # Add some specific stuff to the toolbar
        self.toolbar_goto_comboBox = QComboBox()
        self.toolbar_goto_comboBox.addItem('Goto Auto', 'goto_auto')
        self.toolbar_goto_comboBox.addItem('Goto Forward', 'goto_fwd')
        self.toolbar_goto_comboBox.addItem('Goto Backward', 'goto_bwd')
        self.toolbar_goto_comboBox.addItem('Turnto Front', 'turnto_front')
        self.toolbar_goto_comboBox.addItem('Turnto Behind', 'turnto_behind')

        self.ui.toolBar.insertWidget(self.ui.actionStopMotion, self.toolbar_goto_comboBox)

        # Some default loads
        self.update_playground_size()
        self.update_robot()

        # Add avoidance sensors
        for index, position in self.robot.get_av_positions().items():
            self.graphics.table.add_robot_sensor(position)

    def connect(self):

        # Connect ToolBar items
        self.ui.actionConnect.triggered[bool].connect(self.connect_com)
        self.ui.actionReset.triggered[bool].connect(self.reset)
        self.ui.actionProbe.triggered[bool].connect(self.probe_start_stop)

        self.ui.actionPower_ON.triggered[bool].connect(self.power_on)
        self.ui.actionPower_OFF.triggered[bool].connect(self.power_off)

        self.ui.actionViewConsole.triggered[bool].connect(self.console_dock.setVisible)
        self.console_dock.visibilityChanged[bool].connect(self.ui.actionViewConsole.setChecked)

        self.ui.actionViewBootload.triggered[bool].connect(self.stm32flash_dock.setVisible)
        self.stm32flash_dock.visibilityChanged[bool].connect(self.ui.actionViewBootload.setChecked)

        self.ui.actionViewParameters.triggered[bool].connect(self.parameters_dock.setVisible)
        self.parameters_dock.visibilityChanged[bool].connect(self.ui.actionViewParameters.setChecked)

        self.ui.actionViewVariables.triggered[bool].connect(self.variables_dock.setVisible)
        self.variables_dock.visibilityChanged[bool].connect(self.ui.actionViewVariables.setChecked)

        self.ui.actionViewDigital_Servos.triggered[bool].connect(self.digital_servos_dock.setVisible)
        self.digital_servos_dock.visibilityChanged[bool].connect(self.ui.actionViewDigital_Servos.setChecked)

        self.ui.actionViewSettings.triggered[bool].connect(self.graphics.widget_parameters.setVisible)
        self.ui.actionViewGraphs.triggered[bool].connect(self.graphics.action_view_graphs)

        self.ui.actionViewSequencer.triggered[bool].connect(self.sequencer_dock.setVisible)
        self.sequencer_dock.visibilityChanged[bool].connect(self.ui.actionViewSequencer.setChecked)

        self.parameters.robot_setting_changed.connect(self.update_robot)
        self.parameters.playground_size_changed.connect(self.update_playground_size)
        self.parameters.bootloader_path_changed.connect(self.update_bootload_path)

        self.ui.actionPan.triggered[bool].connect(self.pan_mode)
        self.ui.actionZoom.triggered[bool].connect(self.zoom_mode)
        self.ui.actionGoto.triggered[bool].connect(self.goto_mode)
        self.ui.actionStopMotion.triggered.connect(self.stop_motion)

        self.ui.actionColor.triggered[bool].connect(self.set_team_color)
        self.ui.actionInit.triggered[bool].connect(self.init_match)
        self.ui.actionStart.triggered[bool].connect(self.start_match)
        self.ui.actionPauseResume.triggered[bool].connect(self.pause_match)
        self.ui.actionStop.triggered[bool].connect(self.stop_match)

        self.cli.data_available.connect(self.cli_process)

        self.variables.probe_list_changed.connect(self.probe_list_update)
        self.variables.variable_changed[str, str].connect(self.variable_updated)

        self.digital_servos.register_changed[int, int, str, str, str].connect(self.digital_servo_register_updated)

        self.graphics.goto_clicked[int, int].connect(self.goto)

        self.sequencer.pushButton_get_polys.pressed.connect(self.get_polys)
        self.sequencer.pushButton_get_pois.pressed.connect(self.get_pois)
        self.sequencer.pushButton_get_tasks.pressed.connect(self.get_tasks)

    def set_status_bar_message(self, str):
        self.ui.statusbar.showMessage(str)

    def append_console(self, str):
        self.console.append_text(str)

    def update_playground_size(self):
        width = self.parameters.get_playground_width()
        height = self.parameters.get_playground_height()
        self.graphics.update_table_playground()
        self.graphics.table.set_playground_size(width, height)
        self.graphics.table.update_table_outline()

    def update_robot(self):
        robot_radius = self.parameters.get_robot_radius()
        self.graphics.table.set_robot_radius(robot_radius)

    def update_bootload_path(self):
        self.stm32flash.set_binary_path(self.parameters.get_bootloader_path())

    # -------------------------------------------------------------------------
    # Static methods
    # -------------------------------------------------------------------------

    @staticmethod
    def cleanup_spaces(in_str):
        ret_str = re.sub('\s+', ' ', in_str)
        ret_str = re.sub('\A\s', '', ret_str)
        ret_str = re.sub('\s\Z', '', ret_str)
        return ret_str

    # -------------------------------------------------------------------------
    # Main Actions management
    # -------------------------------------------------------------------------

    def reset(self):
        self.cli.flush()
        self.cli.send('sys reset\n')

    def pan_mode(self, val):
        if val:

            if self.ui.actionZoom.isChecked():
                self.ui.actionZoom.setChecked(False)

            if self.ui.actionGoto.isChecked():
                self.ui.actionGoto.setChecked(False)

            self.graphics.table.viewbox.setMouseMode(pg.ViewBox.PanMode)
            self.graphics.goto_mode = False

        self.graphics.pan_mode = val

    def zoom_mode(self, val):
        if val:

            if self.ui.actionPan.isChecked():
                self.ui.actionPan.setChecked(False)

            if self.ui.actionGoto.isChecked():
                self.ui.actionGoto.setChecked(False)

            self.graphics.table.viewbox.setMouseMode(pg.ViewBox.RectMode)

    def goto_mode(self, val):
        if val:
            if self.ui.actionPan.isChecked():
                self.ui.actionPan.setChecked(False)

            if self.ui.actionZoom.isChecked():
                self.ui.actionZoom.setChecked(False)

            self.graphics.pan_mode = False

        self.graphics.goto_mode = val

    def goto(self, x, y):
        type_str = self.toolbar_goto_comboBox.currentText()
        type_value = self.toolbar_goto_comboBox.currentData()
        print('%s %d %d' %(type_str, x, y))
        self.cli.send('mot %s %d %d\n' % (type_value, x, y))

    def stop_motion(self):
        print('Stopping motion')
        self.cli.send('mot stop\n')

    def power_on(self):
        print('Power all ON')
        self.cli.send('pow all on\n')

    def power_off(self):
        print('Power all OFF')
        self.cli.send('pow all off\n')

    def set_team_color(self, value):

        # Arbitrary: team 1 when not checked
        if value:
            team_color_str = self.parameters.get_color_team_2()
        else:
            team_color_str = self.parameters.get_color_team_1()

        icon_team = QtGui.QIcon()
        icon_team.addPixmap(QtGui.QPixmap(":/icons/fugue/icons/flag-" + team_color_str + ".png"),
                            QtGui.QIcon.Normal,
                            QtGui.QIcon.Off)

        self.ui.actionColor.setIcon(icon_team)

        print("Setting team color to %s (#%u)" % (team_color_str, value))
        self.cli.send("seq color %u\n" % value)

    def init_match(self):
        self.set_team_color(self.ui.actionColor.isChecked())
        print("Initializing match sequence")
        self.cli.send('seq init\n')

    def start_match(self):
        print("Starting the match!")
        self.cli.send('seq start\n')

    def pause_match(self, pause_not_resume):
        if pause_not_resume:
            print("Pausing the match...")
            self.cli.send('seq pause\n')
        else:
            print("Resuming the match")
            self.cli.send('seq resume\n')

    def stop_match(self):
        print("Stopping the match")
        self.cli.send('seq abort\n')

    def probe_list_update(self):
        self.probe_list = self.variables.get_probe_list()
        self.graphics.set_probe_list(self.probe_list)

    def probe_start_stop(self, state):

        if state:
            print('Starting probe...')
            self.cli.flush()
            self.timer.timeout.connect(self.probe_send)
            self.timer.start(1000 / self.parameters.get_probing_frequency())
            self.probe_started = True
        else:
            print('Stopping probe...')
            self.probe_started = False
            self.timer.stop()

    def probe_send(self):
        probe_str = 'prb '
        for i in range(len(self.probe_list)):
            probe_str += '%s ' % self.probe_list[i]['id']

        probe_str += '\n'
        self.cli.send(probe_str)

    def get_polys(self):
        self.graphics.table.clear_all_poly()
        self.cli.send('seq polys\n')

    def get_pois(self):
        self.graphics.table.clear_all_pois()
        self.cli.send('seq pois\n')

    def get_tasks(self):
        self.sequencer.clear_tasks_table()
        self.cli.send('seq tasks\n')

    @pyqtSlot(bool)
    def connect_com(self, checked):

        if checked:
            open_success = self.cli.open(self.parameters.get_serial_port())
            self.ui.actionConnect.setChecked(open_success)

            if open_success:

                # Auto-refresh only the first time
                if self.connect_first_time is False:
                    self.variables.refresh_table()

                self.variables.set_table_enabled(True)
                self.connect_first_time = True
                self.set_status_bar_message("Opened")

            else:
                self.set_status_bar_message("Error")

        else:
            self.cli.close()
            self.variables.set_table_enabled(False)
            self.set_status_bar_message("Closed")

    @pyqtSlot(str, str)
    def variable_updated(self, name, value):
        set_str = 'set ' + name + ' ' + value + '\n'
        self.cli.send(set_str)

    @pyqtSlot(int, int, str, str, str)
    def digital_servo_register_updated(self, itf, id, address, size, value):
        write_str = 'dsv write %d %d %s %s %s\n' %(itf, id, address, size, value)
        self.cli.send(write_str)

    @pyqtSlot()
    def cli_process(self):

        ret_str = self.cli.get_item()

        try:
            if ret_str.startswith('[GET]'):

                # Clean the string
                ret_str = ret_str[5:]
                ret_str = self.cleanup_spaces(ret_str)
                ret_str = re.sub('[^a-zA-Z0-9=_\-. ]+', '', ret_str)

                cmd_args = ret_str.split("=")

                if len(cmd_args) == 2:
                    var = cmd_args[0]
                    val = int(cmd_args[1])
                    self.graphics.set_probe_value(var, val)

            elif ret_str.startswith('[PRB]'):

                # Clean the string
                ret_str = ret_str[5:]
                ret_str = self.cleanup_spaces(ret_str)
                ret_str = re.sub('[^0-9\-. ]+', '', ret_str)

                values = ret_str.split(" ")

                if len(values) == len(self.probe_list):
                    for i in range(len(values)):
                        var = self.probe_list[i]['name']
                        val = int(values[i])  # others like float not yet supported

                        self.graphics.set_probe_value(var, val)

                        if var == self.parameters.get_robot_x_variable():
                            self.robot.set_x(val)
                        elif var == self.parameters.get_robot_y_variable():
                            self.robot.set_y(val)
                        elif var == self.parameters.get_robot_a_variable():
                            self.robot.set_a(val)
                        elif var == self.parameters.get_avoidance_mask_static_variable():
                            self.robot.set_avoidance_mask_static(val)
                        elif var == self.parameters.get_avoidance_mask_dynamic_variable():
                            self.robot.set_avoidance_mask_dynamic(val)
                        elif var == self.parameters.get_avoidance_det_variable():
                            self.robot.set_avoidance_detection(val)
                        elif var == self.parameters.get_avoidance_det_effective_variable():
                            self.robot.set_avoidance_effective_detection(val)

                if self.parameters.get_robot_update_data():
                    self.graphics.table.add_robot_pos(self.robot.get_pos())

                    for i, state in self.robot.get_av_states().items():
                        self.graphics.table.set_robot_sensor_state(i, state)

                    self.graphics.table.update_robot_sensors()

            elif ret_str.startswith('[VAR]'):

                # Display, it is not spammed on screen and would look odd with the header only
                # TODO: remove echo mode from target, put instead interactive mode which does not echo nor
                # display headers
                #self.console.append_text(ret_str)

                # Clean the string
                ret_str = ret_str[5:]
                ret_str = self.cleanup_spaces(ret_str)
                ret_str = re.sub('[^a-zA-Z0-9\-_./ ]+', '', ret_str)

                # Split items, add it to the variable list if it matches the format
                var_items = ret_str.split(' ')
                if len(var_items) == 6:
                    var = {'id': var_items[0],
                           'name': var_items[3],
                           'type': var_items[1],
                           'access': var_items[2],
                           'value': var_items[5],
                           'unit': var_items[4]}
                    self.variables.add_item(var)

                # Some triggers
                name = var_items[3]
                value = var_items[5]

                if name == self.parameters.get_digital_servos_nb_channels_variable():
                    self.digital_servos.refresh_interfaces_list(int(value))

            elif ret_str.startswith('[DSV] [SCAN]'):

                self.console.append_text(ret_str)

                # Clean the string
                ret_str = ret_str[12:]
                ret_str = self.cleanup_spaces(ret_str)
                ret_str = re.sub('[^a-zA-Z0-9_./ ]+', '', ret_str)

                # Split items, add them to the digital servos list
                servo_items = ret_str.split(' ')
                if len(servo_items) == 4:
                    servo = {'itf': servo_items[0],
                             'id': servo_items[1],
                             'model_name': servo_items[2],
                             'status': servo_items[3]}
                    self.digital_servos.add_servo(servo)

            elif ret_str.startswith('[DSV] [DUMP]'):

                self.console.append_text(ret_str)

                # Clean the string
                ret_str = ret_str[12:]
                ret_str = self.cleanup_spaces(ret_str)
                ret_str = re.sub('[^a-zA-Z0-9_./ ]+', '', ret_str)

                # Split items, add them to the digital servos list
                register_items = ret_str.split(' ')
                if len(register_items) == 8:
                    register = {'itf': register_items[0],
                                'id': register_items[1],
                                'area': register_items[2],
                                'access': register_items[3],
                                'address': register_items[4],
                                'size': register_items[5],
                                'name': register_items[6],
                                'value': register_items[7]
                            }
                    self.digital_servos.add_register(register)

            elif ret_str.startswith('[PHYS] [POLY]'):

                #self.console.append_text(ret_str)

                # Clean the string
                ret_str = ret_str[13:]
                ret_str = self.cleanup_spaces(ret_str)
                ret_str = re.sub('[^a-zA-Z0-9\-_./ ;]+', '', ret_str)

                # Split items
                poly_items = ret_str.split(' ')
                poly_idx = poly_items[0]
                poly_items.pop(0)
                x = []
                y = []
                for point_str in poly_items:
                    point_items = point_str.split(';')
                    x.append(int(point_items[0]))
                    y.append(int(point_items[1]))

                self.graphics.table.add_poly({'x': x, 'y': y})

            elif ret_str.startswith('[AI] [PATH]'):

                #self.console.append_text(ret_str)

                # Clean the string
                ret_str = ret_str[12:]
                ret_str = self.cleanup_spaces(ret_str)
                ret_str = re.sub('[^a-zA-Z0-9\-_./ ;]+', '', ret_str)

                # Split items
                path_items = ret_str.split(' ')
                x = []
                y = []
                for point_str in path_items:
                    point_items = point_str.split(';')
                    x.append(int(point_items[0]))
                    y.append(int(point_items[1]))

                self.graphics.table.set_path({'x': x, 'y': y})

            elif ret_str.startswith('[TASK]'):

                self.console.append_text(ret_str)

                # Clean the string
                ret_str = ret_str[7:]
                ret_str = self.cleanup_spaces(ret_str)
                ret_str = re.sub('[^a-zA-Z0-9\-_./ ;]+', '', ret_str)

                # Split items
                task_items = ret_str.split(' ')
                if len(task_items) == 7:
                    task = {'id': task_items[0],
                            'name': task_items[1],
                            'state': task_items[2],
                            'nb_dep': task_items[3],
                            'trials': task_items[4],
                            'priority': task_items[5],
                            'value': task_items[6]
                            }
                    self.sequencer.update_task(task)

            elif ret_str.startswith('[MATCH]'):

                #self.console.append_text(ret_str)

                # Clean the string
                ret_str = ret_str[8:]
                ret_str = self.cleanup_spaces(ret_str)
                ret_str = re.sub('[^a-zA-Z0-9\-_./ ;]+', '', ret_str)

                match_items = ret_str.split(' ')

                if len(match_items) == 5:
                    match = {'state': match_items[0],
                             'color': match_items[1],
                             'task': match_items[2],
                             'timer': match_items[3],
                             'points': match_items[4]
                    }
                    self.sequencer.set_match(match)

            # Default: print string
            else:
                self.console.append_text(ret_str)

        except:
            pass
