#!/usr/bin/env python

import rospy
import PyQt5
from PyQt5.QtWidgets import *  # !/bin/bash

import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, uic
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import os


class Ui(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui, self).__init__()  # Call the inherited classes __init__ method
        path = os.path.join(os.path.dirname(__file__), "traj_gui.ui")
        loadUi(path, baseinstance=self)
        rospy.init_node('traj_gui', anonymous=False)
        self.command = rospy.Publisher('/joint_controller/command', JointTrajectory, queue_size=1)
        self.frame_id = "base"
        self.arm_joints = ['base_rotate',
                           'shoulder_tilt',
                           'elbow_tilt',
                           'wrist_tilt',
                           'wrist_rotate',
                           'open_gripper']
        self.joint_pos = [0, 0, 0, 0, 0, 0]
        self.goButton.pressed.connect(self.on_go)
        self.resetButton.pressed.connect(self.on_reset)
        self.baseSlider.valueChanged.connect(self.on_slider_changed)
        self.shoulderSlider.valueChanged.connect(self.on_slider_changed)
        self.elbowSlider.valueChanged.connect(self.on_slider_changed)
        self.wrist_tiltSlider.valueChanged.connect(self.on_slider_changed)
        self.wrist_rotateSlider.valueChanged.connect(self.on_slider_changed)
        self.gripperSlider.valueChanged.connect(self.on_slider_changed)
        self.show()  # Show the GUI

    def on_go(self):
        self.joint_pos = [float(self.base_lineEdit.text()),
                          float(self.shoulder_lineEdit.text()),
                          float(self.elbow_lineEdit.text()),
                          float(self.wrist_tilt_lineEdit.text()),
                          float(self.wrist_rotate_lineEdit.text()),
                          float(self.gripper_lineEdit.text())]

        # Create a single-point arm trajectory with the joint_pos as the end-point
        arm_trajectory = JointTrajectory()
        arm_trajectory.joint_names = self.arm_joints
        arm_trajectory.points.append(JointTrajectoryPoint())
        arm_trajectory.points[0].positions = self.joint_pos
        arm_trajectory.points[0].velocities = [0.0 for i in self.arm_joints]
        arm_trajectory.points[0].accelerations = [0.0 for i in self.arm_joints]
        arm_trajectory.points[0].time_from_start = rospy.Duration(2.0)
        arm_trajectory.header.frame_id = self.frame_id
        arm_trajectory.header.stamp = rospy.Time.now()
        # Publish trajectry
        rospy.sleep(0.5)
        self.command.publish(arm_trajectory)

    def on_reset(self):
        self.baseSlider.setValue(0)
        self.shoulderSlider.setValue(0)
        self.elbowSlider.setValue(0)
        self.wrist_tiltSlider.setValue(0)
        self.wrist_rotateSlider.setValue(0)
        self.gripperSlider.setValue(0)

    def on_slider_changed(self):
        sender = self.sender()
        # print(sender.objectName())
        if sender.objectName() == "baseSlider":
            self.base_lineEdit.setText(str("{:.2f}".format(sender.value()/100*1.57)))
        elif sender.objectName() == "elbowSlider":
            self.elbow_lineEdit.setText(str("{:.2f}".format(sender.value()/100*1.57)))
        elif sender.objectName() == "shoulderSlider":
            self.shoulder_lineEdit.setText(str("{:.2f}".format(sender.value()/100*1.57)))
        elif sender.objectName() == "wrist_rotateSlider":
            self.wrist_rotate_lineEdit.setText(str("{:.2f}".format(sender.value()/100*1.57)))
        elif sender.objectName() == "wrist_tiltSlider":
            self.wrist_tilt_lineEdit.setText(str("{:.2f}".format(sender.value()/100*1.57)))
        elif sender.objectName() == "gripperSlider":
            self.gripper_lineEdit.setText(str("{:.2f}".format(sender.value()/100*1.57)))




if __name__ == '__main__':
    try:
        app = QApplication([])
        window = Ui()
        app.exec_()
    except rospy.ROSInterruptException:
        pass