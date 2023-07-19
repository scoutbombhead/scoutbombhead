#!/usr/bin/env python

# import rospy
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import os
from ikpy.chain import Chain
from sensor_state_ui import Ui_MainWindow
from enter_name_dialog import enterNameDialog
import time
import matplotlib.pyplot
import serial
import rospy
from al5d.srv import sensor_service

"""
led = Chilled
led_2 = Medium
led_3 = Sparkling
led_4 = Ambient
led_5 = Hot 1
led_6 = Hot_2
led_7 = Portioning
"""

"""
Sensor list:
Sensor1 : Medium
Sensor2: Sparkling
Sensor3: Ambient
Sensor4: Hot left
Sensor5: Hot right
Sensor 6: Chilled
Sensor 7: Portioning
"""


class sensorStateGUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(sensorStateGUI, self).__init__()
        self.setupUi(self)
        self.show()
        self.mediumActualValue = 0
        self.sparklingActualValue = 0
        self.ambientActualValue = 0
        self.hotLeftActualValue = 0
        self.hotRightActualValue = 0
        self.chilledActualValue = 0
        self.portioningActualValue = 0
        self.serviceCallCount = 0
        self.row_count = 0
        #create server
        rospy.init_node("sensor_server")
        s = rospy.Service('sensor_service', sensor_service, self.sensor_callback)

        self.thread = Thread()
        self.thread.setLed.connect(self.set_led)
        self.thread.updateCounters.connect(self.update_counters)
        self.thread.updateTable.connect(self.update_table)
        self.thread.start()
        self.counters = [0, 0, 0, 0, 0, 0, 0]
        self.tableWidget.setRowCount(0)

        self.pushButton_reset.pressed.connect(self.reset_counters)

    def sensor_callback(self, req):
        print("service recieved")
        self.sensor_list = req.sensor_list
        self.reps = req.reps
        print(self.sensor_list)
        self.tableWidget.setRowCount(0)
        self.resetActualValues()

        self.noOfRows = self.sensor_list.count(True)
        self.tableWidget.setRowCount(self.noOfRows)
        if self.sensor_list[0] == True:
            self.tableWidget.setItem(self.row_count, 0, QTableWidgetItem("Medium"))
            self.tableWidget.setItem(self.row_count, 1, QTableWidgetItem(str(self.reps)))
            self.tableWidget.setItem(self.row_count, 2, QTableWidgetItem(str(self.mediumActualValue)))
            self.row_count = self.row_count + 1
        if self.sensor_list[1] == True:
            self.tableWidget.setItem(self.row_count, 0, QTableWidgetItem("Sparkling"))
            self.tableWidget.setItem(self.row_count, 1, QTableWidgetItem(str(self.reps)))
            self.tableWidget.setItem(self.row_count, 2, QTableWidgetItem(str(self.sparklingActualValue)))
            self.row_count = self.row_count + 1
        if self.sensor_list[2] == True:
            self.tableWidget.setItem(self.row_count, 0, QTableWidgetItem("Ambient"))
            self.tableWidget.setItem(self.row_count, 1, QTableWidgetItem(str(self.reps)))
            self.tableWidget.setItem(self.row_count, 2, QTableWidgetItem(str(self.ambientActualValue)))
            self.row_count = self.row_count + 1
        if self.sensor_list[3] == True:
            self.tableWidget.setItem(self.row_count, 0, QTableWidgetItem("Hot left"))
            self.tableWidget.setItem(self.row_count, 1, QTableWidgetItem(str(self.reps)))
            self.tableWidget.setItem(self.row_count, 2, QTableWidgetItem(str(self.hotLeftActualValue)))
            self.row_count = self.row_count + 1
        if self.sensor_list[4] == True:
            self.tableWidget.setItem(self.row_count, 0, QTableWidgetItem("Hot right"))
            self.tableWidget.setItem(self.row_count, 1, QTableWidgetItem(str(self.reps)))
            self.tableWidget.setItem(self.row_count, 2, QTableWidgetItem(str(self.hotRightActualValue)))
            self.row_count = self.row_count + 1
        if self.sensor_list[5] == True:
            self.tableWidget.setItem(self.row_count, 0, QTableWidgetItem("Chilled"))
            self.tableWidget.setItem(self.row_count, 1, QTableWidgetItem(str(self.reps)))
            self.tableWidget.setItem(self.row_count, 2, QTableWidgetItem(str(self.chilledActualValue)))
            self.row_count = self.row_count + 1
        if self.sensor_list[6] == True:
            self.tableWidget.setItem(self.row_count, 0, QTableWidgetItem("Portioning"))
            self.tableWidget.setItem(self.row_count, 1, QTableWidgetItem(str(self.reps)))
            self.tableWidget.setItem(self.row_count, 2, QTableWidgetItem(str(self.portioningActualValue)))
            self.row_count = self.row_count + 1
        
        self.row_count = 0
        return True

    def set_led(self, led, value):
        """
        led = Chilled
        led_2 = Medium
        led_3 = Sparkling
        led_4 = Ambient
        led_5 = Hot 1
        led_6 = Hot_2
        led_7 = Portioning
        """
        if led == 1:
            self.led_1.value = value
            #if value:
        if led == 2:
            self.led_2.value = value
        if led == 3:
            self.led_3.value = value
        if led == 4:
            self.led_4.value = value
        if led == 5:
            self.led_5.value = value
        if led == 6:
            self.led_6.value = value
        if led == 7:
            self.led_7.value = value

    def update_counters(self, counters):
        self.lcdNumber_1.display(counters[0])
        self.lcdNumber_2.display(counters[1])
        self.lcdNumber_3.display(counters[2])
        self.lcdNumber_4.display(counters[3])
        self.lcdNumber_5.display(counters[4])
        self.lcdNumber_6.display(counters[5])
        self.lcdNumber_7.display(counters[6])
    
    def update_table(self, sensor): 
        if sensor == 1:
            self.mediumActualValue = self.mediumActualValue + 1
            if(self.tableWidget.findItems("Medium", Qt.MatchExactly)!=[]):
                row = self.tableWidget.findItems("Medium", Qt.MatchExactly)[0].row()
                # self.chilledActualValue = int(self.tableWidget.item(row, 2).text())
                self.tableWidget.setItem(row, 2, QTableWidgetItem(str(self.mediumActualValue)))
                self.tableWidget.setItem(row, 3, QTableWidgetItem(
                    str((self.reps - self.mediumActualValue) / self.reps * 100)))
        
        if sensor == 2:
            self.sparklingActualValue = self.sparklingActualValue + 1
            if(self.tableWidget.findItems("Sparkling", Qt.MatchExactly)!=[]):
                row = self.tableWidget.findItems("Sparkling", Qt.MatchExactly)[0].row()
                # self.chilledActualValue = int(self.tableWidget.item(row, 2).text())
                self.tableWidget.setItem(row, 2, QTableWidgetItem(str(self.sparklingActualValue)))
                self.tableWidget.setItem(row, 3, QTableWidgetItem(
                    str((self.reps - self.sparklingActualValue) / self.reps * 100)))

        if sensor == 3:
            self.ambientActualValue = self.ambientActualValue + 1
            if(self.tableWidget.findItems("Ambient", Qt.MatchExactly)!=[]):
                row = self.tableWidget.findItems("Ambient", Qt.MatchExactly)[0].row()
                # self.chilledActualValue = int(self.tableWidget.item(row, 2).text())
                self.tableWidget.setItem(row, 2, QTableWidgetItem(str(self.ambientActualValue)))
                self.tableWidget.setItem(row, 3, QTableWidgetItem(
                    str((self.reps - self.ambientActualValue) / self.reps * 100)))
        
        if sensor == 4:
            self.hotLeftActualValue = self.hotLeftActualValue + 1
            if(self.tableWidget.findItems("Hot left", Qt.MatchExactly)!=[]):
                row = self.tableWidget.findItems("Hot left", Qt.MatchExactly)[0].row()
                # self.chilledActualValue = int(self.tableWidget.item(row, 2).text())
                self.tableWidget.setItem(row, 2, QTableWidgetItem(str(self.hotLeftActualValue)))
                self.tableWidget.setItem(row, 3, QTableWidgetItem(
                    str((self.reps - self.hotLeftActualValue) / self.reps * 100)))
        
        if sensor == 5:
            self.hotRightActualValue = self.hotRightActualValue + 1
            if(self.tableWidget.findItems("Hot right", Qt.MatchExactly)!=[]):
                row = self.tableWidget.findItems("Hot right", Qt.MatchExactly)[0].row()
                # self.chilledActualValue = int(self.tableWidget.item(row, 2).text())
                self.tableWidget.setItem(row, 2, QTableWidgetItem(str(self.hotRightActualValue)))
                self.tableWidget.setItem(row, 3, QTableWidgetItem(
                    str((self.reps - self.hotRightActualValue) / self.reps * 100)))
        
        if sensor == 6:
            self.chilledActualValue = self.chilledActualValue + 1
            if(self.tableWidget.findItems("Chilled", Qt.MatchExactly)!=[]):
                row = self.tableWidget.findItems("Chilled", Qt.MatchExactly)[0].row()
                # self.chilledActualValue = int(self.tableWidget.item(row, 2).text())
                self.tableWidget.setItem(row, 2, QTableWidgetItem(str(self.chilledActualValue)))
                self.tableWidget.setItem(row, 3, QTableWidgetItem(
                    str((self.reps - self.chilledActualValue) / self.reps * 100)))

        if sensor == 7:
            self.portioningActualValue = self.portioningActualValue + 1
            if(self.tableWidget.findItems("Portioning", Qt.MatchExactly)!=[]):
                row = self.tableWidget.findItems("Portioning", Qt.MatchExactly)[0].row()
                # self.chilledActualValue = int(self.tableWidget.item(row, 2).text())
                self.tableWidget.setItem(row, 2, QTableWidgetItem(str(self.portioningActualValue)))
                self.tableWidget.setItem(row, 3, QTableWidgetItem(
                    str((self.reps - self.portioningActualValue) / self.reps * 100)))
        


    def resetActualValues(self):
        self.mediumActualValue = 0
        self.sparklingActualValue = 0
        self.ambientActualValue = 0
        self.hotLeftActualValue = 0
        self.hotRightActualValue = 0
        self.chilledActualValue = 0
        self.portioningActualValue = 0
        self.serviceCallCount = 0
    
    def reset_counters(self):
        self.lcdNumber_1.display(0)
        self.lcdNumber_2.display(0)
        self.lcdNumber_3.display(0)
        self.lcdNumber_4.display(0)
        self.lcdNumber_5.display(0)
        self.lcdNumber_6.display(0)
        self.lcdNumber_7.display(0)
        self.thread.counters = [0, 0, 0, 0, 0, 0, 0]


