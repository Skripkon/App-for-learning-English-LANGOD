from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtCore
import Exerciser
import Word
from WindowsGraphics import Windows


class AuditionModeWindow(QDialog):
    words: list[str] = []
    array_of_mistakes = []
    index_of_the_current_word: int
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

    def init_first_word(self):
        self.word_line.setText(self.words[-1])
        Word.Word.current_word = self.words[-1]
        self.index_of_the_current_word = len(self.words) - 1

    def connect_interface_with_functions(self):
        self.pronunciation_US.clicked.connect(Windows.Windows.play_sound_with_us_accent)
        self.pronunciation_UK.clicked.connect(Windows.Windows.play_sound_with_uk_accent)
        self.exit_button.clicked.connect(self.exit_button_function)
        self.next_button.clicked.connect(self.next_button_function)
        self.submit_button.clicked.connect(self.submit_button_function)
        self.shuffle_button.clicked.connect(self.shuffle_button_function)
        self.right_answer_button.clicked.connect(self.right_answer_button_function)

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
                self.array_of_mistakes.append(answer)
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
            self.array_of_mistakes.append(Word.Word.current_word)
        self.word_line.show()

    def shuffle_button_function(self):
        if self.type_of_order == "straight":
            self.type_of_order = "shuffled"
            Exerciser.Exerciser.random_shuffle(self.words)
            self.shuffle_button.setStyleSheet(Windows.Windows.style_sheet_for_shuffle_button_on)
            self.word_line.setText(self.words[-1])
            Word.Word.current_word = self.words[-1]
        else:
            self.type_of_order = "straight"
            wordlist: str = Windows.Windows.exerciser_window.choose_wordlist.currentText()
            self.words = Exerciser.Exerciser.dict_of_added_words[wordlist].copy()
            self.index_of_the_current_word = len(self.words) - 1
            self.word_line.setText(self.words[-1])
            self.shuffle_button.setStyleSheet(Windows.Windows.style_sheet_for_shuffle_button_off)
            Word.Word.current_word = self.words[-1]
        self.word_line.hide()
        self.wrong_answer_line.hide()
        self.input_text.clear()
        self.input_text.setStyleSheet(Windows.Windows.style_sheet_by_default)
        Windows.Windows.widget.setFocus()

    @staticmethod
    def exit_button_function():
        Windows.Windows.audition_mode_window.hide()
        Windows.Windows.exerciser_window.show()
        Windows.Windows.audition_mode_window.setFocus()

    def next_button_function(self):
        self.index_of_the_current_word -= 1
        if self.mistake_was_made == "None":
            self.array_of_mistakes.append(Word.Word.current_word)
        self.mistake_was_made = "None"
        if self.index_of_the_current_word < 0:
            action: str = Windows.Windows.open_window_after_all_words_reviewed(len(self.array_of_mistakes), len(self.words))
            if action == "break":
                self.exit_button_function()
                self.array_of_mistakes.clear()
                self.mistake_was_made = "None"
                return None
            elif action == "Learn your mistakes":
                self.words = self.array_of_mistakes.copy()
                self.index_of_the_current_word = len(self.words) - 1
                self.array_of_mistakes.clear()
                self.mistake_was_made = "None"
            else:
                self.mistake_was_made = "None"
                if self.words != Exerciser.Exerciser.array_of_words_for_exercise:
                    self.words = Exerciser.Exerciser.array_of_words_for_exercise
                self.index_of_the_current_word = len(self.words) - 1
                self.array_of_mistakes.clear()
        self.input_text.clear()
        Word.Word.current_word = self.words[self.index_of_the_current_word]
        self.wrong_answer_line.hide()
        self.input_text.setStyleSheet(Windows.Windows.style_sheet_by_default)
        Windows.Windows.widget.setFocus()
        self.word_line.setText(self.words[self.index_of_the_current_word])
        self.word_line.hide()