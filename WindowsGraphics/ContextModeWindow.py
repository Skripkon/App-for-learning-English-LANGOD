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

    def __init__(self):
        super(ContextModeWindow, self).__init__()
        loadUi("WindowsGraphics/ContextModeWindow.ui", self)
        Windows.Windows.context_mode_window = self
        self.wrong_answer_line.hide()
        self.pronunciation_US.setIcon(QIcon("WindowsGraphics/voiceButtonIcon.png"))
        self.pronunciation_UK.setIcon(QIcon("WindowsGraphics/voiceButtonIcon.png"))
        self.usage_text.setReadOnly(True)
        Word.Word.current_word = self.words[-1]
        self.connect_interface_with_functions()
        self.index_of_the_current_word = len(self.words) - 1
        self.type_of_order = "straight"
        # self.display_the_usage()

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
            self.input_text.setStyleSheet('QLineEdit '
                                          '{selection-background-color: rgb(255, 255, 255);'
                                          'font-size:15pt;'
                                          'background-color: #008000}')
        else:
            self.wrong_answer_line.show()
            self.input_text.setStyleSheet('QLineEdit '
                                          '{selection-background-color: rgb(255, 255, 255);'
                                          'font-size:15pt;'
                                          'color: rgb(255, 255, 255)}')
        Windows.Windows.context_mode_window.setFocus()

    def hint_button_function(self):
        self.wrong_answer_line.hide()
        self.input_text.setText(Word.Word.current_word[0:self.current_hint_index])
        self.current_hint_index += 1
        Windows.Windows.context_mode_window.setFocus()

    def answer_button_function(self):
        self.wrong_answer_line.hide()
        self.input_text.setText(Word.Word.current_word)
        self.current_hint_index = len(Word.Word.current_word)
        Windows.Windows.context_mode_window.setFocus()

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
            self.shuffle_button.setStyleSheet('QPushButton {selection-background-color: rgb(255, 255, 255); '
                                              'font-size:15pt; color: yellow;}')
            Word.Word.current_word = self.words[-1]
            self.display_the_usage()

        else:
            self.type_of_order = "straight"
            self.words = Exerciser.Exerciser.array_of_added_words.copy()
            Word.Word.current_word = self.words[-1]
            self.display_the_usage()
            self.shuffle_button.setStyleSheet('QPushButton {selection-background-color: rgb(255, 255, 255); '
                                              'font-size:15pt; color: white;}')
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
            self.index_of_the_current_word = len(self.words) - 1
        self.clear_output()
        Word.Word.current_word = self.words[self.index_of_the_current_word]
        self.display_the_usage()
        self.wrong_answer_line.hide()
        self.input_text.setStyleSheet('QLineEdit '
                                      '{selection-background-color: rgb(255, 255, 255);'
                                      'font-size:15pt;'
                                      'color: rgb(255, 255, 255)}')
        Windows.Windows.context_mode_window.setFocus()
        self.current_hint_index = 1

    def keyPressEvent(self, event):
        if event.nativeScanCode() == 36:  # button Enter pressed
            self.submit_button_function()
        Windows.Windows.context_mode_window.setFocus()

