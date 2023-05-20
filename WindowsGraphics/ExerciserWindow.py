from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets

import Exerciser
from WindowsGraphics import Windows, RevisionModeWindow, FlashCardsModeWindow, ContextModeWindow


class ExerciserWindow(QDialog):

    def __init__(self):
        super(ExerciserWindow, self).__init__()
        loadUi("WindowsGraphics/ExerciserWindow.ui", self)
        self.back_to_the_search_button.clicked.connect(self.back_to_the_search_button_function)
        self.revision_mode_button.clicked.connect(self.revision_mode_button_function)
        self.flashcards_mode_button.clicked.connect(self.flashcards_mode_button_function)
        self.context_mode_button.clicked.connect(self.context_mode_window_button_function)
        Windows.Windows.exerciser_window = self
        self.choose_wordlist.currentTextChanged.connect(self.currentTextChangedFunction)

    def currentTextChangedFunction(self):
        new_wordlist: str = self.choose_wordlist.currentText()
        if new_wordlist == "":
            return None
        Exerciser.Exerciser.array_of_words_for_exercise = Exerciser.Exerciser.dict_of_added_words[new_wordlist]

    @staticmethod
    def back_to_the_search_button_function():
        Windows.Windows.exerciser_window.hide()
        Windows.Windows.search_window.show()
        Windows.Windows.widget.setFocus()

    @staticmethod
    def revision_mode_button_function():
        RevisionModeWindow.RevisionModeWindow.words = Exerciser.Exerciser.array_of_words_for_exercise.copy()
        Windows.Windows.exerciser_window.hide()
        if Windows.Windows.revision_mode_window is None:
            RevisionModeWindow.RevisionModeWindow()
            Windows.Windows.widget.addWidget(Windows.Windows.revision_mode_window)
            Windows.Windows.widget.setCurrentIndex(Windows.Windows.widget.currentIndex() + 1)
        Windows.Windows.revision_mode_window.init_first_word()
        Windows.Windows.revision_mode_window.show()
        Windows.Windows.widget.setFocus()

    @staticmethod
    def flashcards_mode_button_function():
        FlashCardsModeWindow.FlashCardsModeWindow.words = Exerciser.Exerciser.array_of_words_for_exercise.copy()
        Windows.Windows.exerciser_window.hide()
        if Windows.Windows.flashcards_mode_window is None:
            FlashCardsModeWindow.FlashCardsModeWindow()
            Windows.Windows.widget.addWidget(Windows.Windows.flashcards_mode_window)
            Windows.Windows.widget.setCurrentIndex(Windows.Windows.widget.currentIndex() + 1)
        Windows.Windows.flashcards_mode_window.init_first_word()
        Windows.Windows.flashcards_mode_window.show()
        Windows.Windows.widget.setFocus()

    @staticmethod
    def context_mode_window_button_function():
        ContextModeWindow.ContextModeWindow.words = Exerciser.Exerciser.array_of_words_for_exercise.copy()
        Windows.Windows.exerciser_window.hide()
        if Windows.Windows.context_mode_window is None:
            ContextModeWindow.ContextModeWindow()
            Windows.Windows.widget.addWidget(Windows.Windows.context_mode_window)
            Windows.Windows.widget.setCurrentIndex(Windows.Windows.widget.currentIndex() + 1)
        Windows.Windows.context_mode_window.init_first_word()
        Windows.Windows.context_mode_window.show()
        Windows.Windows.widget.setFocus()
