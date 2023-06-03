from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtCore
import Exerciser
import Word
from WindowsGraphics import Windows


class RevisionModeWindow(QDialog):
    words: list[str] = []
    array_of_mistakes = []
    index_of_the_current_word: int

    def __init__(self):
        super(RevisionModeWindow, self).__init__()
        loadUi("WindowsGraphics/RevisionModeWindow.ui", self)
        Windows.Windows.revision_mode_window = self
        self.pronunciation_US.setIcon(QIcon("WindowsGraphics/voiceButtonIcon.png"))
        self.pronunciation_UK.setIcon(QIcon("WindowsGraphics/voiceButtonIcon.png"))
        self.hide_definitions_and_usage()
        self.definitions_text.setReadOnly(True)
        self.examples_text.setReadOnly(True)
        self.connect_interface_with_functions()
        self.type_of_order = "straight"

    def init_first_word(self):
        self.word_line.setText(self.words[-1])
        Word.Word.current_word = self.words[-1]
        self.index_of_the_current_word = len(self.words) - 1

    def connect_interface_with_functions(self):
        self.pronunciation_US.clicked.connect(Windows.Windows.play_sound_with_us_accent)
        self.pronunciation_UK.clicked.connect(Windows.Windows.play_sound_with_uk_accent)
        self.show_definitions_button.clicked.connect(self.show_definitions_button_function)
        self.show_examples_button.clicked.connect(self.show_examples_button_function)
        self.exit_button.clicked.connect(self.exit_button_function)
        self.next_button.clicked.connect(self.next_button_function)
        self.shuffle_button.clicked.connect(self.shuffle_button_function)
        self.do_not_remember_button.clicked.connect(self.do_not_remember_button_function)

    def do_not_remember_button_function(self):
        self.array_of_mistakes.append(self.words[self.index_of_the_current_word])
        self.next_button_function()

    def show_definitions_button_function(self):
        self.definitions_text.clear()
        self.definitions_text.show()
        output_of_definitions = Word.Word.get_the_meaning_of_a_word()
        self.definitions_text.append(output_of_definitions)
        self.definitions_text.verticalScrollBar().setValue(0)
        Windows.Windows.revision_mode_window.setFocus()

    def show_examples_button_function(self):
        self.examples_text.clear()
        self.examples_text.show()
        output_of_examples = Word.Word.get_the_usage_of_a_word()
        self.examples_text.append(output_of_examples)
        self.examples_text.verticalScrollBar().setValue(0)
        Windows.Windows.revision_mode_window.setFocus()

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
        self.clear_output()
        Windows.Windows.revision_mode_window.setFocus()

    @staticmethod
    def exit_button_function():
        Windows.Windows.revision_mode_window.hide()
        Windows.Windows.exerciser_window.show()
        Windows.Windows.revision_mode_window.setFocus()

    def clear_output(self):
        self.definitions_text.clear()
        self.examples_text.clear()

    def next_button_function(self):
        self.index_of_the_current_word -= 1
        if self.index_of_the_current_word < 0:
            action: str = Windows.Windows.open_window_after_all_words_reviewed(len(self.array_of_mistakes), len(self.words))
            if action == "break":
                self.exit_button_function()
                self.array_of_mistakes.clear()
                return None
            elif action == "Learn your mistakes":
                self.words = self.array_of_mistakes.copy()
                self.index_of_the_current_word = len(self.words) - 1
                self.array_of_mistakes.clear()
            else:
                if self.words != Exerciser.Exerciser.array_of_words_for_exercise:
                    self.words = Exerciser.Exerciser.array_of_words_for_exercise
                self.index_of_the_current_word = len(self.words) - 1
                self.array_of_mistakes.clear()
        self.clear_output()
        Word.Word.current_word = self.words[self.index_of_the_current_word]
        self.word_line.setText(Word.Word.current_word)
        self.hide_definitions_and_usage()
        Windows.Windows.revision_mode_window.setFocus()

    def hide_definitions_and_usage(self):
        self.examples_text.hide()
        self.definitions_text.hide()

    def keyPressEvent(self, event):
        if event.nativeScanCode() == 9:  # button ESC pressed
            self.exit_button_function()
        if event.nativeScanCode() == 39:  # button s pressed
            Windows.Windows.play_sound_with_us_accent()
        if event.nativeScanCode() == 26:  # button e pressed
            self.show_examples_button_function()
        if event.nativeScanCode() == 40:  # button d pressed
            self.show_definitions_button_function()
        if event.nativeScanCode() == 65:  # button space pressed
            self.next_button_function()