class Thread(QThread):

    setLed = pyqtSignal(int, bool)
    updateCounters = pyqtSignal(list)
    updateTable = pyqtSignal(int)

    def __init__(self):
        super(Thread, self).__init__()
        self.ser = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate=115200,
            parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_ONE)

        self.counters = [0, 0, 0, 0, 0, 0, 0]
        self.pressed = [False, False, False, False, False, False, False]

    def run(self):
        while True:
            raw = self.ser.read_until(b'\xaa\x55').hex()
            # print(raw)
            # print(len(raw))
        # hexlist = [raw[i:i + 2] for i in range(0, len(raw), 2)]
        # print(hexlist)
            if len(raw) == 176:
                # print(raw[24:26], raw[48:50], raw[72:74], raw[96:98], raw[120:122], raw[144:146], raw[168:170])
                if raw[24:26] == "01":
                    self.setLed.emit(1, True)
                    if not self.pressed[0]:
                        self.counters[0] = self.counters[0] + 1
                        self.updateTable.emit(1)
                        self.pressed[0] = True
                elif raw[24:26] == "00":
                    self.setLed.emit(1, False)
                    if self.pressed[0]:
                        self.pressed[0] = False

                if raw[48:50] == "01":
                    self.setLed.emit(2, True)
                    if not self.pressed[1]:
                        self.counters[1] = self.counters[1] + 1
                        self.updateTable.emit(2)
                        self.pressed[1] = True
                elif raw[48:50] == "00":
                    self.setLed.emit(2, False)
                    if self.pressed[1]:
                        self.pressed[1] = False

                if raw[72:74] == "01":
                    self.setLed.emit(3, True)
                    if not self.pressed[2]:
                        self.counters[2] = self.counters[2] + 1
                        self.updateTable.emit(3)
                        self.pressed[2] = True
                elif raw[72:74] == "00":
                    self.setLed.emit(3, False)
                    if self.pressed[2]:
                        self.pressed[2] = False

                if raw[96:98] == "01":
                    self.setLed.emit(4, True)
                    if not self.pressed[3]:
                        self.counters[3] = self.counters[3] + 1
                        self.updateTable.emit(4)
                        self.pressed[3] = True
                elif raw[96:98] == "00":
                    self.setLed.emit(4, False)
                    if self.pressed[3]:
                        self.pressed[3] = False

                if raw[120:122] == "01":
                    self.setLed.emit(5, True)
                    if not self.pressed[4]:
                        self.counters[4] = self.counters[4] + 1
                        self.updateTable.emit(5)
                        self.pressed[4] = True
                elif raw[120:122] == "00":
                    self.setLed.emit(5, False)
                    if self.pressed[4]:
                        self.pressed[4] = False

                if raw[144:146] == "01":
                    self.setLed.emit(6, True)
                    if not self.pressed[5]:
                        self.counters[5] = self.counters[5] + 1
                        self.updateTable.emit(6)
                        self.pressed[5] = True
                elif raw[144:146] == "00":
                    self.setLed.emit(6, False)
                    if self.pressed[5]:
                        self.pressed[5] = False

                if raw[168:170] == "01":
                    self.setLed.emit(7, True)
                    if not self.pressed[6]:
                        self.counters[6] = self.counters[6] + 1
                        self.updateTable.emit(7)
                        self.pressed[6] = True
                elif raw[168:170] == "00":
                    self.setLed.emit(7, False)
                    if self.pressed[6]:
                        self.pressed[6] = False

            self.updateCounters.emit(self.counters)




if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = sensorStateGUI()
    window.show()
    sys.exit(app.exec_())
