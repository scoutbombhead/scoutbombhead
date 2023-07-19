"""@package updater_gui
@file updater_help_dialog.py

@brief contains the help dialog class

@copyright Copyright 2021 Brita GmbH. All rights reserved.
"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
# noinspection PyUnresolvedReferences
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, uic
import os

'''This class inherits from QDialog'''
class Help_dialog(QtWidgets.QDialog):
    def __init__(self):
        super(Help_dialog, self).__init__()  # Call the inherited classes __init__ method
        # uic.loadUi('updater_ver_2.ui', self)  # Load the .ui file
        path = os.path.join(os.path.dirname(__file__), "help_dialog.ui")
        loadUi(path, baseinstance=self)

        self.button_close.pressed.connect(self.close)

