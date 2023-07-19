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
from enter_name_dialog import enterNameDialog
from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
from math import *
import numpy as np
import matplotlib.pyplot


class Ui(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui, self).__init__()  # Call the inherited classes __init__ method
        path = os.path.join(os.path.dirname(__file__), "/home/sa/repo/robo/ui/traj_gui_5.ui")
        loadUi(path, baseinstance=self)
        rospy.init_node('traj_gui_w_coord', anonymous=False)
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

        self.chain = Chain.from_urdf_file("/home/sa/repo/robo/urdf/AL5D_arm.urdf", active_links_mask=[False, True, True,
                                                                                                      True, True, True])

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

        # spin boxes
        self.base_spinBox.valueChanged.connect(self.on_spinbox_changed)
        self.elbow_spinBox.valueChanged.connect(self.on_spinbox_changed)
        self.shoulder_spinBox.valueChanged.connect(self.on_spinbox_changed)
        self.wrist_tilt_spinBox.valueChanged.connect(self.on_spinbox_changed)
        self.wrist_rotate_spinBox.valueChanged.connect(self.on_spinbox_changed)
        self.gripper_spinBox.valueChanged.connect(self.on_spinbox_changed)

        # combo box
        self.comboBox.setDuplicatesEnabled(False)
        self.comboBox.activated.connect(self.on_select)
        self.comboBox.currentIndexChanged.connect(self.on_select)
        # settings
        self.settings = QSettings("Brita", "traj_gui")
        self.settings.setValue("Default", [-1.57, 0.0, 0.0, 0.0, 0.0, 0.0])
        self.update_settings()

        # variables
        self.show()  # Show the GUI

    def on_go(self):
        self.joint_pos = [float(self.base_spinBox.value()),
                          float(self.shoulder_spinBox.value()),
                          float(self.elbow_spinBox.value()),
                          float(self.wrist_tilt_spinBox.value()),
                          float(self.wrist_rotate_spinBox.value()),
                          float(self.gripper_spinBox.value())]

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
        # Publish trajectory
        rospy.sleep(0.5)
        self.command.publish(arm_trajectory)
        

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
                                      self.elbow_spinBox.value(),
                                      self.shoulder_spinBox.value(),
                                      self.wrist_tilt_spinBox.value(),
                                      self.wrist_rotate_spinBox.value(),
                                      self.gripper_spinBox.value()]
                                     )
            self.doubleSpinBox_x.setValue(gripper_pos[0])
            self.doubleSpinBox_y.setValue(gripper_pos[1])
            self.doubleSpinBox_z.setValue(gripper_pos[2])

    def update_settings(self):
        keys = self.settings.allKeys()
        for i in keys:
            self.comboBox.addItem(i, self.settings.value(i))
            # print(self.settings.value(i))

    def on_select(self):
        itemName = self.comboBox.currentText()
        itemValues = self.settings.value(itemName)
        print(itemName, itemValues)
        self.move_sliders(itemValues)

    def move_sliders(self, values):
        self.base_spinBox.setValue(float(values[0]))
        self.shoulder_spinBox.setValue(float(values[1]))
        self.elbow_spinBox.setValue(float(values[2]))
        self.wrist_tilt_spinBox.setValue(float(values[3]))
        self.wrist_rotate_spinBox.setValue(float(values[4]))
        self.gripper_spinBox.setValue(float(values[5]))

    def eventFilter(self, source, event):
        if event.type() == QEvent.Wheel:
            return True

        return super(Ui, self).eventFilter(source, event)

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
            self.settings.setValue(name, joints_list)
            # add to combo box
            self.comboBox.addItem(name, joints_list)
            # change current index to latest
            self.comboBox.setCurrentIndex(self.comboBox.count() - 1)

        else:
            print("please enter name!")

    def on_remove(self):
        if self.comboBox.currentText() != "Default":
            self.settings.remove(self.comboBox.currentText())
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
        self.elbow_spinBox.setValue(joint_angles[2])
        self.shoulder_spinBox.setValue(joint_angles[3])
        self.wrist_tilt_spinBox.setValue(joint_angles[4])
        self.wrist_rotate_spinBox.setValue(joint_angles[5])
        self.doneIk = False

    def do_ik(self, pos):
        joint_pos = self.chain.inverse_kinematics(pos)
        return joint_pos

    def on_pos_spinbox_changed(self):
        pass


if __name__ == '__main__':
    try:
        app = QApplication([])
        window = Ui()
        app.exec_()
    except rospy.ROSInterruptException:
    # except:
        pass
