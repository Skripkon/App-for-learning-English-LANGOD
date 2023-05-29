import requests
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QDialog, QPushButton, QScrollArea, QGroupBox, QVBoxLayout, QFormLayout, QLabel, QInputDialog
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets

import Exerciser
import Word
import connection
from WindowsGraphics import Windows, RevisionModeWindow, FlashCardsModeWindow, ContextModeWindow


class FindWordlistsWindow(QDialog):
    labelList = []
    buttonList = []
    list_of_words_to_add: list[str] = []
    scroll: QScrollArea = None
    groupBox: QGroupBox = None
    formLayout: QFormLayout = None

    def __init__(self):
        super(FindWordlistsWindow, self).__init__()
        loadUi("WindowsGraphics/FindWordlistsWindow.ui", self)
        self.back_to_my_wordlists_button.clicked.connect(self.back_to_my_wordlists_button_function)
        Windows.Windows.find_wordlists_window = self
        self.words_text.setReadOnly(True)
        self.words_text.hide()
        self.find_wordlist_button.clicked.connect(self.search)
        self.add_wordlist_button.clicked.connect(self.add_wordlist_button_function)

    def add_wordlist_button_function(self):
        # TODO
        self.show_dialog()

    def change_displayed_text(self, wordlist: str):
        self.words_text.show()
        self.words_text.clear()
        url: str = "http://" + connection.IP.ip + f":{connection.IP.port}/GetTheListOfAddedWordsFromParticularWordlist"
        response = requests.get(url, headers={'Wordlist': wordlist})
        self.list_of_words_to_add = response.json()
        for word in self.list_of_words_to_add:
            self.words_text.append("• " + word)
        self.words_text.verticalScrollBar().setValue(0)

    def view_words_function(self):  # button's name = word list's name
        sending_button = self.sender()
        name_of_wordlist = sending_button.objectName()
        self.change_displayed_text(name_of_wordlist)

    def clear_last_search_data(self):
        for widget in self.buttonList:
            self.verticalLayout.removeWidget(widget)
        self.buttonList.clear()
        for widget in self.labelList:
            self.verticalLayout.removeWidget(widget)
        self.labelList.clear()
        if self.scroll is not None:
            self.verticalLayout.removeWidget(self.scroll)

    def search(self):
        self.words_text.hide()
        self.clear_last_search_data()
        self.formLayout = QFormLayout()
        self.groupBox = QGroupBox()
        search_text = self.find_wordlist_input.text()

        url1: str = "http://" + connection.IP.ip + f":{connection.IP.port}/FindWordlistsBySubstring"
        response = requests.get(url1, headers={'Substring': search_text, 'UserId': str(connection.IP.user_id)})
        wordlists = response.json()  # wordlists[i] = [wordlist_i, amount_of_words_i]
        i: int = 0
        wordlists.sort(key=lambda x: -x[1])
        for w in wordlists:
            wordlist = w[0]
            index: int = 0
            while wordlist[index] != '_':
                index += 1
            wordlist_without_index = wordlist[index + 1:]
            amount_of_words = w[1]
            self.labelList.append(QLabel(wordlist_without_index))
            self.labelList[i].setStyleSheet("font: 19pt \"Yrsa\";color:white;")
            self.labelList[i].setFixedWidth(400)
            self.buttonList.append(QPushButton("view words (" + str(amount_of_words - 1) + ')'))
            self.buttonList[i].clicked.connect(self.view_words_function)
            self.buttonList[i].setObjectName(wordlist)
            self.buttonList[i].setStyleSheet(Windows.Windows.style_sheet_for_shuffle_button_off)
            self.buttonList[i].setFixedWidth(270)
            self.buttonList[i].setFixedHeight(60)
            self.formLayout.addRow(self.labelList[i], self.buttonList[i])
            i += 1

        self.groupBox.setLayout(self.formLayout)
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.groupBox)
        self.scroll.setWidgetResizable(True)
        self.verticalLayout.addWidget(self.scroll)
        self.setLayout(self.verticalLayout)
        for w in ["scroll", "groupBox"]:
            getattr(self, w).show()

    def show_dialog(self):
        dialog = QInputDialog(self)
        dialog.setLabelText("Name of new wordlist:")
        dialog.setGeometry(300, 300, 400, 450)
        dialog.setWindowTitle(" ")
        dialog.setStyleSheet(
                """ 
                QInputDialog {
                    background-color:rgb(200, 211, 223);
                    color: #333333;
                    font: 21pt "Yrsa";
                    border: 1px solid #87AEDF;
                }
                QInputDialog QLabel {
                    color:black;
                    font: 22pt "Yrsa";
                    background-color:rgb(200, 211, 223);
                }
                QInputDialog QLineEdit {
                    background-color:white;
                    font: 20pt "Yrsa";
                    color:black;
                    selection-background-color: rgb(255, 255, 255);
                    border-style: outset;
                    border-width: 1px;
                    border-radius: 15px;
                    border-color: black;
                    padding: 4px;
                    selection-color: rgb(101, 145, 232);
                }
                QInputDialog QPushButton {
                    background-color: rgb(30, 85, 138);
                    color: #FFFFFF;
                    padding: 6px;
                    border: 1px;
                    font: 20pt "Yrsa";
                }
                QInputDialog QPushButton:hover {
                    background-color: rgb(20, 75, 130);
                }
                QInputDialog QPushButton:pressed {
                    background-color: #426C99;
                }
                """
        )
        answer: int = dialog.exec()
        if answer == 1:
            print(dialog.textValue())

    @staticmethod
    def back_to_my_wordlists_button_function():
        Windows.Windows.find_wordlists_window.hide()
        Windows.Windows.my_wordlists_window.show()
        Windows.Windows.widget.setFocus()
