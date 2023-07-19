#!/usr/bin/env python

# import rospy
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import os
# from ikpy.chain import Chain
from sensor_state_w_table import Ui_MainWindow
from enter_name_dialog import enterNameDialog
import time
import matplotlib.pyplot
# import serial
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
        #create server
        rospy.init_node("sensor_server_node")
        s = rospy.Service('sensor_service', sensor_service, self.sensor_callback)
        self.row_count = 0
        self.service_call_count = 0
        self.mediumActualValue = 0
        self.sparkilingActualValue = 0
        self.ambientActualValue = 0
        self.hotLeftActualValue = 0
        self.hotRightActualValue = 0
        self.chilledActualValue = 0
        self.portioningActualValue = 0

        # self.sensor_test = [True, False, False, False, True, True, True]

    def sensor_callback(self, req):
        self.sensor_list = req.sensor_list
        self.reps = req.reps
        print(self.sensor_list)
        print(self.reps)
        self.service_call_count = self.service_call_count + 1
        print(self.service_call_count)
        
        self.noOfRows = self.sensor_list.count(True)
        if self.service_call_count == 1:
            self.tableWidget.setRowCount(self.noOfRows)
            if self.sensor_list[0] == True:
                self.tableWidget.setItem(self.row_count, 0, QTableWidgetItem("Medium"))
                self.tableWidget.setItem(self.row_count, 1, QTableWidgetItem(str(self.reps)))
                self.tableWidget.setItem(self.row_count, 2, QTableWidgetItem(str(self.mediumActualValue)))
                self.row_count = self.row_count + 1
            if self.sensor_list[1] == True:
                self.tableWidget.setItem(self.row_count, 0, QTableWidgetItem("Sparkling"))
                self.tableWidget.setItem(self.row_count, 1, QTableWidgetItem(str(self.reps)))
                self.tableWidget.setItem(self.row_count, 2, QTableWidgetItem(str(self.sparkilingActualValue)))
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
        
        for i in range(0, self.noOfRows):
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(self.reps)))
            # self.tableWidget.setItem(i, 2, QTableWidgetItem(str(self.actualValue)))
        
        item = self.tableWidget.findItems("Portioning", Qt.MatchExactly)
        row = item[0].row()
        print("row: ", row)
        self.portioningActualValue = int(self.tableWidget.item(row, 2).text())

        # print(actualValue)
        self.portioningActualValue = self.portioningActualValue + 1
        # print(actualValue)
        self.tableWidget.setItem(row, 2, QTableWidgetItem(str(self.portioningActualValue)))
        self.tableWidget.setItem(row, 3, QTableWidgetItem(str((self.reps - self.portioningActualValue) / self.reps * 100)))
        
        return True



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = sensorStateGUI()
    window.show()
    sys.exit(app.exec_())
