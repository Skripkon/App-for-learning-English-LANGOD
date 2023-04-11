from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from time import time
import Exerciser
import Word
from WindowsGraphics import Windows
from random import randint
from functools import partial


class FlashCardsModeWindow(QDialog):
    words: list[str] = []
    list_of_buttons: list[str] = []

    def __init__(self):
        super(FlashCardsModeWindow, self).__init__()
        loadUi("WindowsGraphics/FlashCardsModeWindow.ui", self)
        Windows.Windows.flashcards_mode_window = self
        for i in range(1, 7):
            self.list_of_buttons.append("var" + str(i) + "_button")
        Word.Word.current_word = self.words[-1]
        self.word_label.setText(Word.Word.get_the_meaning_of_a_word())
        self.index_of_current_word = len(self.words) - 1
        self.connect_interface_with_functions()
        self.set_variants_function()


    @staticmethod
    def exit_button_function():
        Windows.Windows.flashcards_mode_window.hide()
        Windows.Windows.exerciser_window.show()
        Windows.Windows.flashcards_mode_window.setFocus()

    def connect_interface_with_functions(self):
        self.exit_button.clicked.connect(self.exit_button_function)
        self.shuffle_button.clicked.connect(self.shuffle_button_function)
        self.right_answer_button.clicked.connect(self.right_answer_button_function)
        self.next_button.clicked.connect(self.next_button_function)
        for button in self.list_of_buttons:
            getattr(self, button).clicked.connect(partial(self.answer_button_function, button))


    def set_variants_function(self):
        set_of_words = {Word.Word.current_word}
        while len(set_of_words) < 6:
            set_of_words.add(FlashCardsModeWindow.words[randint(1, len(FlashCardsModeWindow.words) - 1)])
        set_of_words = list(set_of_words)
        for i in range(6):
            getattr(self, self.list_of_buttons[i]).setText(set_of_words[i])

    def shuffle_button_function(self):
        Exerciser.Exerciser.random_shuffle(self.words)
        Word.Word.current_word = self.words[randint(0, len(self.words) - 1)]
        self.word_label.setText(Word.Word.get_the_meaning_of_a_word())
        self.set_variants_function()
        self.set_default_colors()

    def answer_button_function(self, name_of_clicked_button):
        if getattr(self, name_of_clicked_button).text() == Word.Word.current_word:
            getattr(self, name_of_clicked_button).setStyleSheet('QPushButton {background-color: #008000}')
        else:
            getattr(self, name_of_clicked_button).setStyleSheet('QPushButton {background-color: #800000}')

    def next_button_function(self):
        self.index_of_current_word -= 1
        Word.Word.current_word = self.words[self.index_of_current_word]
        self.word_label.setText(Word.Word.get_the_meaning_of_a_word())
        self.set_variants_function()
        self.set_default_colors()

    def set_default_colors(self):
        for i in range(6):
            getattr(self, self.list_of_buttons[i]).setStyleSheet('QPushButton {selection-background-color: rgb(255, 255, 255); '
                                              'font-size:15pt; color: white;}')

    def right_answer_button_function(self):
        for button in self.list_of_buttons:
            if getattr(self, button).text() == Word.Word.current_word:
                getattr(self, button).setStyleSheet('QPushButton {background-color: #008000}')
                break
