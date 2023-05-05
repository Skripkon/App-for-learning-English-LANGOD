from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from time import time
import Exerciser
import Word
from WindowsGraphics import Windows


class RevisionModeWindow(QDialog):
    words: list[str] = []

    def __init__(self):
        super(RevisionModeWindow, self).__init__()
        loadUi("WindowsGraphics/RevisionModeWindow.ui", self)
        Windows.Windows.revision_mode_window = self
        self.pronunciation_US.setIcon(QIcon("WindowsGraphics/voiceButtonIcon.png"))
        self.pronunciation_UK.setIcon(QIcon("WindowsGraphics/voiceButtonIcon.png"))
        self.definitions_text.setReadOnly(True)
        self.examples_text.setReadOnly(True)
        self.word_line.setText(self.words[-1])
        Word.Word.current_word = self.words[-1]
        self.connect_interface_with_functions()
        self.index_of_the_current_word = len(self.words) - 1
        self.type_of_order = "straight"

    def connect_interface_with_functions(self):
        self.pronunciation_US.clicked.connect(self.play_sound_with_us_accent)
        self.pronunciation_UK.clicked.connect(self.play_sound_with_uk_accent)
        self.show_definitions_button.clicked.connect(self.show_definitions_button_function)
        self.show_examples_button.clicked.connect(self.show_examples_button_function)
        self.exit_button.clicked.connect(self.exit_button_function)
        self.next_button.clicked.connect(self.next_button_function)
        self.shuffle_button.clicked.connect(self.shuffle_button_function)

    def play_sound_with_uk_accent(self):
        self.time_required(Word.Word.get_the_pronunciation_of_a_word_with_British_accent())
        Windows.Windows.revision_mode_window.setFocus()

    def play_sound_with_us_accent(self):
        self.time_required(Word.Word.get_the_pronunciation_of_a_word_with_American_accent())
        Windows.Windows.revision_mode_window.setFocus()

    def show_definitions_button_function(self):
        self.definitions_text.clear()
        output_of_definitions = Word.Word.get_the_meaning_of_a_word()
        self.definitions_text.append(output_of_definitions)
        self.definitions_text.verticalScrollBar().setValue(0)
        Windows.Windows.revision_mode_window.setFocus()

    def show_examples_button_function(self):
        self.examples_text.clear()
        output_of_examples = Word.Word.get_the_usage_of_a_word()
        self.examples_text.append(output_of_examples)
        self.examples_text.verticalScrollBar().setValue(0)
        Windows.Windows.revision_mode_window.setFocus()

    def shuffle_button_function(self):
        if self.type_of_order == "straight":
            self.type_of_order = "shuffled"
            Exerciser.Exerciser.random_shuffle(self.words)
            self.shuffle_button.setStyleSheet('QPushButton {selection-background-color: rgb(255, 255, 255); '
                                              'font-size:15pt; color: yellow;}')
            self.word_line.setText(self.words[-1])
            Word.Word.current_word = self.words[-1]
        else:
            self.type_of_order = "straight"
            self.words = Exerciser.Exerciser.array_of_added_words.copy()
            self.index_of_the_current_word = len(self.words) - 1
            self.word_line.setText(self.words[-1])
            self.shuffle_button.setStyleSheet('QPushButton {selection-background-color: rgb(255, 255, 255); '
                                              'font-size:15pt; color: white;}')
            Word.Word.current_word = self.words[-1]
        self.clear_output()
        Windows.Windows.revision_mode_window.setFocus()

    @staticmethod
    def exit_button_function():
        # Exerciser.Exerciser.array_of_words_for_exercise.clear()
        Windows.Windows.revision_mode_window.hide()
        Windows.Windows.exerciser_window.show()
        Windows.Windows.revision_mode_window.setFocus()

    def clear_output(self):
        self.definitions_text.clear()
        self.examples_text.clear()

    def next_button_function(self):
        self.index_of_the_current_word -= 1
        if self.index_of_the_current_word < 0:
            self.index_of_the_current_word = len(self.words) - 1
        self.clear_output()
        Word.Word.current_word = self.words[self.index_of_the_current_word]
        self.word_line.setText(Word.Word.current_word)
        Windows.Windows.revision_mode_window.setFocus()

    def keyPressEvent(self, event):
        if event.nativeScanCode() == 9:  # button ESC pressed
            self.exit_button_function()
        if event.nativeScanCode() == 39:  # button s pressed
            self.play_sound_with_us_accent()
        if event.nativeScanCode() == 26:  # button e pressed
            self.show_examples_button_function()
        if event.nativeScanCode() == 40:  # button d pressed
            self.show_definitions_button_function()
        if event.nativeScanCode() == 65:  # button space pressed
            self.next_button_function()

    @staticmethod
    def time_required(f):
        last = [time()]

        def decorator():
            if time() - last[0] < 1:
                return None
            last[0] = time()
            return f()

        return decorator
