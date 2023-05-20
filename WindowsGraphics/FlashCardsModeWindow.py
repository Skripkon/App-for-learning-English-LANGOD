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
    style_sheet_for_option: str = "selection-background-color: rgb(255, 255, 255);" \
                                  "border-style: outset;" \
                                  "border-width: 1px;" \
                                  "border-radius: 15px;" \
                                  "border-color: black;" \
                                  "padding: 4px;"

    style_sheet_after_correct_answer = 'background-color:rgb(205, 247, 190); ' \
                                       'font: 19pt \"Yrsa\"; color:black;' + style_sheet_for_option
    style_sheet_after_wrong_answer = 'background-color:rgb(255, 192, 192); ' \
                                     'font: 19pt \"Yrsa\"; color:black;' + style_sheet_for_option
    style_sheet_by_default = 'background-color:rgb(30, 85, 138); ' \
                             'font: 19pt \"Yrsa\"; color:white;' + style_sheet_for_option

    def __init__(self):
        super(FlashCardsModeWindow, self).__init__()
        loadUi("WindowsGraphics/FlashCardsModeWindow.ui", self)
        Windows.Windows.flashcards_mode_window = self
        for i in range(1, 7):
            self.list_of_buttons.append("var" + str(i) + "_button")
        Word.Word.current_word = self.words[-1]
        self.word_label.setText(Word.Word.get_the_meaning_of_a_word())
        self.index_of_the_current_word = len(self.words) - 1
        self.connect_interface_with_functions()
        self.set_variants_function()
        self.type_of_order = "straight"
        self.word_label.setReadOnly(True)

    @staticmethod
    def exit_button_function():
        # Exerciser.Exerciser.array_of_words_for_exercise.clear()
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
        self.index_of_the_current_word = len(self.words) - 1
        self.set_default_colors()
        if self.type_of_order == "straight":
            self.type_of_order = "shuffled"
            Exerciser.Exerciser.random_shuffle(self.words)
            self.shuffle_button.setStyleSheet('QPushButton {selection-background-color: rgb(255, 255, 255); '
                                              'font-size:15pt; color: yellow;}')
        else:
            self.type_of_order = "straight"
            wordlist: str = Windows.Windows.exerciser_window.choose_wordlist.currentText()
            self.words = Exerciser.Exerciser.dict_of_added_words[wordlist].copy()
            self.shuffle_button.setStyleSheet('QPushButton {selection-background-color: rgb(255, 255, 255); '
                                              'font-size:15pt; color: white;}')

        Word.Word.current_word = self.words[-1]
        self.word_label.setText(Word.Word.get_the_meaning_of_a_word())
        self.word_label.verticalScrollBar().setValue(0)
        self.set_variants_function()
        Windows.Windows.flashcards_mode_window.setFocus()

    def answer_button_function(self, name_of_clicked_button):
        if getattr(self, name_of_clicked_button).text() == Word.Word.current_word:
            getattr(self, name_of_clicked_button).setStyleSheet(self.style_sheet_after_correct_answer)
        else:
            getattr(self, name_of_clicked_button).setStyleSheet(self.style_sheet_after_wrong_answer)
        Windows.Windows.flashcards_mode_window.setFocus()

    def next_button_function(self):
        self.index_of_the_current_word -= 1
        if self.index_of_the_current_word < 0:
            Windows.Windows.open_the_window("A study completed!",
                                            "You went over all of your words!\nCongratulations!\n"
                                            "You might review your words one more time or try other mods!")
            self.index_of_the_current_word = len(self.words) - 1
        Word.Word.current_word = self.words[self.index_of_the_current_word]
        self.word_label.setText(Word.Word.get_the_meaning_of_a_word())
        self.word_label.verticalScrollBar().setValue(0)
        self.set_variants_function()
        self.set_default_colors()
        Windows.Windows.flashcards_mode_window.setFocus()

    def keyPressEvent(self, event):
        if event.nativeScanCode() == 36:  # button ESC pressed
            self.next_button_function()

    def set_default_colors(self):
        for i in range(6):
            getattr(self, self.list_of_buttons[i]).setStyleSheet(self.style_sheet_by_default)

    def right_answer_button_function(self):
        for button in self.list_of_buttons:
            if getattr(self, button).text() == Word.Word.current_word:
                getattr(self, button).setStyleSheet(self.style_sheet_after_correct_answer)
                break
        Windows.Windows.flashcards_mode_window.setFocus()
