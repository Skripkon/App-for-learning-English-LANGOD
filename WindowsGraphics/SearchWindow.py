import requests
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from time import time
import Exerciser
import Word
import connection
from WindowsGraphics import Windows, ExerciserWindow
from PyQt5 import QtCore


class SearchWindow(QDialog):
    def __init__(self):
        super(SearchWindow, self).__init__()
        loadUi('WindowsGraphics/SearchWindow.ui', self)
        self.connect_interface_with_functions()
        self.forbid_to_change_the_interface()
        self.hide_the_interface()
        self.pronunciation_US.setIcon(QIcon("WindowsGraphics/voiceButtonIcon.png"))
        self.pronunciation_UK.setIcon(QIcon("WindowsGraphics/voiceButtonIcon.png"))
        self.add_word_button.setIcon(QIcon("WindowsGraphics/add_button.png"))
        self.add_word_button.setIconSize(QtCore.QSize(50, 50))
        Word.Word.create_folder_to_store_mp4_files()  # check whether necessary folder exists
        Windows.Windows.search_window = self

    def back_to_the_main_page_button_function(self):
        connection.IP.user_id = None
        Windows.Windows.search_window.hide()
        Windows.Windows.sign_in_window.show()
        self.hide_the_interface()
        self.clear_fields()
        Windows.Windows.widget.setFocus()
        Windows.Windows.search_window = None
        Windows.Windows.exerciser_window = None
        Windows.Windows.revision_mode_window = None
        Windows.Windows.flashcards_mode_window = None
        Windows.Windows.context_mode_window = None

    def clear_fields(self):
        self.search_field.clear()
        self.definitions_text.clear()
        self.usage_text.clear()

    def go_to_the_exerciser_button_function(self):
        if Windows.Windows.exerciser_window is None:
            ExerciserWindow.ExerciserWindow()
            Windows.Windows.widget.addWidget(Windows.Windows.exerciser_window)
            Windows.Windows.widget.setCurrentIndex(Windows.Windows.widget.currentIndex() + 1)
        Windows.Windows.search_window.hide()
        Windows.Windows.exerciser_window.show()
        self.hide_the_interface()
        self.clear_fields()
        Windows.Windows.widget.setFocus()

    def connect_interface_with_functions(self):
        self.back_to_the_main_page_button.clicked.connect(self.back_to_the_main_page_button_function)
        self.search_button.clicked.connect(self.search_button_function)
        self.pronunciation_US.clicked.connect(
            self.time_required(Word.Word.get_the_pronunciation_of_a_word_with_American_accent))
        self.pronunciation_UK.clicked.connect(
            self.time_required(Word.Word.get_the_pronunciation_of_a_word_with_British_accent))
        self.go_to_the_exerciser_button.clicked.connect(self.go_to_the_exerciser_button_function)
        self.add_word_button.clicked.connect(self.add_word_button_function)
        self.add_word_button.released.connect(self.add_word_button_released_function)

    @staticmethod
    def add_word_button_function():
        if Word.Word.current_word not in Exerciser.Exerciser.dict_of_added_words:
            url: str = "http://" + connection.IP.ip + ":12345/AddNewWord"
            response = requests.get(url, headers={'Word': Word.Word.current_word})
            n = int(response.text)
            Exerciser.Exerciser.dict_of_added_words[Word.Word.current_word] = n
            Exerciser.Exerciser.array_of_added_words.append(Word.Word.current_word)
        Windows.Windows.search_window.setFocus()

    def add_word_button_released_function(self):
        self.add_word_button.setIcon(QIcon("WindowsGraphics/add_button_yellow.png"))

    def hide_the_interface(self):
        self.pronunciation_US.hide()
        self.pronunciation_UK.hide()
        self.pronunciation_US_text.hide()
        self.pronunciation_UK_text.hide()
        self.definitions_title.hide()
        self.definitions_text.hide()
        self.usage_text.hide()
        self.usage_title.hide()
        self.add_word_button.hide()
        self.add_line.hide()
        self.nothing_found_error_line.hide()

    def show_the_interface(self):
        self.pronunciation_US.show()
        self.pronunciation_UK.show()
        self.pronunciation_US_text.show()
        self.pronunciation_UK_text.show()
        self.definitions_title.show()
        self.definitions_text.show()
        self.usage_text.show()
        self.usage_title.show()
        self.add_word_button.show()
        self.add_line.show()

    def forbid_to_change_the_interface(self):
        self.definitions_text.setReadOnly(True)
        self.usage_text.setReadOnly(True)

    def search_button_function(self):
        self.definitions_text.clear()
        self.usage_text.clear()
        Word.Word.current_word = self.search_field.text().lower().replace(" ", '')
        if Word.Word.check_whether_the_word_is_valid() is False:
            self.hide_the_interface()
            self.nothing_found_error_line.show()
            Windows.Windows.search_window.setFocus()
            return None
        self.nothing_found_error_line.hide()
        output_of_examples = Word.Word.get_the_usage_of_a_word()
        output_of_definitions = Word.Word.get_the_meaning_of_a_word()
        self.definitions_text.append(output_of_definitions)
        self.usage_text.append(output_of_examples)
        if Word.Word.current_word in Exerciser.Exerciser.dict_of_added_words:
            self.add_word_button.setIcon(QIcon("WindowsGraphics/add_button_yellow.png"))
        else:
            self.add_word_button.setIcon(QIcon("WindowsGraphics/add_button.png"))
        self.show_the_interface()
        self.definitions_text.verticalScrollBar().setValue(0)
        self.usage_text.verticalScrollBar().setValue(0)
        Windows.Windows.search_window.setFocus()

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
