from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from time import time
import Word
from WindowsGraphics import Windows


def time_required(f):
    last = [time()]

    def decorator():
        if time() - last[0] < 1:
            return None
        last[0] = time()
        return f()

    return decorator


class SearchWindow(QMainWindow):
    __metaclass__ = Windows

    def __init__(self):
        super(SearchWindow, self).__init__()
        loadUi('WindowsGraphics/SearchWindow.ui', self)
        self.connect_interface_with_functions()
        self.forbid_to_change_the_interface()
        self.hide_the_interface()
        self.pronunciationUSA.setIcon(QIcon("WindowsGraphics/voiceButtonIcon.png"))
        self.pronunciationUK.setIcon(QIcon("WindowsGraphics/voiceButtonIcon.png"))
        Word.Word.create_folder_to_store_mp4_files()  # check whether necessary folder exists
        Windows.Windows.search_window = self

    def connect_interface_with_functions(self):
        self.searchbutton.clicked.connect(self.search_button_function)
        self.pronunciationUSA.clicked.connect(
            time_required(Word.Word.get_the_pronunciation_of_a_word_with_American_accent))
        self.pronunciationUK.clicked.connect(
            time_required(Word.Word.get_the_pronunciation_of_a_word_with_British_accent))

    def hide_the_interface(self):
        self.pronunciationUSA.hide()
        self.pronunciationUK.hide()
        self.pronunciationUSAtext.hide()
        self.pronunciationUKtext.hide()
        self.definitionsTitle.hide()
        self.definitionsText.hide()
        self.usageText.hide()
        self.usageTitle.hide()

    def show_the_interface(self):
        self.pronunciationUSA.show()
        self.pronunciationUK.show()
        self.pronunciationUSAtext.show()
        self.pronunciationUKtext.show()
        self.definitionsTitle.show()
        self.definitionsText.show()
        self.usageText.show()
        self.usageTitle.show()

    def forbid_to_change_the_interface(self):
        self.definitionsTitle.setReadOnly(True)
        self.pronunciationUSAtext.setReadOnly(True)
        self.pronunciationUKtext.setReadOnly(True)
        self.definitionsText.setReadOnly(True)
        self.usageText.setReadOnly(True)
        self.usageTitle.setReadOnly(True)

    def search_button_function(self):
        self.definitionsText.clear()
        self.usageText.clear()
        search_text = self.searchfield.text()
        Word.Word.current_word = search_text
        meanings = Word.Word.get_the_meaning_of_a_word()
        if isinstance(meanings, str):
            self.definitionsText.append("Your search terms did not match any entries")
            return None
        outputOfDefinitions: str = ""
        for part_of_speech, definitions in meanings:
            outputOfDefinitions += part_of_speech
            outputOfDefinitions += ":\n"
            for definition in definitions:
                outputOfDefinitions += "- "
                outputOfDefinitions += definition
                outputOfDefinitions += '\n'

        outputOfExamples: str = ""
        examples = Word.Word.get_the_usage_of_a_word()
        for example in examples:
            outputOfExamples += '- '
            outputOfExamples += example
            outputOfExamples += '\n'
        self.definitionsText.append(outputOfDefinitions)
        self.usageText.append(outputOfExamples)
        self.show_the_interface()
        self.definitionsText.verticalScrollBar().setValue(0)
        self.usageText.verticalScrollBar().setValue(0)

    def keyPressEvent(self, event):
        if event.nativeScanCode() == 36:  # button Enter pressed
            self.search_button_function()
