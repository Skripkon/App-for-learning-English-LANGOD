from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from time import time
import Word
from WindowsGraphics import Windows
import threading


class SearchWindow(QMainWindow):
    __metaclass__ = Windows
    # this field indicates whether the search returns text or nothing.
    # If the text was found, it contains it
    output_of_definitions = "Error"

    def __init__(self):
        super(SearchWindow, self).__init__()
        loadUi('WindowsGraphics/SearchWindow.ui', self)
        self.connect_interface_with_functions()
        self.forbid_to_change_the_interface()
        self.hide_the_interface()
        self.pronunciationUSA.setIcon(QIcon("WindowsGraphics/voiceButtonIcon.png"))
        self.pronunciationUK.setIcon(QIcon("WindowsGraphics/voiceButtonIcon.png"))
        self.add_word_button.setIcon(QIcon("WindowsGraphics/add_button.png"))
        self.add_word_button.setIconSize(QtCore.QSize(50, 50))
        Word.Word.create_folder_to_store_mp4_files()  # check whether necessary folder exists
        Windows.Windows.search_window = self
        self.Back_button.clicked.connect(self.back_to_sign_in_button_function)
        
    def back_to_sign_in_button_function(self):
        Windows.Windows.search_window.hide()
        Windows.Windows.sign_in_window.show()

    def connect_interface_with_functions(self):
        self.searchbutton.clicked.connect(self.search_button_function)
        self.pronunciationUSA.clicked.connect(
            self.time_required(Word.Word.get_the_pronunciation_of_a_word_with_American_accent))
        self.pronunciationUK.clicked.connect(
            self.time_required(Word.Word.get_the_pronunciation_of_a_word_with_British_accent))

    def hide_the_interface(self):
        self.pronunciationUSA.hide()
        self.pronunciationUK.hide()
        self.pronunciationUSAtext.hide()
        self.pronunciationUKtext.hide()
        self.definitionsTitle.hide()
        self.definitionsText.hide()
        self.usageText.hide()
        self.usageTitle.hide()
        self.add_word_button.hide()
        self.add_line.hide()

    def show_the_interface(self):
        self.pronunciationUSA.show()
        self.pronunciationUK.show()
        self.pronunciationUSAtext.show()
        self.pronunciationUKtext.show()
        self.definitionsTitle.show()
        self.definitionsText.show()
        self.usageText.show()
        self.usageTitle.show()
        self.add_word_button.show()
        self.add_line.show()

    def forbid_to_change_the_interface(self):
        self.definitionsTitle.setReadOnly(True)
        self.pronunciationUSAtext.setReadOnly(True)
        self.pronunciationUKtext.setReadOnly(True)
        self.definitionsText.setReadOnly(True)
        self.usageText.setReadOnly(True)
        self.usageTitle.setReadOnly(True)

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
