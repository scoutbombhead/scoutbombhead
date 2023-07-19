"""@package updater_gui
@file updater_settings_dialog.py

@brief contains the settings dialog class

@copyright Copyright 2021 Brita GmbH. All rights reserved.
"""
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, uic
import os

'''This class inherits from QDialog and is used to display the settings dialog'''
class Settings_dialog(QtWidgets.QDialog):
    def __init__(self):
        super(Settings_dialog, self).__init__()  # Call the inherited classes __init__ method
        path = os.path.join(os.path.dirname(__file__), "settings_dialog.ui")
        loadUi(path, baseinstance=self)

        self.button_ok.pressed.connect(self.close)

