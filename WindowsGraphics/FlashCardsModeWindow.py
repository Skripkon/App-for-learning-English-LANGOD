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

    def __init__(self):
        super(FlashCardsModeWindow, self).__init__()
        loadUi("WindowsGraphics/FlashCardsModeWindow.ui", self)
        Windows.Windows.flashcards_mode_window = self
        Word.Word.current_word = self.words[-1]
        self.word_label.setText(Word.Word.get_the_meaning_of_a_word())
        self.index_of_current_word = len(self.words) - 1
        self.set_variants_function()
        self.connect_interface_with_functions()

    @staticmethod
    def exit_button_function():
        Windows.Windows.flashcards_mode_window.hide()
        Windows.Windows.exerciser_window.show()
        Windows.Windows.revision_mode_window.setFocus()

    def connect_interface_with_functions(self):
        self.exit_button.clicked.connect(self.exit_button_function)
        self.shuffle_button.clicked.connect(self.shuffle_button_function)
        list_of_buttons = []
        for i in range(1, 7):
            list_of_buttons.append("var" + str(i) + "_button")
        for button in list_of_buttons:
            getattr(self, button).clicked.connect(partial(self.answer_button_function, button))

    def set_variants_function(self):
        set_of_words = {Word.Word.current_word}
        while len(set_of_words) < 6:
            set_of_words.add(FlashCardsModeWindow.words[randint(1, len(FlashCardsModeWindow.words) - 1)])
        set_of_words = list(set_of_words)
        list_of_buttons = []
        for i in range(1, 7):
            list_of_buttons.append("var" + str(i) + "_button")
        for i in range(6):
            getattr(self, list_of_buttons[i]).setText(set_of_words[i])

    def shuffle_button_function(self):
        Exerciser.Exerciser.random_shuffle(self.words)
        Word.Word.current_word = self.words[randint(0, len(self.words) - 1)]
        self.word_label.setText(Word.Word.get_the_meaning_of_a_word())
        self.set_variants_function()

    def answer_button_function(self, name_of_clicked_button):
        if getattr(self, name_of_clicked_button).text() == Word.Word.current_word:
            getattr(self, name_of_clicked_button).setStyleSheet('QPushButton {background-color: #008000}')
            self.next_partion_of_words()
        else:
            getattr(self, name_of_clicked_button).setStyleSheet('QPushButton {background-color: #800000}')

    def next_partion_of_words(self):
        self.index_of_current_word -= 1
        Word.Word.current_word = self.words[self.index_of_current_word]
        self.word_label.setText(Word.Word.get_the_meaning_of_a_word())
        self.set_variants_function()
        self.set_default_colors()

    def set_default_colors(self):
        list_of_buttons = []
        for i in range(1, 7):
            list_of_buttons.append("var" + str(i) + "_button")
        for i in range(6):
            getattr(self, list_of_buttons[i]).setStyleSheet('QPushButton {selection-background-color: rgb(255, 255, 255); '
                                              'font-size:15pt; color: white;}')
