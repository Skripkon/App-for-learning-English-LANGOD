import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QMessageBox, QVBoxLayout, QHBoxLayout, QSpacerItem, \
    QSizePolicy, QScrollArea
from PyQt5.uic import loadUi
import sqlite3
from PyQt5 import QtCore, QtWidgets
from time import time
from PyQt5.uic.properties import QtCore
import DataBase
import Word


def time_required(f):
    last = [time()]

    def decorator():
        if time() - last[0] < 1:
            return None
        last[0] = time()
        return f()

    return decorator


class SignInWindow(QDialog):
    def __init__(self):
        super(SignInWindow, self).__init__()
        loadUi("SignInWindow.ui", self)
        self.loginbutton.clicked.connect(self.login_button_function)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.sign_up_button_function)

    def keyPressEvent(self, event):
        if event.nativeScanCode() == 36:  # button Enter pressed
            self.login_button_function()

    def login_button_function(self):
        DataBase.DataBase.check_whether_data_bases_exist()
        login_text = self.email.text()
        password = self.password.text()
        if DataBase.DataBase.check_if_user_exists(login_text, password) != -1:
            search = SearchWindow()
            widget.addWidget(search)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        else:
            self.open_the_window("ERROR", "Such user hasn't found")

    @classmethod
    def sign_up_button_function(cls):
        sign_up = SignUpWindow()
        widget.addWidget(sign_up)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    @classmethod
    def open_the_window(cls, title_of_the_window: str, information: str):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setText(information)
        msg_box.setWindowTitle(title_of_the_window)
        msg_box.setIcon(QtWidgets.QMessageBox.Information)
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg_box.exec_()


class SignUpWindow(QDialog):
    def __init__(self):
        super(SignUpWindow, self).__init__()
        loadUi("SignUpWindow.ui", self)
        self.signupbutton.clicked.connect(self.create_new_user_button_function)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)

    @classmethod
    def correct_password(cls, password: str) -> str:
        # TODO
        return "NO ERROR"

    def keyPressEvent(self, event):
        if event.nativeScanCode() == 36:  # button Enter pressed
            self.create_new_user_button_function()

    def create_new_user_button_function(self):
        DataBase.DataBase.check_whether_data_bases_exist()
        login_text = self.email.text()
        if self.password.text() == self.confirmpass.text():
            password = self.password.text()
            is_password_correct: str = self.correct_password(password)
            if is_password_correct != "NO ERROR":
                self.open_the_window("Error", is_password_correct)
                return None
            try:
                DataBase.DataBase.create_user(login_text, password)
            except sqlite3.Error:
                self.open_the_window("Error", "User with this login already exists")
                return None
            self.open_the_window("OK", "Have fun using our app!")
            login = SignInWindow()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        else:
            self.open_the_window("Error", "Passwords aren't the same")

    def open_the_window(self, title_of_the_window: str, information: str):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setText(information)
        msg_box.setWindowTitle(title_of_the_window)
        msg_box.setIcon(QtWidgets.QMessageBox.Information)
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg_box.exec_()
        self.password.clear()
        self.confirmpass.clear()


class SearchWindow(QMainWindow):
    def __init__(self):
        super(SearchWindow, self).__init__()
        loadUi('SearchWindow.ui', self)
        self.connect_interface_with_functions()
        self.forbid_to_change_the_interface()
        self.hide_the_interface()
        self.pronunciationUSA.setIcon(QIcon("voiceButtonIcon.png"))
        self.pronunciationUK.setIcon(QIcon("voiceButtonIcon.png"))
        Word.Word.create_folder_to_store_mp4_files()  # check whether necessary folder exists

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = SignInWindow()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(MainWindow)
    widget.setFixedWidth(600)
    widget.setFixedHeight(800)
    widget.show()
    sys.exit(app.exec_())
