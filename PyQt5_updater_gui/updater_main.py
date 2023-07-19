"""@package updater_gui
@file updater_main.py

@brief GUI-Application to run the bdpctl and ubundler Tools

@copyright Copyright 2021 Brita GmbH. All rights reserved.
"""
#!/bin/bash

import PyQt5
from PyQt5.QtWidgets import *#!/bin/bash

import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, uic
import subprocess
import os
import sys
from datetime import datetime
from updater_help_dialog import Help_dialog
from updater_settings_dialog import Settings_dialog
from PyQt5 import QtMultimedia


'''This is the main window class. It contains all the widgets used in the GUI '''
class Ui(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui, self).__init__()  # Call the inherited classes __init__ method
        path = os.path.join(os.path.dirname(__file__), "updater.ui")
        loadUi(path, baseinstance=self)
        # Create the QThread object
        self.worker = Thread()
        # Create QProcess object
        self.reflash = QProcess(self)
        # Declare local variables
        self.proc = subprocess.Popen
        self.fileName = ''
        self.fileNameSet = False
        self.ubundlerPath = ""
        # Connect buttons to respective slots
        self.button_update.pressed.connect(self.on_update)
        self.button_abort_update.pressed.connect(self.on_abort_update)
        self.button_init.pressed.connect(self.on_init)
        self.button_abort_init.pressed.connect(self.on_abort_init)
        self.button_close.pressed.connect(self.close)
        self.button_help.pressed.connect(self.on_help)
        self.button_settings.pressed.connect(self.on_settings)

        # Connect the QProcess output event to respective slot
        self.reflash.readyRead.connect(self.on_reflash_output)

        # Connect QThread object signals to respective slots
        self.worker.sendString.connect(self.get_string)
        self.worker.sendProcObj.connect(self.get_proc_obj)
        self.worker.finished.connect(self.thread_finished)

        # Create QSettings Object
        self.settings = QSettings("Brita", "Updater_GUI")
        # Load the settings into local variables
        self.worker.bdpctlPath = self.settings.value("bdpctl_path")
        self.ubundlerPath = self.settings.value("ubundler_path")
        self.lastSerialNr = self.settings.value("last_serial_nr")
        self.lastSapCode = self.settings.value("last_sap_code")
        self.lastVersionNr = self.settings.value("last_version_nr")
        # Restore the GUI
        self.restore_gui()
        # Show the GUI
        self.show()

    '''This function restores the text fields with the last used parameters'''
    def restore_gui(self):
        self.lineEdit_serialNr.insert(self.settings.value("last_serial_nr"))
        self.lineEdit_sapCode.insert(self.settings.value("last_sap_code"))
        self.lineEdit_version.insert(self.settings.value("last_version_nr"))

    '''This function runs when the update button is pressed. It starts the ubundler tool.'''
    def on_update(self):
        self.button_abort_update.setEnabled(True)
        self.button_init.setEnabled(False)
        VersionNr = self.lineEdit_version.text()
        self.lastVersionNr = VersionNr
        # Update the QSettings object
        self.settings.setValue("last_version_nr", VersionNr)
        # Start QPeocess
        self.reflash.start(self.ubundlerPath + 'reflash', [VersionNr, 'latest', 'true'])
        self.console.append('Update started.')
        # Update log file
        if not self.fileNameSet:
            now = datetime.now()
            self.fileName = now.strftime("%Y-%m-%d_%H-%M-%S") + '.txt'
            self.fileNameSet = True
        logFile = open('log/' + self.fileName, 'a')
        logFile.write('Update started.\n')
        logFile.close()

    '''This function is called when the QProcess receives an output'''
    def on_reflash_output(self):
        while self.reflash.canReadLine():
            out = self.reflash.readLine()
            out = out.data().decode()
            # Edit the output data string
            strlist = out.split('\b')
            if len(strlist) > 1:
                out = strlist[0][:-5] + strlist[-1]
            else:
                out = strlist[0]
            # Update log file
            logFile = open('log/' + self.fileName, 'a')
            logFile.write(out)
            logFile.write('\n')
            logFile.close()
            self.console.append(out)
            if out == 'Device found\n':
                self.console.append(out)
            if out == 'Locked\n':
                self.console.append('Reflash done\n')
                self.console.append('Please disconnect and reconnect power source\n')
                # Play sound
                QtMultimedia.QSound.play("Chord2.wav")
                self.reflash.kill()
                self.button_init.setEnabled(True)
                self.button_abort_update.setEnabled(False)

    '''This function is called when the abort update button is pressed. It is used to abort the ubundler process'''
    def on_abort_update(self):
        self.reflash.kill()
        self.console.append('Update aborted!')
        # Update log file
        logFile = open('log/' + self.fileName, 'a')
        logFile.write('Update aborted!\n')
        logFile.close()
        self.button_abort_update.setEnabled(False)
        self.button_init.setEnabled(True)

    '''This function is called when the init button is pressed'''
    def on_init(self):
        sapCodeSet = False
        serialNrSet = False
        sapCode = ''
        serialNr = ''
        if not self.fileNameSet:
            now = datetime.now()
            self.fileName = now.strftime("%Y-%m-%d_%H-%M-%S") + '.txt'
            self.fileNameSet = True

        # Check if sapCode is entered
        if self.lineEdit_sapCode.text() is not '':
            sapCode = self.lineEdit_sapCode.text()
            sapCodeSet = True
        # Check if serial Nr. is 15 chars long
        if len(self.lineEdit_serialNr.text()) == 15:
            serialNr = self.lineEdit_serialNr.text()
            serialNrSet = True
        # If serial nr. is set start the thread
        if not sapCodeSet and serialNrSet:
            self.worker.setCodes(sapCode, serialNr)
            self.worker.start()
            self.button_abort_init.setEnabled(True)
            self.button_init.setEnabled(False)
            # Update log file
            logFile = open('log/' + self.fileName, 'a')
            logFile.write('Init started.\n')
            logFile.close()
            self.console.append('Init started.\n')
        # If serial nr. is not the required nr. of characters finish the thread
        elif sapCodeSet and not serialNrSet:
            self.console.append('Serial nr. must be 15 characters long\n')
            self.worker.finished.emit()
            self.button_update.setEnabled(True)
        # If serial nr. and SAP code is set start the thread
        elif sapCodeSet and serialNrSet:
            self.worker.setCodes(sapCode, serialNr)
            self.worker.start()
            self.button_abort_init.setEnabled(True)
            self.button_init.setEnabled(False)
            self.button_update.setEnabled(False)
            logFile = open('log/' + self.fileName, 'a')
            logFile.write('Init started.\n')
            logFile.close()
            self.console.append('Init started.\n')
            self.lastSerialNr = serialNr
            self.lastSapCode = sapCode
        # If neither are set start the thread
        else:
            self.worker.setCodes(sapCode, serialNr)
            self.worker.start()
            self.button_abort_init.setEnabled(True)
            self.lastSerialNr = ""
            self.lastSapCode = ""

    '''This function is the slot function of the signal send_string(). It us used to send the strings received from
        the QThread and send it to the QMainWindow object'''
    def get_string(self, mystr):

        # Print string to console
        self.console.append(mystr)
        # Update log file
        logFile = open('log/' + self.fileName, 'a')
        logFile.write(mystr)
        logFile.close()
        if mystr == '':
            self.console.append('Update successful\n')
            # stop thread
            self.worker.finished.emit()
        elif str == 'Timeout':
            # stop thread
            self.worker.finished.emit()
        else:
            # stop thread
            self.worker.finished.emit()

    '''This function is used to send the subprocess.Popen object to the QMainWindow object. So that the process 
      can be killed in the QMainWindow thread'''
    def get_proc_obj(self, proc):
        self.proc = proc

    '''This function is called when the abort init button is pressed. It is used to abort the bdpctl process'''
    def on_abort_init(self):
        # Kill thread
        self.worker.terminate()
        # Update log file
        logFile = open('log/' + self.fileName, 'a')
        logFile.write('Init aborted!\n')
        logFile.close()
        self.console.append('Init aborted!\n')
        self.button_abort_init.setEnabled(False)
        self.button_init.setEnabled(True)
        self.button_update.setEnabled(True)

    '''This funciton is called when the thread finishes'''
    def thread_finished(self):
        QtMultimedia.QSound.play("Chord2.wav")
        self.button_abort_init.setEnabled(False)
        self.button_update.setEnabled(True)
        self.button_init.setEnabled(True)

    '''This function is called when the Help button is pressed. Opens a help dialog window'''
    def on_help(self):
        # Create and show QDialog object
        helpDialog = Help_dialog()
        helpDialog.show()
        helpDialog.exec_()

    '''This function is called when the Settings button is pressed. Opens a settings dialog window'''
    def on_settings(self):
        # Create and show QDialog object
        settingsDialog = Settings_dialog()
        # Display current Settings from the QSettings object
        settingsDialog.lineEdit.insert(self.settings.value("ubundler_path"))
        settingsDialog.lineEdit_2.insert(self.settings.value("bdpctl_path"))
        settingsDialog.show()
        settingsDialog.exec_()
        # Update the QSettings object with the text field of QDialog
        self.settings.setValue("ubundler_path", settingsDialog.lineEdit.text())
        self.settings.setValue("bdpctl_path", settingsDialog.lineEdit_2.text())
        self.ubundlerPath = self.settings.value('ubundler_path')
        self.worker.setPath(self.settings.value('bdpctl_path'))

    '''This function is called when the close button is pressed. It updates the last used parameters and tool paths
    to the QSettings object'''
    def closeEvent(self, event):
        self.settings.setValue('ubundler_path', self.ubundlerPath)
        self.settings.setValue('bdpctl_path', self.worker.bdpctlPath)
        self.settings.setValue('last_serial_nr', self.lastSerialNr)
        self.settings.setValue('last_sap_code', self.lastSapCode)
        self.settings.setValue('last_version_nr', self.lastVersionNr)

