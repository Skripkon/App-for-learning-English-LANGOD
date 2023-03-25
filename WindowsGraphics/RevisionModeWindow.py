from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from WindowsGraphics import Windows


class RevisionModeWindow(QDialog):
    def __init__(self):
        super(RevisionModeWindow, self).__init__()
        loadUi("WindowsGraphics/RevisionModeWindow.ui", self)
        Windows.Windows.revision_mode_window = self
        # self.back_to_the_search_button.clicked.connect(self.back_to_the_search_button_function)

