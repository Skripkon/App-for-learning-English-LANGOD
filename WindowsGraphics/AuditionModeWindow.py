from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from time import time
import Exerciser
import Word
from WindowsGraphics import Windows


class AuditionModeWindow(QDialog):
    words: list[str] = []
    current_hint_index = 1
    type_of_order = "straight"
    index_of_the_current_word: int
    style_sheet_for_input_field: str = 'font: 19pt "Yrsa";' \
                                       'color:black;' \
                                       'selection-background-color:' \
                                       'rgb(255, 255, 255);' \
                                       'border-style: outset;' \
                                       'border-width: 1px;' \
                                       'border-radius: 15px;' \
                                       'border-color: black;' \
                                       'padding: 4px;' \
                                       'selection-color: rgb(101, 145, 232);'
    style_sheet_after_correct_answer = 'background-color:rgb(205, 247, 190);' + style_sheet_for_input_field
    style_sheet_by_default = 'background-color:rgb(200, 211, 223);' + style_sheet_for_input_field
    style_sheet_after_wrong_answer = 'background-color:rgb(255, 192, 192);' + style_sheet_for_input_field
    array_of_mistakes: list[str] = []
    mistake_was_made: str = "None"  # other values of this variable are "True" and "False"

    def __init__(self):
        super(AuditionModeWindow, self).__init__()
        loadUi("WindowsGraphics/AuditionModeWindow.ui", self)
        self.wrong_answer_line.hide()
        self.pronunciation_US.setIcon(QIcon("WindowsGraphics/voiceButtonIcon.png"))
        self.pronunciation_UK.setIcon(QIcon("WindowsGraphics/voiceButtonIcon.png"))
        self.connect_interface_with_functions()

    def connect_interface_with_functions(self):
        self.exit_button.clicked.connect(self.exit_button_function)
        self.hint_button.clicked.connect(self.hint_button_function)
        self.pronunciation_UK.clicked.connect(self.pronunciation_UK_function)
        self.pronunciation_UK.clicked.connect(self.pronunciation_US_function)
        self.shuffle_button.clicked.connect(self.shuffle_button_function)
        self.submit_button.clicked.connect(self.submit_button_function)
        self.next_button.clicked.connect(self.next_button_function)

    @staticmethod
    def exit_button_function():
        Windows.Windows.audition_mode_window.hide()
        Windows.Windows.exerciser_window.show()
        Windows.Windows.audition_mode_window.setFocus()

    def hint_button_function(self):
        if self.mistake_was_made == "None":
            self.mistake_was_made = "True"
            self.array_of_mistakes.append(Word.Word.current_word)
        if self.input_text.text() == Word.Word.current_word:
            self.input_text.setStyleSheet(self.style_sheet_after_correct_answer)
            self.show_pronunciation_buttons()
            return None
        self.wrong_answer_line.hide()
        self.input_text.setStyleSheet(self.style_sheet_by_default)
        if self.current_hint_index == 0:
            self.input_text.setText(Word.Word.current_word[0:self.current_hint_index])
        else:
            if len(self.input_text.text()) < len(Word.Word.current_word):
                IsPrefixTheSame: bool = True
                for i in range(0, len(self.input_text.text())):
                    if self.input_text.text()[i] != Word.Word.current_word[i]:
                        IsPrefixTheSame = False
                        break
                if IsPrefixTheSame is True:
                    self.current_hint_index = len(self.input_text.text())
                    self.input_text.setText(Word.Word.current_word[0:self.current_hint_index + 1])
                else:
                    self.current_hint_index = 0
                    self.input_text.setText(Word.Word.current_word[0])
            else:
                self.current_hint_index = 0
                self.input_text.setText(Word.Word.current_word[0])
        self.current_hint_index += 1
        Windows.Windows.context_mode_window.setFocus()

    @staticmethod
    def pronunciation_UK_function():
        Word.Word.get_the_pronunciation_of_a_word_with_British_accent()
        Windows.Windows.audition_mode_window.setFocus()

    @staticmethod
    def pronunciation_US_function():
        Word.Word.get_the_pronunciation_of_a_word_with_American_accent()
        Windows.Windows.context_mode_window.setFocus()

    def shuffle_button_function(self):
        self.index_of_the_current_word = len(self.words) - 1
        if self.type_of_order == "straight":
            self.type_of_order = "shuffled"
            Exerciser.Exerciser.random_shuffle(self.words)
            self.shuffle_button.setStyleSheet(Windows.Windows.style_sheet_for_shuffle_button_on)
            Word.Word.current_word = self.words[-1]
            self.display_the_usage()

        else:
            self.type_of_order = "straight"
            wordlist: str = Windows.Windows.exerciser_window.choose_wordlist.currentText()
            self.words = Exerciser.Exerciser.dict_of_added_words[wordlist].copy()
            Word.Word.current_word = self.words[-1]
            self.display_the_usage()
            self.shuffle_button.setStyleSheet(Windows.Windows.style_sheet_for_shuffle_button_off)
        Windows.Windows.context_mode_window.setFocus()

    def submit_button_function(self):
        answer: str = self.input_text.text()
        if answer == Word.Word.current_word:
            self.wrong_answer_line.hide()
            self.input_text.setStyleSheet(self.style_sheet_after_correct_answer)
            self.show_pronunciation_buttons()
            if self.mistake_was_made == "None":
                self.mistake_was_made = "False"
        else:
            if self.mistake_was_made == "None":
                self.array_of_mistakes.append(answer)
                self.mistake_was_made = "True"
            self.wrong_answer_line.show()
            self.input_text.setStyleSheet(self.style_sheet_after_wrong_answer)
        Windows.Windows.context_mode_window.setFocus()

    def next_button_function(self):
        self.index_of_the_current_word -= 1
        if self.mistake_was_made == "None":
            self.array_of_mistakes.append(Word.Word.current_word)
        self.mistake_was_made = "None"
        if self.index_of_the_current_word < 0:
            action: str = Windows.Windows.open_window_after_all_words_reviewed(len(self.array_of_mistakes),
                                                                               len(self.words))
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
        self.input_text.setStyleSheet(self.style_sheet_by_default)
        Windows.Windows.audition_mode_window.setFocus()
        self.current_hint_index = 1


