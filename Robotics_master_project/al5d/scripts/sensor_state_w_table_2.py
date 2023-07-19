# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sensor_state_w_table.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from QLed import QLed as LED


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(571, 653)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.led_6 = LED(self.centralwidget)
        self.led_6.setEnabled(False)
        self.led_6.setGeometry(QtCore.QRect(190, 180, 64, 48))
        self.led_6.setVisible(True)
        # self.led_6.setColor(QtGui.QColor(115, 210, 22))
        # self.led_6.setState(False)
        self.led_6.setObjectName("led_6")
        
        self.led_1 = LED(self.centralwidget)
        self.led_1.setGeometry(QtCore.QRect(230, 110, 64, 48))
        self.led_1.setVisible(True)
        # self.led_1.setColor(QtGui.QColor(115, 210, 22))
        # self.led_1.setState(False)
        self.led_1.setObjectName("led_1")
        
        self.led_2 = LED(self.centralwidget)
        self.led_2.setGeometry(QtCore.QRect(330, 110, 64, 48))
        self.led_2.setVisible(True)
        # self.led_2.setColor(QtGui.QColor(115, 210, 22))
        # self.led_2.setState(False)
        self.led_2.setObjectName("led_2")
        
        self.led_3 = LED(self.centralwidget)
        self.led_3.setGeometry(QtCore.QRect(370, 180, 64, 48))
        self.led_3.setVisible(True)
        # self.led_3.setColor(QtGui.QColor(115, 210, 22))
        # self.led_3.setState(False)
        self.led_3.setObjectName("led_3")
        
        self.led_5 = LED(self.centralwidget)
        self.led_5.setGeometry(QtCore.QRect(330, 270, 64, 48))
        self.led_5.setVisible(True)
        # self.led_5.setColor(QtGui.QColor(115, 210, 22))
        # self.led_5.setState(False)
        self.led_5.setObjectName("led_5")
        
        self.led_4 = LED(self.centralwidget)
        self.led_4.setGeometry(QtCore.QRect(230, 270, 64, 48))
        self.led_4.setVisible(True)
        # self.led_4.setColor(QtGui.QColor(115, 210, 22))
        # self.led_4.setState(False)
        self.led_4.setObjectName("led_4")
        
        self.led_7 = LED(self.centralwidget)
        self.led_7.setGeometry(QtCore.QRect(280, 180, 64, 48))
        self.led_7.setVisible(True)
        # self.led_7.setColor(QtGui.QColor(115, 210, 22))
        # self.led_7.setState(False)
        self.led_7.setObjectName("led_7")
        
        self.lcdNumber_6 = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber_6.setGeometry(QtCore.QRect(90, 200, 64, 23))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.lcdNumber_6.setFont(font)
        self.lcdNumber_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lcdNumber_6.setObjectName("lcdNumber_6")
        self.lcdNumber_1 = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber_1.setGeometry(QtCore.QRect(220, 80, 64, 23))
        self.lcdNumber_1.setObjectName("lcdNumber_x")
        self.lcdNumber_2 = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber_2.setGeometry(QtCore.QRect(330, 80, 64, 23))
        self.lcdNumber_2.setObjectName("lcdNumber_2")
        self.lcdNumber_3 = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber_3.setGeometry(QtCore.QRect(450, 200, 64, 23))
        self.lcdNumber_3.setObjectName("lcdNumber_3")
        self.lcdNumber_4 = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber_4.setGeometry(QtCore.QRect(200, 320, 64, 23))
        self.lcdNumber_4.setObjectName("lcdNumber_4")
        self.lcdNumber_5 = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber_5.setGeometry(QtCore.QRect(340, 320, 64, 23))
        self.lcdNumber_5.setObjectName("lcdNumber_5")
        self.lcdNumber_7 = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber_7.setGeometry(QtCore.QRect(280, 230, 64, 23))
        self.lcdNumber_7.setObjectName("lcdNumber_7")
        self.lcdNumber_1.setStyleSheet('background: grey')
        self.lcdNumber_2.setStyleSheet('background: grey')
        self.lcdNumber_3.setStyleSheet('background: grey')
        self.lcdNumber_4.setStyleSheet('background: grey')
        self.lcdNumber_5.setStyleSheet('background: grey')
        self.lcdNumber_6.setStyleSheet('background: grey')
        self.lcdNumber_7.setStyleSheet('background: grey')
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(90, 170, 67, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(220, 50, 67, 17))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(330, 50, 67, 17))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(440, 170, 67, 17))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(350, 350, 67, 17))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(200, 350, 67, 17))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(280, 160, 81, 17))
        self.label_7.setObjectName("label_7")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(100, 400, 401, 192))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 571, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Chilled"))
        self.label_2.setText(_translate("MainWindow", "Medium"))
        self.label_3.setText(_translate("MainWindow", "Sparkling"))
        self.label_4.setText(_translate("MainWindow", "Ambient"))
        self.label_5.setText(_translate("MainWindow", "Hot 1"))
        self.label_6.setText(_translate("MainWindow", "Hot 2"))
        self.label_7.setText(_translate("MainWindow", "Portioning"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Sensors"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Target"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Actual"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Error %"))
# from LED import LED

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())