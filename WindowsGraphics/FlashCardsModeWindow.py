from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from time import time
import Exerciser
import Word
from WindowsGraphics import Windows
from random import randint


class FlashCardsModeWindow(QDialog):
    words: list[str] = []

    def __init__(self):
        super(FlashCardsModeWindow, self).__init__()
        loadUi("WindowsGraphics/FlashCardsModeWindow.ui", self)
        Windows.Windows.flashcards_mode_window = self
        Word.Word.current_word = self.words[-1]
        self.word_label.setText(Word.Word.get_the_meaning_of_a_word())
        self.index_of_current_word = len(self.words) - 1
        self.set_variants_button()
        self.connect_interface_with_functions()

    @staticmethod
    def exit_button_function():
        Windows.Windows.flashcards_mode_window.hide()
        Windows.Windows.exerciser_window.show()
        Windows.Windows.revision_mode_window.setFocus()

    def connect_interface_with_functions(self):
        self.exit_button.clicked.connect(self.exit_button_function)
        self.shuffle_button.clicked.connect(self.shuffle_button_function)

    def set_variants_button(self):
        splitter: int = (len(self.words) - 1) // 6
        index: int = 0
        self.var1_button.setText(self.words[randint(splitter * index, splitter * (index + 1))])
        index += 1
        self.var2_button.setText(self.words[randint(splitter * index + 1, splitter * (index + 1))])
        index += 1
        self.var3_button.setText(self.words[randint(splitter * index + 1, splitter * (index + 1))])
        index += 1
        self.var4_button.setText(self.words[randint(splitter * index + 1, splitter * (index + 1))])
        index += 1
        self.var5_button.setText(self.words[randint(splitter * index + 1, splitter * (index + 1))])
        index += 1
        self.var6_button.setText(self.words[randint(splitter * index + 1, splitter * (index + 1))])
        correct: int = randint(1, 6)
        if correct == 1:
            self.var1_button.setText(Word.Word.current_word)
        elif correct == 2:
            self.var2_button.setText(Word.Word.current_word)
        elif correct == 2:
            self.var3_button.setText(Word.Word.current_word)
        elif correct == 4:
            self.var4_button.setText(Word.Word.current_word)
        elif correct == 5:
            self.var5_button.setText(Word.Word.current_word)
        else:
            self.var6_button.setText(Word.Word.current_word)

    @staticmethod
    def swap(a: str, b: str):
        tmp = a
        a = b
        b = tmp

    def shuffle_button_function(self):
        for i in range(len(self.words)):
            self.swap(self.words[i], self.words[randint(0, i)])
        Word.Word.current_word = self.words[randint(0, len(self.words) - 1)]
        self.word_label.setText(Word.Word.get_the_meaning_of_a_word())
        self.set_variants_button()
