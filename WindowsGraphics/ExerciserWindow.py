from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from WindowsGraphics import Windows


class ExerciserWindow(QDialog):

    def __init__(self):
        super(ExerciserWindow, self).__init__()
        loadUi("WindowsGraphics/ExerciserWindow.ui", self)
        Windows.Windows.exerciser_window = self
        self.back_to_the_search_button.clicked.connect(self.back_to_the_search_button_function)

    @staticmethod
    def back_to_the_search_button_function():
        Windows.Windows.exerciser_window.hide()
        Windows.Windows.search_window.show()
