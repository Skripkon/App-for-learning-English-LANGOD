from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
import Exerciser
import Word
from WindowsGraphics import Windows
from random import randint
from functools import partial


class FlashCardsModeWindow(QDialog):
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
    first_answer = "None"  # unless you give any answer
    # other values of "first_answer" are "Right" and "Wrong"

    def __init__(self):
        super(FlashCardsModeWindow, self).__init__()
        loadUi("WindowsGraphics/FlashCardsModeWindow.ui", self)
        Windows.Windows.flashcards_mode_window = self
        for i in range(1, 7):
            self.list_of_buttons.append("var" + str(i) + "_button")
        self.connect_interface_with_functions()
        self.type_of_order = "straight"
        self.word_label.setReadOnly(True)
        self.init_first_word()

    def init_first_word(self):
        Windows.Windows.initialization_after_mode_was_opened()
        self.display_current_word()

    @staticmethod
    def exit_button_function():
        Windows.Windows.exit_button_function("flashcards_mode_window")

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
            set_of_words.add(FlashCardsModeWindow.words[randint(0, len(FlashCardsModeWindow.words) - 1)])
        set_of_words = list(set_of_words)
        for i in range(6):
            getattr(self, self.list_of_buttons[i]).setText(set_of_words[i])

    def display_current_word(self):
        self.set_default_colors()
        self.word_label.setText(Word.Word.get_the_meaning_of_a_word())
        self.word_label.verticalScrollBar().setValue(0)
        self.set_variants_function()

    @staticmethod
    def shuffle_button_function(self):
        Windows.Windows.shuffle_button_function("flashcards_mode_window")

    def answer_button_function(self, name_of_clicked_button):
        answer: str = getattr(self, name_of_clicked_button).text()
        if answer == Word.Word.current_word:
            getattr(self, name_of_clicked_button).setStyleSheet(self.style_sheet_after_correct_answer)
            if self.first_answer == "None":
                self.first_answer = "Right"
        else:
            if self.first_answer == "Right":
                pass
            elif self.first_answer == "Wrong":
                pass
            elif self.first_answer == "None":
                self.first_answer = "Wrong"
                Exerciser.Exerciser.array_of_mistakes.append(Exerciser.Exerciser.words_for_exercise[Exerciser.Exerciser.index_of_the_current_word])
            getattr(self, name_of_clicked_button).setStyleSheet(self.style_sheet_after_wrong_answer)
        Windows.Windows.flashcards_mode_window.setFocus()

    def next_button_function(self):
        Exerciser.Exerciser.index_of_the_current_word -= 1
        if self.first_answer == "None":
            Exerciser.Exerciser.array_of_mistakes.append(Word.Word.current_word)
        self.first_answer = "None"
        if Exerciser.Exerciser.index_of_the_current_word < 0:
            action: str = Windows.Windows.open_window_after_all_words_reviewed()
            if action == "break":
                self.exit_button_function()
                Exerciser.Exerciser.array_of_mistakes.clear()
                self.first_answer = "None"
                return None
            elif action == "Learn your mistakes":
                Exerciser.Exerciser.words_for_exercise = Exerciser.Exerciser.array_of_mistakes.copy()
                Exerciser.Exerciser.index_of_the_current_word = len(Exerciser.Exerciser.words_for_exercise) - 1
                Exerciser.Exerciser.array_of_mistakes.clear()
                self.first_answer = None
            else:
                self.first_answer = "None"
                if Exerciser.Exerciser.words_for_exercise != Exerciser.Exerciser.words_for_exercise:
                    Exerciser.Exerciser.words_for_exercise = Exerciser.Exerciser.words_for_exercise
                Exerciser.Exerciser.index_of_the_current_word = len(Exerciser.Exerciser.words_for_exercise) - 1
                Exerciser.Exerciser.array_of_mistakes.clear()
        Word.Word.current_word = Exerciser.Exerciser.words_for_exercise[Exerciser.Exerciser.index_of_the_current_word]
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
        if self.first_answer == "None":
            Exerciser.Exerciser.array_of_mistakes.append(Exerciser.Exerciser.words_for_exercise[Exerciser.Exerciser.index_of_the_current_word])
            self.first_answer = "Wrong"
        Windows.Windows.flashcards_mode_window.setFocus()