import requests
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from time import time
import Exerciser
import Word
import connection
from WindowsGraphics import Windows, ExerciserWindow, MyWordlistsWindow
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
        for wordlist in Exerciser.Exerciser.dict_of_added_words:
            self.choose_wordlist.addItem(wordlist)

    def currentTextChangedFunction(self):
        if Word.Word.current_word in Exerciser.Exerciser.dict_of_added_words[self.choose_wordlist.currentText()]:
            self.add_word_button.setIcon(QIcon("WindowsGraphics/add_button_yellow.png"))
        else:
            self.add_word_button.setIcon(QIcon("WindowsGraphics/add_button.png"))

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
        else:
            Windows.Windows.exerciser_window.choose_wordlist.clear()
        isComboBoxEmpty: bool = True
        for item in Exerciser.Exerciser.dict_of_added_words.keys():
            if len(Exerciser.Exerciser.dict_of_added_words[item]) >= 6:
                Windows.Windows.exerciser_window.choose_wordlist.addItem(item)
                isComboBoxEmpty = False
        if not isComboBoxEmpty:
            Exerciser.Exerciser.array_of_words_for_exercise = \
                Exerciser.Exerciser.dict_of_added_words[Windows.Windows.exerciser_window.choose_wordlist.currentText()]
            Windows.Windows.exerciser_window.show()
            Windows.Windows.search_window.hide()
            self.hide_the_interface()
        else:
            Windows.Windows.exerciser_window.hide()
            Windows.Windows.search_window.show()
            Windows.Windows.open_the_window("error",
                                            "to start exercising you must have at least one wordlist with at least 6 words")
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
        self.create_new_wordlist_button.clicked.connect(self.create_new_wordlist_button_function)
        self.go_to_my_wordlists_button.clicked.connect(self.go_to_my_wordlists_button_function)
        self.choose_wordlist.currentTextChanged.connect(self.currentTextChangedFunction)

    @staticmethod
    def go_to_my_wordlists_button_function():
        if Windows.Windows.my_wordlists_window is None:
            MyWordlistsWindow.MyWordlistsWindow()
            Windows.Windows.widget.addWidget(Windows.Windows.my_wordlists_window)
            Windows.Windows.widget.setCurrentIndex(Windows.Windows.widget.currentIndex() + 1)
        else:
            Windows.Windows.my_wordlists_window.change_displayed_text \
                (Windows.Windows.my_wordlists_window.choose_wordlist.currentText())
        Windows.Windows.search_window.hide()
        Windows.Windows.my_wordlists_window.show()
        Windows.Windows.my_wordlists_window.words_text.verticalScrollBar().setValue(0)
        Windows.Windows.widget.setFocus()

    @classmethod
    def check_whether_wordlist_with_such_name_already_exists(cls, name: str) -> bool:
        if name in Exerciser.Exerciser.dict_of_added_words:
            return True
        else:
            return False

    def create_new_wordlist_button_function(self):
        name: str = self.create_new_wordlist_input.text()
        if self.check_whether_wordlist_with_such_name_already_exists(name):
            Windows.Windows.open_the_window("Error", f"Wordlist with name '{name}' already exists")
            return None
        url: str = "http://" + connection.IP.ip + f":{connection.IP.port}/AddNewWordlist"
        requests.get(url, headers={'Wordlist': name, 'UserId': str(connection.IP.user_id)})
        self.choose_wordlist.addItem(name)
        self.create_new_wordlist_input.clear()
        Exerciser.Exerciser.dict_of_added_words[name] = []
        Exerciser.Exerciser.privacy_settings_for_wordlists[name] = ["public"]
        Windows.Windows.search_window.setFocus()

    def add_word_button_function(self):
        if Word.Word.current_word not in Exerciser.Exerciser.dict_of_added_words[self.choose_wordlist.currentText()]:
            wordlist: str = self.choose_wordlist.currentText()
            url: str = "http://" + connection.IP.ip + f":{connection.IP.port}/AddNewWord"
            requests.get(url, headers={'Word': Word.Word.current_word,
                                       'UserId': str(connection.IP.user_id),
                                       'Wordlist': wordlist})
            Exerciser.Exerciser.dict_of_added_words[wordlist].append(Word.Word.current_word)
            self.add_word_button_released_function()
        else:
            word: str = self.search_field.text().lower()
            url: str = "http://" + connection.IP.ip + f":{connection.IP.port}/DeleteWord"
            id_wordlist = str(connection.IP.user_id) + '_' + self.choose_wordlist.currentText()
            requests.get(url, headers={'Word': word, "id_wordlist": id_wordlist})
            self.add_word_button_released_function()
            self.add_word_button.setIcon(QIcon("WindowsGraphics/add_button.png"))
            Exerciser.Exerciser.dict_of_added_words[self.choose_wordlist.currentText()].remove(Word.Word.current_word)
        Windows.Windows.search_window.setFocus()

    def add_word_button_released_function(self):
        if Word.Word.current_word in Exerciser.Exerciser.dict_of_added_words[self.choose_wordlist.currentText()]:
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
        self.nothing_found_error_line.hide()
        self.choose_wordlist.hide()
        self.create_new_wordlist_input.hide()
        self.create_new_wordlist_button.hide()

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
        self.choose_wordlist.show()
        self.create_new_wordlist_input.show()
        self.create_new_wordlist_button.show()

    def forbid_to_change_the_interface(self):
        self.definitions_text.setReadOnly(True)
        self.usage_text.setReadOnly(True)

    def search_button_function(self):
        self.definitions_text.clear()
        self.usage_text.clear()
        Word.Word.current_word = self.search_field.text().lower()
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
        if Word.Word.current_word in Exerciser.Exerciser.dict_of_added_words[self.choose_wordlist.currentText()]:
            self.add_word_button.setIcon(QIcon("WindowsGraphics/add_button_yellow.png"))
        else:
            self.add_word_button.setIcon(QIcon("WindowsGraphics/add_button.png"))
        self.show_the_interface()
        self.choose_wordlist.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
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
