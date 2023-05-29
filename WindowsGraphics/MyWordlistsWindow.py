import requests
from PyQt5.QtWidgets import QDialog, QPushButton, QScrollArea, QGroupBox, QVBoxLayout, QFormLayout, QLabel
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets

import Exerciser
import Word
import connection
from WindowsGraphics import Windows, FindWordlistsWindow


class MyWordlistsWindow(QDialog):

    def __init__(self):
        super(MyWordlistsWindow, self).__init__()
        loadUi("WindowsGraphics/MyWordlistsWindow.ui", self)
        self.choose_wordlist.currentTextChanged.connect(self.currentTextChangedFunction)
        self.back_to_the_search_button.clicked.connect(self.back_to_the_search_button_function)
        self.delete_word_button.clicked.connect(self.delete_word_button_function)
        self.change_privacy_button.clicked.connect(self.change_privacy_button_function)
        self.find_wordlists_button.clicked.connect(self.find_wordlists_button_function)
        Windows.Windows.my_wordlists_window = self

    def set_wordlists(self):
        for wordlist in Exerciser.Exerciser.dict_of_added_words:
            self.choose_wordlist.addItem(wordlist)
        self.words_text.setReadOnly(True)

    def find_wordlists_button_function(self):
        self.hide()
        if Windows.Windows.find_wordlists_window is None:
            FindWordlistsWindow.FindWordlistsWindow()
            Windows.Windows.widget.addWidget(Windows.Windows.find_wordlists_window)
            Windows.Windows.widget.setCurrentIndex(Windows.Windows.widget.currentIndex() + 1)
        else:
            Windows.Windows.find_wordlists_window.show()
        Windows.Windows.widget.setFocus()

    def change_privacy_button_function(self):
        wordlist = self.choose_wordlist.currentText()
        if wordlist == "":
            return None
        new_privacy: str = "private" if \
            Exerciser.Exerciser.privacy_settings_for_wordlists[wordlist] == "public" else "public"
        self.change_privacy_button.setText(new_privacy)
        Exerciser.Exerciser.privacy_settings_for_wordlists[wordlist] = new_privacy
        id_wordlist: str = str(connection.IP.user_id) + "_" + wordlist
        url: str = "http://" + connection.IP.ip + f":{connection.IP.port}/ChangePrivacySettings"
        requests.get(url, headers={'IdWordlist': id_wordlist, 'PrivacyType': new_privacy})
        Windows.Windows.my_wordlists_window.setFocus()

    def delete_word_button_function(self):
        current_wordlist: str = self.choose_wordlist.currentText()
        word_to_delete: str = self.delete_word_input.text().lower()
        if word_to_delete in Exerciser.Exerciser.dict_of_added_words[current_wordlist]:
            url: str = "http://" + connection.IP.ip + f":{connection.IP.port}/DeleteWord"
            id_wordlist = str(connection.IP.user_id) + '_' + current_wordlist
            requests.get(url, headers={'Word': word_to_delete, "id_wordlist": id_wordlist})
            Exerciser.Exerciser.dict_of_added_words[current_wordlist].remove(word_to_delete)
            self.change_displayed_text(current_wordlist)
        else:
            Windows.Windows.open_the_window("error", "You are attempting to delete the word, "
                                                     "which does not exist in selected wordlist")
        self.delete_word_input.clear()
        Windows.Windows.my_wordlists_window.setFocus()

    def currentTextChangedFunction(self):
        new_wordlist: str = self.choose_wordlist.currentText()
        if new_wordlist == "":
            return None
        self.change_displayed_text(new_wordlist)

    def change_displayed_text(self, wordlist: str):
        self.words_text.clear()
        if Exerciser.Exerciser.privacy_settings_for_wordlists[wordlist] == "public":
            self.change_privacy_button.setText("public")
        elif Exerciser.Exerciser.privacy_settings_for_wordlists[wordlist] == "private":
            self.change_privacy_button.setText("private")
        for word in Exerciser.Exerciser.dict_of_added_words[wordlist]:
            self.words_text.append("• " + word)
        self.words_text.verticalScrollBar().setValue(0)

    @staticmethod
    def back_to_the_search_button_function():
        Windows.Windows.my_wordlists_window.hide()
        Windows.Windows.search_window.show()
        Windows.Windows.widget.setFocus()
