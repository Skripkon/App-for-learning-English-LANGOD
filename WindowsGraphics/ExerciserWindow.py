from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
import Exerciser
from WindowsGraphics import Windows, RevisionModeWindow, FlashCardsModeWindow, ContextModeWindow, AuditionModeWindow


class ExerciserWindow(QDialog):

    def __init__(self):
        super(ExerciserWindow, self).__init__()
        loadUi("WindowsGraphics/ExerciserWindow.ui", self)
        self.back_to_the_search_button.clicked.connect(self.back_to_the_search_button_function)
        self.revision_mode_button.clicked.connect(self.revision_mode_button_function)
        self.flashcards_mode_button.clicked.connect(self.flashcards_mode_button_function)
        self.context_mode_button.clicked.connect(self.context_mode_window_button_function)
        self.audition_mode_button.clicked.connect(self.audition_mode_window_button_function)
        Windows.Windows.exerciser_window = self

    @staticmethod
    def back_to_the_search_button_function():
        Windows.Windows.exerciser_window.hide()
        Windows.Windows.search_window.show()
        Windows.Windows.widget.setFocus()

    @staticmethod
    def revision_mode_button_function():
        Windows.Windows.exerciser_window.hide()
        RevisionModeWindow.RevisionModeWindow()
        Windows.Windows.widget.addWidget(Windows.Windows.revision_mode_window)
        Windows.Windows.widget.setCurrentIndex(Windows.Windows.widget.currentIndex() + 1)
        Windows.Windows.revision_mode_window.init_first_word()
        Windows.Windows.revision_mode_window.show()
        Windows.Windows.widget.setFocus()

    @staticmethod
    def flashcards_mode_button_function():
        FlashCardsModeWindow.FlashCardsModeWindow.words = Exerciser.Exerciser.words_for_exercise.copy()
        Windows.Windows.exerciser_window.hide()
        FlashCardsModeWindow.FlashCardsModeWindow()
        Windows.Windows.widget.addWidget(Windows.Windows.flashcards_mode_window)
        Windows.Windows.widget.setCurrentIndex(Windows.Windows.widget.currentIndex() + 1)
        Windows.Windows.flashcards_mode_window.init_first_word()
        Windows.Windows.flashcards_mode_window.show()
        Windows.Windows.widget.setFocus()

    @staticmethod
    def context_mode_window_button_function():
        ContextModeWindow.ContextModeWindow.words = Exerciser.Exerciser.words_for_exercise.copy()
        Windows.Windows.exerciser_window.hide()
        ContextModeWindow.ContextModeWindow()
        Windows.Windows.widget.addWidget(Windows.Windows.context_mode_window)
        Windows.Windows.widget.setCurrentIndex(Windows.Windows.widget.currentIndex() + 1)
        Windows.Windows.context_mode_window.init_first_word()
        Windows.Windows.context_mode_window.show()
        Windows.Windows.widget.setFocus()

    @staticmethod
    def audition_mode_window_button_function():
        AuditionModeWindow.AuditionModeWindow.words = Exerciser.Exerciser.words_for_exercise.copy()
        Windows.Windows.exerciser_window.hide()
        AuditionModeWindow.AuditionModeWindow()
        Windows.Windows.widget.addWidget(Windows.Windows.audition_mode_window)
        Windows.Windows.widget.setCurrentIndex(Windows.Windows.widget.currentIndex() + 1)
        Windows.Windows.audition_mode_window.init_first_word()
        Windows.Windows.audition_mode_window.show()
        Windows.Windows.widget.setFocus()
