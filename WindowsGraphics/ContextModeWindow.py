from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from time import time
import Exerciser
import Word
from WindowsGraphics import Windows
import time


class ContextModeWindow(QDialog):
    words: list[str] = []
    current_hint_index = 1
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

    def __init__(self):
        super(ContextModeWindow, self).__init__()
        loadUi("WindowsGraphics/ContextModeWindow.ui", self)
        Windows.Windows.context_mode_window = self
        self.wrong_answer_line.hide()
        self.pronunciation_US.setIcon(QIcon("WindowsGraphics/voiceButtonIcon.png"))
        self.pronunciation_UK.setIcon(QIcon("WindowsGraphics/voiceButtonIcon.png"))
        self.usage_text.setReadOnly(True)
        self.connect_interface_with_functions()
        self.type_of_order = "straight"
        self.hide_pronunciation_buttons()

    def init_first_word(self):
        Word.Word.current_word = self.words[-1]
        self.display_the_usage()
        self.index_of_the_current_word = len(self.words) - 1
        self.input_text.setStyleSheet(self.style_sheet_by_default)
        self.hide_pronunciation_buttons()

    def show_pronunciation_buttons(self):
        self.pronunciation_US.show()
        self.pronunciation_UK.show()
        self.pronunciation_UK_text.show()
        self.pronunciation_US_text.show()

    def hide_pronunciation_buttons(self):
        self.pronunciation_US.hide()
        self.pronunciation_UK.hide()
        self.pronunciation_UK_text.hide()
        self.pronunciation_US_text.hide()

    def connect_interface_with_functions(self):
        self.pronunciation_US.clicked.connect(self.play_sound_with_us_accent)
        self.pronunciation_UK.clicked.connect(self.play_sound_with_uk_accent)
        self.exit_button.clicked.connect(self.exit_button_function)
        self.next_button.clicked.connect(self.next_button_function)
        self.shuffle_button.clicked.connect(self.shuffle_button_function)
        self.submit_button.clicked.connect(self.submit_button_function)
        self.answer_button.clicked.connect(self.answer_button_function)
        self.hint_button.clicked.connect(self.hint_button_function)

    def submit_button_function(self):
        answer: str = self.input_text.text()
        if answer == Word.Word.current_word:
            self.wrong_answer_line.hide()
            self.input_text.setStyleSheet(self.style_sheet_after_correct_answer)
            self.show_pronunciation_buttons()
        else:
            self.wrong_answer_line.show()
            self.input_text.setStyleSheet(self.style_sheet_after_wrong_answer)
        Windows.Windows.context_mode_window.setFocus()

    def hint_button_function(self):
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

    def answer_button_function(self):
        self.wrong_answer_line.hide()
        self.input_text.setText(Word.Word.current_word)
        self.current_hint_index = len(Word.Word.current_word)
        self.input_text.setStyleSheet(self.style_sheet_after_correct_answer)
        Windows.Windows.context_mode_window.setFocus()
        self.show_pronunciation_buttons()

    @staticmethod
    def play_sound_with_uk_accent():
        Word.Word.get_the_pronunciation_of_a_word_with_British_accent()
        Windows.Windows.context_mode_window.setFocus()

    @staticmethod
    def play_sound_with_us_accent():
        Word.Word.get_the_pronunciation_of_a_word_with_American_accent()
        Windows.Windows.context_mode_window.setFocus()

    def display_the_usage(self):
        self.clear_output()
        output_of_examples = Word.Word.get_the_usage_of_a_word()
        output_of_examples = output_of_examples.replace(Word.Word.current_word, " . . . . ")
        self.usage_text.append(output_of_examples)
        self.usage_text.verticalScrollBar().setValue(0)
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

    @staticmethod
    def exit_button_function():
        Windows.Windows.context_mode_window.hide()
        Windows.Windows.exerciser_window.show()
        Windows.Windows.context_mode_window.setFocus()

    def clear_output(self):
        self.usage_text.clear()
        self.input_text.clear()

    def next_button_function(self):
        self.index_of_the_current_word -= 1
        if self.index_of_the_current_word < 0:
            action: str = Windows.Windows.open_window_after_all_words_reviewed()
            if action == "break":
                self.exit_button_function()
                return None
            else:
                self.index_of_the_current_word = len(self.words) - 1
        self.clear_output()
        Word.Word.current_word = self.words[self.index_of_the_current_word]
        self.display_the_usage()
        self.wrong_answer_line.hide()
        self.input_text.setStyleSheet(self.style_sheet_by_default)
        Windows.Windows.context_mode_window.setFocus()
        self.current_hint_index = 1
        self.hide_pronunciation_buttons()

    def keyPressEvent(self, event):
        if event.nativeScanCode() == 36:  # button Enter pressed
            self.submit_button_function()
        Windows.Windows.context_mode_window.setFocus()