#!/usr/bin/env python

import rospy
import rosparam
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import os
from ikpy.chain import Chain
from robo_ui_2 import Ui_MainWindow
from enter_name_dialog import enterNameDialog
import time
import matplotlib.pyplot
from al5d.srv import sensor_service


class roboGui(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(roboGui, self).__init__()
        self.setupUi(self)
        # absPath = os.path.dirname(os.path.abspath(os.getcwd())) + "/ui/traj_gui_5.ui"
        # path = os.path.join(os.path.dirname(__file__), "/home/sa/repo/robo/ui/traj_gui_5.ui")
        # path = os.path.join(os.path.dirname(__file__), absPath)
        # loadUi(path, baseinstance=self)
        rospy.init_node('traj_gui', anonymous=False)
        self.command = rospy.Publisher('/joint_controller/command', JointTrajectory, queue_size=1)

        # Variables
        self.frame_id = "base"
        self.arm_joints = ['base_rotate',
                           'shoulder_tilt',
                           'elbow_tilt',
                           'wrist_tilt',
                           'wrist_rotate',
                           'open_gripper']
        self.joint_pos = [0, 0, 0, 0, 0, 0]
        self.doneIk = False

        urdfPath =  path = os.path.join(os.path.dirname(__file__), os.pardir, 'urdf')
        print(urdfPath)
        self.chain = Chain.from_urdf_file(urdfPath + '/AL5D_arm_mm.urdf', active_links_mask=[False, True, True, True, True, True])

        # buttons
        self.goButton.pressed.connect(self.on_go)
        self.resetButton.pressed.connect(self.on_reset)
        self.addButton.pressed.connect(self.on_teach)
        self.removeButton.pressed.connect(self.on_remove)
        self.doIKButton.pressed.connect(self.on_do_ik)

        # sliders
        # disable mouse wheel events
        self.baseSlider.installEventFilter(self)
        self.shoulderSlider.installEventFilter(self)
        self.elbowSlider.installEventFilter(self)
        self.wrist_tiltSlider.installEventFilter(self)
        self.wrist_rotateSlider.installEventFilter(self)
        self.gripperSlider.installEventFilter(self)

        # connect signals to slots
        self.baseSlider.sliderMoved.connect(self.on_slider_moved)
        self.shoulderSlider.sliderMoved.connect(self.on_slider_moved)
        self.elbowSlider.sliderMoved.connect(self.on_slider_moved)
        self.wrist_tiltSlider.sliderMoved.connect(self.on_slider_moved)
        self.wrist_rotateSlider.sliderMoved.connect(self.on_slider_moved)
        self.gripperSlider.sliderMoved.connect(self.on_slider_moved)

        # self.baseSlider.valueChanged.connect(self.on_slider_moved)
        # self.shoulderSlider.valueChanged.connect(self.on_slider_moved)
        # self.elbowSlider.valueChanged.connect(self.on_slider_moved)
        # self.wrist_tiltSlider.valueChanged.connect(self.on_slider_moved)
        # self.wrist_rotateSlider.valueChanged.connect(self.on_slider_moved)
        # self.gripperSlider.valueChanged.connect(self.on_slider_moved)

        # spin boxes
        self.base_spinBox.valueChanged.connect(self.on_spinbox_changed)
        self.elbow_spinBox.valueChanged.connect(self.on_spinbox_changed)
        self.shoulder_spinBox.valueChanged.connect(self.on_spinbox_changed)
        self.wrist_tilt_spinBox.valueChanged.connect(self.on_spinbox_changed)
        self.wrist_rotate_spinBox.valueChanged.connect(self.on_spinbox_changed)
        self.gripper_spinBox.valueChanged.connect(self.on_spinbox_changed)

        # self.doubleSpinBox_x.textChanged.connect(self.on_pos_spinbox_changed)
        # self.doubleSpinBox_y.textChanged.connect(self.on_pos_spinbox_changed)
        # self.doubleSpinBox_z.textChanged.connect(self.on_pos_spinbox_changed)

        # combo box
        self.comboBox.setDuplicatesEnabled(False)
        self.comboBox.activated.connect(self.on_select)
        self.comboBox.currentIndexChanged.connect(self.on_select)
        # settings
        self.settings1 = QSettings("Brita", "traj_gui")
        self.settings1.setValue("Default", [-1.57, 0.0, 0.0, 0.0, 0.0, 0.0])

        self.ax = matplotlib.pyplot.figure().add_subplot(111, projection='3d')

        self.update_settings()

        #####################################################################################################################
        self.seqNames = []
        self.data = {1: {'name': "Default sequence", 'positions': {1: {'x': 130, 'y': -12, 'z': 311},
                                                                   2: {'x': 168, 'y': -12, 'z': 247},
                                                                   3: {'x': 130, 'y': -12, 'z': 311},
                                                                   }
                         }
        }
        
        self.seqThread = Thread()

        self.settings2 = QSettings("Brita", "Test_sequences")
        # self.settings.setPath(QSettings.NativeFormat, QSettings.UserScope, os.path.abspath(os.getcwd())+"/settings")
        # if QFile("$HOME/.config/Brita/Test_sequences.conf").exists():
        if self.settings2.contains("Saved sequences"):
            print("file exists")
            self.data = self.settings2.value("Saved sequences")
        else:
            print("file does not exist")
            self.settings2.setValue("Saved sequences", self.data)

        self.noOfSeq = len(self.data.keys())
        self.tableWidget.setColumnCount(3)
        # self.load_data()
        self.show()

        for items in self.data.items():
            self.seqNames.append(items[1]["name"])

        self.listWidget.addItems(self.seqNames)
        self.listWidget.currentRowChanged.connect(self.on_row_changed)
        self.listWidget.setCurrentRow(0)

        for index in range(self.listWidget.count()):
            item = self.listWidget.item(index)
            item.setFlags(item.flags() | Qt.ItemIsEditable)

        self.pushButton_addSequence.pressed.connect(self.on_add_sequence)
        self.pushButton_removeSequence.pressed.connect(self.on_remove_sequence)
        self.pushButton_plus.pressed.connect(self.on_plus)
        self.pushButton_minus.pressed.connect(self.on_minus)
        self.tableWidget.itemDoubleClicked.connect(self.on_double_click)
        self.pushButton_runSequence.pressed.connect(self.on_run_sequence)
        self.pushButton_stopSequence.pressed.connect(self.on_stop_sequence)

        # Checkable comboBox
        self.model = QStandardItemModel(6, 1)
        self.sensorList = ["Medium", "Sparkling", "Ambient", "Hot left", "Hot right", "Chilled", "Portioning"]
        for i in range(0, 7):
            item = QStandardItem(self.sensorList[i])
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            item.setData(Qt.Unchecked, Qt.CheckStateRole)
            self.model.setItem(i, 0, item)

        self.sensorMask = [0]*7

        self.comboBox_2.setModel(self.model)
        self.comboBox_2.model().dataChanged.connect(self.on_checklist_changes)
        # rospy.set_param("checked_sensors", self.checkedItems)

        self.show()  # Show the GUI

    def on_go(self):
        self.joint_pos = [float(self.base_spinBox.value()),
                          float(self.shoulder_spinBox.value()),
                          float(self.elbow_spinBox.value()),
                          float(self.wrist_tilt_spinBox.value()),
                          float(self.wrist_rotate_spinBox.value()),
                          float(self.gripper_spinBox.value())]
        print(self.joint_pos)

        # Create a single-point arm trajectory with the joint_pos as the end-point
        arm_trajectory = JointTrajectory()
        arm_trajectory.joint_names = self.arm_joints
        arm_trajectory.points.append(JointTrajectoryPoint())
        arm_trajectory.points[0].positions = self.joint_pos
        arm_trajectory.points[0].velocities = [0.0 for i in self.arm_joints]
        arm_trajectory.points[0].accelerations = [0.0 for i in self.arm_joints]
        # arm_trajectory.points[0].time_from_start = rospy.Duration(2.0)
        arm_trajectory.header.frame_id = self.frame_id
        arm_trajectory.header.stamp = rospy.Time.now()
        # Publish trajectory
        rospy.sleep(0.5)
        self.command.publish(arm_trajectory)

        plot_joints = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        for i in range(0, 5):
            plot_joints[i + 1] = self.joint_pos[i]
        # print("joint_pos :", joint_pos)
        # print("new_joints", plot_joints)

        self.chain.plot(plot_joints, self.ax)
        matplotlib.pyplot.show()
        print("plotted")

    def on_reset(self):
        self.baseSlider.setValue(0)
        self.base_spinBox.setValue(0)
        self.shoulderSlider.setValue(0)
        self.shoulder_spinBox.setValue(0)
        self.elbowSlider.setValue(0)
        self.elbow_spinBox.setValue(0)
        self.wrist_tiltSlider.setValue(0)
        self.wrist_tilt_spinBox.setValue(0)
        self.wrist_rotateSlider.setValue(0)
        self.wrist_rotate_spinBox.setValue(0)
        self.gripperSlider.setValue(0)
        self.gripper_spinBox.setValue(0)
        # self.doubleSpinBox_x.setValue(4.19)

    def on_slider_moved(self):
        sender = self.sender()
        # print(sender.objectName())
        if sender.objectName() == "baseSlider":
            self.base_spinBox.setValue(sender.value() / 100 * 1.57)
        elif sender.objectName() == "elbowSlider":
            self.elbow_spinBox.setValue(sender.value() / 100 * 1.57)
        elif sender.objectName() == "shoulderSlider":
            self.shoulder_spinBox.setValue(sender.value() / 100 * 1.57)
        elif sender.objectName() == "wrist_rotateSlider":
            self.wrist_rotate_spinBox.setValue(sender.value() / 100 * 1.57)
        elif sender.objectName() == "wrist_tiltSlider":
            self.wrist_tilt_spinBox.setValue(sender.value() / 100 * 1.57)
        elif sender.objectName() == "gripperSlider":
            self.gripper_spinBox.setValue(sender.value() / 100 * 1.57)

    def on_spinbox_changed(self):
        sender = self.sender()
        if sender.objectName() == "base_spinBox":
            self.baseSlider.setValue(sender.value() * 100 / 1.57)
        elif sender.objectName() == "elbow_spinBox":
            self.elbowSlider.setValue(sender.value() * 100 / 1.57)
        elif sender.objectName() == "shoulder_spinBox":
            self.shoulderSlider.setValue(sender.value() * 100 / 1.57)
        elif sender.objectName() == "wrist_rotate_spinBox":
            self.wrist_rotateSlider.setValue(sender.value() * 100 / 1.57)
        elif sender.objectName() == "wrist_tilt_spinBox":
            self.wrist_tiltSlider.setValue(sender.value() * 100 / 1.57)
        elif sender.objectName() == "gripper_spinBox":
            self.gripperSlider.setValue(sender.value() * 100 / 1.57)

        if not self.doneIk:
            gripper_pos = self.do_fk([self.base_spinBox.value(),
                                      self.shoulder_spinBox.value(),
                                      self.elbow_spinBox.value(),
                                      self.wrist_tilt_spinBox.value(),
                                      self.wrist_rotate_spinBox.value(),
                                      self.gripper_spinBox.value()]
                                     )
            self.doubleSpinBox_x.setValue(gripper_pos[0])
            self.doubleSpinBox_y.setValue(gripper_pos[1])
            self.doubleSpinBox_z.setValue(gripper_pos[2])

    def update_settings(self):
        keys = self.settings1.allKeys()
        for i in keys:
            self.comboBox.addItem(i, self.settings1.value(i))
            # print(self.settings.value(i))

    def on_select(self):
        itemName = self.comboBox.currentText()
        itemValues = self.settings1.value(itemName)
        print(itemName, itemValues)
        self.move_sliders(itemValues)

    def move_sliders(self, values):
        # self.base_spinBox.setValue(values[0])
        # self.shoulder_spinBox.setValue(values[1])
        # self.elbow_spinBox.setValue(values[2])
        # self.wrist_tilt_spinBox.setValue(values[3])
        # self.wrist_rotate_spinBox.setValue(values[4])
        # self.gripper_spinBox.setValue(values[5])
        self.base_spinBox.setValue(float(values[0]))
        self.shoulder_spinBox.setValue(float(values[1]))
        self.elbow_spinBox.setValue(float(values[2]))
        self.wrist_tilt_spinBox.setValue(float(values[3]))
        self.wrist_rotate_spinBox.setValue(float(values[4]))
        self.gripper_spinBox.setValue(float(values[5]))

    def eventFilter(self, source, event):
        if event.type() == QEvent.Wheel:
            return True

        return super(roboGui, self).eventFilter(source, event)

    def on_teach(self):
        # get current joint positions
        joints_list = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        joints_list[0] = self.base_spinBox.value()
        joints_list[1] = self.shoulder_spinBox.value()
        joints_list[2] = self.elbow_spinBox.value()
        joints_list[3] = self.wrist_tilt_spinBox.value()
        joints_list[4] = self.wrist_rotate_spinBox.value()
        joints_list[5] = self.gripper_spinBox.value()
        print(joints_list)
        # check for no. of itmes in the combo box
        # add to setings
        # self.settings.setValue("Custom" + str(self.comboBox.count()), joints_list)
        # open dialog to enter name
        dialog = enterNameDialog()
        # Display current Settings from the QSettings object
        dialog.lineEdit.setText("Custom" + str(self.comboBox.count()))
        dialog.lineEdit.selectAll()
        dialog.show()
        dialog.exec_()
        name = dialog.lineEdit.text()
        # update combo box
        print("name = ", name)
        if name != "":
            # add to settings
            self.settings1.setValue(name, joints_list)
            # add to combo box
            self.comboBox.addItem(name, joints_list)
            # change current index to latest
            self.comboBox.setCurrentIndex(self.comboBox.count() - 1)

        else:
            print("please enter name!")

    def on_remove(self):
        if self.comboBox.currentText() != "Default":
            self.settings1.remove(self.comboBox.currentText())
            self.comboBox.removeItem(self.comboBox.currentIndex())

    def do_fk(self, joint_pos):
        new_joints = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        for i in range(0, 5):
            new_joints[i + 1] = joint_pos[i]
        print("joint_pos :", joint_pos)
        print("new_joints", new_joints)
        pos = self.chain.forward_kinematics(new_joints)[:3, 3]
        print(pos)
        return pos

    def on_do_ik(self):
        print("doing ik")
        self.doneIk = True
        joint_angles = self.do_ik([self.doubleSpinBox_x.value(), self.doubleSpinBox_y.value(),
                                   self.doubleSpinBox_z.value()])
        print(joint_angles)
        self.base_spinBox.setValue(joint_angles[1])
        self.shoulder_spinBox.setValue(joint_angles[2])
        self.elbow_spinBox.setValue(joint_angles[3])
        self.wrist_tilt_spinBox.setValue(joint_angles[4])
        # self.wrist_rotate_spinBox.setValue(joint_angles[5])
        self.doneIk = False

    def do_ik(self, pos):
        joint_pos = self.chain.inverse_kinematics(pos)
        return joint_pos

    def load_data(self, name):
        for items in self.data.items():
            if items[1]["name"] == name:
                # print("No. of positions for ", name, " = ", len(items[1]["positions"].keys()))
                print(items[1])
                self.tableWidget.setRowCount(len(items[1]["positions"].keys()))

        for items in self.data.items():
            if items[1]["name"] == name:
                for pos in items[1]["positions"]:
                    self.tableWidget.setItem(pos - 1, 0, QTableWidgetItem(str(items[1]["positions"][pos]["x"])))
                    self.tableWidget.setItem(pos - 1, 1, QTableWidgetItem(str(items[1]["positions"][pos]["y"])))
                    self.tableWidget.setItem(pos - 1, 2, QTableWidgetItem(str(items[1]["positions"][pos]["z"])))

    def load_sequences(self):
        for names in self.data:
            self.seqNames[names] = self.data[names]

    def on_row_changed(self):
        name = self.listWidget.item(self.listWidget.currentRow()).text()
        self.load_data(name)

    def on_add_sequence(self):
        dialog = enterNameDialog()
        dialog.lineEdit.setText("Custom sequence")
        QTimer.singleShot(0, 0, dialog.lineEdit.selectAll)
        dialog.show()
        dialog.exec_()
        name = dialog.lineEdit.text()
        self.listWidget.insertItem(self.listWidget.count(), name)
        self.data[self.noOfSeq + 1] = {"name": name, "positions": {}}
        print("sequence added")
        print(self.data)

    def on_remove_sequence(self):
        currentSeqName = self.listWidget.currentItem().text()
        if currentSeqName != "Default sequence":
            for items in self.data.items():
                if items[1]["name"] == currentSeqName:
                    currentKey = items[0]
            del self.data[currentKey]
            self.listWidget.takeItem(self.listWidget.currentRow())
            print("deleted something ", self.data)
            self.load_data(self.listWidget.currentItem().text())

    def on_plus(self):
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        currentSeqName = self.listWidget.currentItem().text()
        for items in self.data.items():
            if items[1]["name"] == currentSeqName:
                items[1]["positions"][self.tableWidget.rowCount()] = {"x": 0.0, "y": 0.0, "z": 0.0}
        self.load_data(currentSeqName)
        # print(self.data)

    def on_minus(self):
        if self.tableWidget.rowCount() is not 0:
            self.tableWidget.removeRow(self.tableWidget.rowCount())
            currentSeqName = self.listWidget.currentItem().text()
            for items in self.data.items():
                if items[1]["name"] == currentSeqName:
                    del items[1]["positions"][self.tableWidget.rowCount()]
        self.load_data(self.listWidget.currentItem().text())

    def on_double_click(self):
        print("Double clicked")
        self.tableWidget.itemChanged.connect(self.on_item_changed)
        # self.tableWidget.clearFocus()

    def on_item_changed(self):
        print("item changed")
        currentRow = self.tableWidget.currentRow()
        currentColumn = self.tableWidget.currentColumn()
        currentData = self.tableWidget.currentItem().text()
        # print(currentData)
        currentSeqName = self.listWidget.currentItem().text()
        print("editing ", currentSeqName)
        self.tableWidget.itemChanged.disconnect()

        for items in self.data.items():
            if items[1]["name"] == currentSeqName:
                if currentColumn == 0:
                    # change x value of current position
                    items[1]["positions"][currentRow + 1]["x"] = currentData
                elif currentColumn == 1:
                    # change x value of current position
                    items[1]["positions"][currentRow + 1]["y"] = currentData
                elif currentColumn == 2:
                    # change x value of current position
                    items[1]["positions"][currentRow + 1]["z"] = currentData
            print(self.data)

    def on_run_sequence(self):
        coord = [0.0, 0.0, 0.0]
        jointPositions = {}
        currSeqName = self.listWidget.currentItem().text()
        for items in self.data.items():
            if items[1]["name"] == currSeqName:
                positions = items[1]["positions"]

        for pos in positions.items():
            coord[0] = pos[1]["x"]
            coord[1] = pos[1]["y"]
            coord[2] = pos[1]["z"]
            # print(coord)
            jointAngles = self.do_ik(coord)
            jointPositions.update({pos[0]: jointAngles.tolist()})
        print("sensor mask", self.sensorMask)
        self.seqThread.setup_seq(jointPositions, self.doubleSpinBox_interval.value(), self.spinBox_frequency.value(), self.sensorMask)
        self.seqThread.start()

    def on_stop_sequence(self):
        self.seqThread.terminate()
        print("Sequence terminated")

    def on_checklist_changes(self):
        self.checkedItems = []
        for i in range(0, self.comboBox_2.count()):
            if self.comboBox_2.model().item(i, 0).checkState() == Qt.Checked:
                self.checkedItems.append(str(self.comboBox_2.model().item(i, 0).text()))
                # self.checkedItems[i] = str(self.comboBox_2.model().item(i, 0).text())
        print(self.checkedItems)

        for i in range(0, 7):
            item = self.model.item(i)
            if item.checkState() == Qt.Checked:
                self.sensorMask[i] = True
            else:
                self.sensorMask[i] = False
        print(self.sensorMask)

    def closeEvent(self, event):
        print("close event triggered")
        self.settings2.setValue('Saved sequences', self.data)


class Thread(QThread):

    def __init__(self):
        super(Thread, self).__init__()
        self.frame_id = "base"
        self.arm_joints = ['base_rotate',
                       'shoulder_tilt',
                       'elbow_tilt',
                       'wrist_tilt',
                       'wrist_rotate',
                       'open_gripper']
        self.command = rospy.Publisher('/joint_controller/command', JointTrajectory, queue_size=1)

    def setup_seq(self, joint_positions, interval, reps , sensors):
        self.positions = joint_positions
        self.interval = interval
        self.reps = reps
        self.sensors = sensors
        print(self.sensors)
        self.coord = [0.0, 0.0, 0.0]
        self.pub_joints = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        service = rospy.ServiceProxy('sensor_service', sensor_service)
        res = service(self.sensors, self.reps)
        
    def run(self):
        for reps in range(self.reps):
            for pos in self.positions.items():
                self.pub_joints[0] = pos[1][1]
                self.pub_joints[1] = pos[1][2]
                self.pub_joints[2] = pos[1][3]
                self.pub_joints[3] = pos[1][4]
                self.pub_joints[4] = -1.43

                # Create a single-point arm trajectory with the joint_pos as the end-point
                arm_trajectory = JointTrajectory()
                arm_trajectory.joint_names = self.arm_joints
                arm_trajectory.points.append(JointTrajectoryPoint())
                arm_trajectory.points[0].positions = self.pub_joints
                arm_trajectory.points[0].velocities = [0.0 for i in self.arm_joints]
                arm_trajectory.points[0].accelerations = [0.0 for i in self.arm_joints]
                arm_trajectory.points[0].time_from_start = rospy.Duration(2.0)
                arm_trajectory.header.frame_id = self.frame_id
                arm_trajectory.header.stamp = rospy.Time.now()
                # Publish trajectory
                rospy.sleep(0.5)
                self.command.publish(arm_trajectory)
                print(self.pub_joints)
                time.sleep(self.interval / 1000)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = roboGui()
    window.show()
    sys.exit(app.exec_())
