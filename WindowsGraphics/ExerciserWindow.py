from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets

import Exerciser
from WindowsGraphics import Windows, RevisionModeWindow, FlashCardsModeWindow


class ExerciserWindow(QDialog):

    def __init__(self):
        super(ExerciserWindow, self).__init__()
        loadUi("WindowsGraphics/ExerciserWindow.ui", self)
        self.back_to_the_search_button.clicked.connect(self.back_to_the_search_button_function)
        self.revision_mode_button.clicked.connect(self.revision_mode_button_function)
        self.flashcards_mode_button.clicked.connect(self.flashcards_mode_button_function)
        Windows.Windows.exerciser_window = self

    @staticmethod
    def back_to_the_search_button_function():
        Windows.Windows.exerciser_window.hide()
        Windows.Windows.search_window.show()
        Windows.Windows.widget.setFocus()

    @staticmethod
    def revision_mode_button_function():
        RevisionModeWindow.RevisionModeWindow.words = Exerciser.Exerciser.array_of_added_words.copy()
        Windows.Windows.exerciser_window.hide()
        if Windows.Windows.revision_mode_window is None:
            RevisionModeWindow.RevisionModeWindow()
            Windows.Windows.widget.addWidget(Windows.Windows.revision_mode_window)
            Windows.Windows.widget.setCurrentIndex(Windows.Windows.widget.currentIndex() + 1)
        Windows.Windows.revision_mode_window.show()
        Windows.Windows.widget.setFocus()


    @staticmethod
    def flashcards_mode_button_function():
        FlashCardsModeWindow.FlashCardsModeWindow.words = Exerciser.Exerciser.array_of_added_words.copy()
        Windows.Windows.exerciser_window.hide()
        if Windows.Windows.flashcards_mode_window is None:
            FlashCardsModeWindow.FlashCardsModeWindow()
            Windows.Windows.widget.addWidget(Windows.Windows.flashcards_mode_window)
            Windows.Windows.widget.setCurrentIndex(Windows.Windows.widget.currentIndex() + 1)
        else:
            FlashCardsModeWindow.FlashCardsModeWindow.set_default_colors(Windows.Windows.flashcards_mode_window)
        Windows.Windows.flashcards_mode_window.show()
        Windows.Windows.widget.setFocus()

