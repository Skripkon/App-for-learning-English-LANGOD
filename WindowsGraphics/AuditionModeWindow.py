import time

from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtCore
import Exerciser
import Word
from WindowsGraphics import Windows


class AuditionModeWindow(QDialog):
    mistake_was_made = "None"

    def __init__(self):
        super(AuditionModeWindow, self).__init__()
        loadUi("WindowsGraphics/AuditionModeWindow.ui", self)
        Windows.Windows.audition_mode_window = self
        self.pronunciation_US.setIconSize(QtCore.QSize(90, 90))
        self.pronunciation_UK.setIconSize(QtCore.QSize(90, 90))
        self.pronunciation_US.setIcon(QIcon("WindowsGraphics/icon_of_a_sound_button.png"))
        self.pronunciation_UK.setIcon(QIcon("WindowsGraphics/icon_of_a_sound_button.png"))
        self.connect_interface_with_functions()
        self.type_of_order = "straight"
        self.word_line.hide()
        self.wrong_answer_line.hide()
        self.init_first_word()

    def init_first_word(self):
        Windows.Windows.initialization_after_mode_was_opened()
        self.word_line.setText(Exerciser.Exerciser.words_for_exercise[-1])

    def connect_interface_with_functions(self):
        self.pronunciation_US.clicked.connect(self.us_pronunciation)
        self.pronunciation_UK.clicked.connect(self.uk_pronunciation)
        self.exit_button.clicked.connect(self.exit_button_function)
        self.next_button.clicked.connect(self.next_button_function)
        self.submit_button.clicked.connect(self.submit_button_function)
        self.shuffle_button.clicked.connect(self.shuffle_button_function)
        self.right_answer_button.clicked.connect(self.right_answer_button_function)

    def us_pronunciation(self):
        Windows.Windows.play_sound_with_us_accent()
        self.input_text.setFocus()

    def uk_pronunciation(self):
        Windows.Windows.play_sound_with_uk_accent()
        self.input_text.setFocus()

    def submit_button_function(self):
        answer: str = self.input_text.text()
        if answer == Word.Word.current_word:
            self.word_line.show()
            self.wrong_answer_line.hide()
            self.input_text.setStyleSheet(Windows.Windows.style_sheet_after_correct_answer)
            if self.mistake_was_made == "None":
                self.mistake_was_made = "False"
        else:
            if self.mistake_was_made == "None":
                Exerciser.Exerciser.array_of_mistakes.append(answer)
                self.mistake_was_made = "True"
            self.wrong_answer_line.show()
            self.input_text.setStyleSheet(Windows.Windows.style_sheet_after_wrong_answer)
        Windows.Windows.widget.setFocus()

    def right_answer_button_function(self):
        self.wrong_answer_line.hide()
        self.input_text.setText(Word.Word.current_word)
        self.input_text.setStyleSheet(Windows.Windows.style_sheet_after_correct_answer)
        Windows.Windows.widget.setFocus()
        if self.mistake_was_made == "None":
            self.mistake_was_made = "True"
            Exerciser.Exerciser.array_of_mistakes.append(Word.Word.current_word)
        self.word_line.show()

    def display_current_word(self):
        self.word_line.hide()
        self.wrong_answer_line.hide()
        self.input_text.clear()
        self.input_text.setStyleSheet(Windows.Windows.style_sheet_by_default)

    @staticmethod
    def shuffle_button_function():
        Windows.Windows.shuffle_button_function("audition_mode_window")

    @staticmethod
    def exit_button_function():
        Windows.Windows.exit_button_function("audition_mode_window")

    def next_button_function(self):
        Exerciser.Exerciser.index_of_the_current_word -= 1
        if self.mistake_was_made == "None":
            Exerciser.Exerciser.array_of_mistakes.append(Word.Word.current_word)
        self.mistake_was_made = "None"
        if Exerciser.Exerciser.index_of_the_current_word < 0:
            action: str = Windows.Windows.open_window_after_all_words_reviewed()
            if action == "break":
                self.exit_button_function()
                Exerciser.Exerciser.array_of_mistakes.clear()
                self.mistake_was_made = "None"
                return None
            elif action == "Learn your mistakes":
                Exerciser.Exerciser.words_for_exercise = Exerciser.Exerciser.array_of_mistakes.copy()
                Exerciser.Exerciser.index_of_the_current_word = len(Exerciser.Exerciser.words_for_exercise) - 1
                Exerciser.Exerciser.array_of_mistakes.clear()
                self.mistake_was_made = "None"
            else:
                self.mistake_was_made = "None"
                if Exerciser.Exerciser.words_for_exercise != Exerciser.Exerciser.words_for_exercise:
                    Exerciser.Exerciser.words_for_exercise = Exerciser.Exerciser.words_for_exercise
                Exerciser.Exerciser.index_of_the_current_word = len(Exerciser.Exerciser.words_for_exercise) - 1
                Exerciser.Exerciser.array_of_mistakes.clear()
        self.input_text.clear()
        Word.Word.current_word = Exerciser.Exerciser.words_for_exercise[Exerciser.Exerciser.index_of_the_current_word]
        self.wrong_answer_line.hide()
        self.input_text.setStyleSheet(Windows.Windows.style_sheet_by_default)
        Windows.Windows.widget.setFocus()
        self.word_line.setText(Exerciser.Exerciser.words_for_exercise[Exerciser.Exerciser.index_of_the_current_word])
        self.word_line.hide()
        Windows.Windows.play_sound_with_us_accent()

    def keyPressEvent(self, event):
        if event.nativeScanCode() == 36:  # button Enter pressed
            self.submit_button_function()