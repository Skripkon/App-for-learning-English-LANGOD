from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QDialog
from PyQt5.uic import loadUi
from time import time

import DataBase
import Word
from WindowsGraphics import Windows, ExerciserWindow
import threading
from PyQt5 import QtCore


class SearchWindow(QDialog):
    # this field indicates whether the search returns text or nothing.
    # If the text was found, it contains it
    output_of_definitions = "Error"

    def __init__(self):
        super(SearchWindow, self).__init__()
        loadUi('WindowsGraphics/SearchWindow.ui', self)
        self.connect_interface_with_functions()
        self.forbid_to_change_the_interface()
        self.hide_the_interface()
        self.pronunciationUS.setIcon(QIcon("WindowsGraphics/voiceButtonIcon.png"))
        self.pronunciationUK.setIcon(QIcon("WindowsGraphics/voiceButtonIcon.png"))
        self.add_word_button.setIcon(QIcon("WindowsGraphics/add_button.png"))
        self.add_word_button.setIconSize(QtCore.QSize(50, 50))
        Word.Word.create_folder_to_store_mp4_files()  # check whether necessary folder exists
        Windows.Windows.search_window = self


    @staticmethod
    def back_to_the_main_page_button_function():
        DataBase.DataBase.current_user_id = None
        Windows.Windows.search_window.hide()
        Windows.Windows.sign_in_window.show()

    @staticmethod
    def go_to_the_exerciser_button_function():
        Windows.Windows.search_window.hide()
        if Windows.Windows.exerciser_window is None:
            ExerciserWindow.ExerciserWindow()
            Windows.Windows.widget.addWidget(Windows.Windows.exerciser_window)
            Windows.Windows.widget.setCurrentIndex(Windows.Windows.widget.currentIndex() + 1)
        Windows.Windows.exerciser_window.show()

    def connect_interface_with_functions(self):
        self.back_to_the_main_page_button.clicked.connect(self.back_to_the_main_page_button_function)
        self.searchbutton.clicked.connect(self.search_button_function)
        self.pronunciationUS.clicked.connect(
            self.time_required(Word.Word.get_the_pronunciation_of_a_word_with_American_accent))
        self.pronunciationUK.clicked.connect(
            self.time_required(Word.Word.get_the_pronunciation_of_a_word_with_British_accent))
        self.go_to_the_exerciser_button.clicked.connect(self.go_to_the_exerciser_button_function)
        self.add_word_button.clicked.connect(self.add_word_button_function)
        self.add_word_button.released.connect(self.add_word_button_released_function)

    def add_word_button_released_function(self):
        print("added")

    def add_word_button_function(self):
        DataBase.DataBase.add_new_word()

    def hide_the_interface(self):
        self.pronunciationUS.hide()
        self.pronunciationUK.hide()
        self.pronunciationUStext.hide()
        self.pronunciationUKtext.hide()
        self.definitionsTitle.hide()
        self.definitionsText.hide()
        self.usageText.hide()
        self.usageTitle.hide()
        self.add_word_button.hide()
        self.addLine.hide()

    def show_the_interface(self):
        self.pronunciationUS.show()
        self.pronunciationUK.show()
        self.pronunciationUStext.show()
        self.pronunciationUKtext.show()
        self.definitionsTitle.show()
        self.definitionsText.show()
        self.usageText.show()
        self.usageTitle.show()
        self.add_word_button.show()
        self.addLine.show()

    def forbid_to_change_the_interface(self):
        self.definitionsText.setReadOnly(True)
        self.usageText.setReadOnly(True)

    @staticmethod
    def return_usage() -> str:
        output_of_examples: str = ""
        examples = Word.Word.get_the_usage_of_a_word()
        for example in examples:
            output_of_examples += '- '
            output_of_examples += example
            output_of_examples += '\n'
        return output_of_examples

    def save_definitions_into_the_field_output_of_definitions(self) -> str:
        meanings = Word.Word.get_the_meaning_of_a_word()
        if isinstance(meanings, str):
            return "Error"
        output_of_definitions: str = ""
        for part_of_speech, definitions in meanings:
            output_of_definitions += part_of_speech
            output_of_definitions += ":\n"
            for definition in definitions:
                output_of_definitions += "- "
                output_of_definitions += definition
                output_of_definitions += '\n'
        self.output_of_definitions = output_of_definitions

    def search_button_function(self):
        self.definitionsText.clear()
        self.usageText.clear()
        Word.Word.current_word = self.searchfield.text()
        thread_to_get_definitions = \
            threading.Thread(target=self.save_definitions_into_the_field_output_of_definitions)
        thread_to_get_definitions.start()
        output_of_examples = self.return_usage()
        thread_to_get_definitions.join()
        if self.output_of_definitions == "Error":
            self.definitionsText.append("Your search terms did not match any entries")
        else:
            self.definitionsText.append(self.output_of_definitions)
            self.usageText.append(output_of_examples)
            self.show_the_interface()
            self.definitionsText.verticalScrollBar().setValue(0)
            self.usageText.verticalScrollBar().setValue(0)

    def keyPressEvent(self, event):
        if event.nativeScanCode() == 36:  # button Enter pressed
            self.search_button_function()

    @staticmethod
    def time_required(f):
        last = [time()]

        def decorator():
            if time() - last[0] < 1:
                return None
            last[0] = time()
            return f()

        return decorator