'''This is class inherits from the QThread class. It is used to create a custon QThread object'''
class Thread(QThread):

    # Declare signal objects
    finished = pyqtSignal()
    sendString = pyqtSignal(str)
    sendProcObj = pyqtSignal(subprocess.Popen)

    # This method is used to get the parameters from the QMainWindow object and save them to local variables
    def setCodes(self, sapCode, serialNr):
        self.sapCode = sapCode
        self.serialNr = serialNr

    # This method is used to get the bdpctl tool path from the QMainWindow object
    def setPath(self, bdpctlPath):
        self.bdpctlPath = bdpctlPath

    # Init method
    def __init__(self):
        super(Thread, self).__init__()
        # declare local variables
        self.sapCode = 0
        self.serialNr = 0
        self.bdpctlPath = ''

    # This method is called when the start() method in the thread object is called
    def run(self):
        my_env = os.environ.copy()
        cmd = self.bdpctlPath + 'bdpctl eolp init --sc ' + self.sapCode + ' --sn ' + self.serialNr
        # run the subprocess
        proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True,
                                env=my_env)
        # save output to variable
        out = proc.stdout.read()
        # trigger signals
        self.sendString.emit(out)
        self.sendProcObj.emit(proc)

"""This is the main function"""
def main():
    app = QApplication([])
    window = Ui()
    reflash = QProcess(window)
    app.exec_()


if __name__ == '__main__':
    main()
