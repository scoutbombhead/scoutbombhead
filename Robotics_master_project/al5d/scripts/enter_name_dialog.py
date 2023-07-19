"""@package updater_gui
@file enter_name_dialog.py

@copyright Copyright 2021 Brita GmbH. All rights reserved.
"""
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, uic
import os

'''This class inherits from QDialog and is used to display the settings dialog'''


class enterNameDialog(QtWidgets.QDialog):
    def __init__(self):
        super(enterNameDialog, self).__init__()  # Call the inherited classes __init__ method
        path = os.path.join(os.path.dirname(__file__), "enter_name_dialog.ui")
        loadUi(path, baseinstance=self)

        # self.button_ok.pressed.connect(self.close)
