import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QMessageBox, QVBoxLayout, QHBoxLayout, QSpacerItem, \
    QSizePolicy, QScrollArea
from PyQt5.uic import loadUi
import sqlite3
from PyQt5 import QtCore, QtWidgets

from PyQt5.uic.properties import QtCore

import DataBase
import Word


class SignInWindow(QDialog):
    def __init__(self):
        super(SignInWindow, self).__init__()
        loadUi("SignInWindow.ui", self)
        self.loginbutton.clicked.connect(self.login_button_function)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.sign_up_button_function)

    def keyPressEvent(self, event):
        if event.Enter == 10:
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
        if event.Enter == 10:
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
        self.searchbutton.clicked.connect(self.search_button_function)
        self.pronunciationUSA.clicked.connect(Word.Word.get_the_pronunciation_of_a_word_with_American_accent)
        self.pronunciationUK.clicked.connect(Word.Word.get_the_pronunciation_of_a_word_with_British_accent)
        self.pronunciationUSA.hide()
        self.pronunciationUK.hide()
        self.pronunciationUSAtext.hide()
        self.pronunciationUKtext.hide()
        self.definition.setReadOnly(True)
        self.pronunciationUSAtext.setReadOnly(True)
        self.pronunciationUKtext.setReadOnly(True)


    def search_button_function(self):
        self.definition.clear()
        search_text = self.searchfield.text()
        self.definition.verticalScrollBar().setValue(0)
        Word.Word.current_word = search_text
        self.definition.setReadOnly(True)

        for definition_of_the_word in Word.Word.get_the_meaning_of_a_word():
            self.definition.append(definition_of_the_word)
        self.pronunciationUSA.show()
        self.pronunciationUK.show()
        self.pronunciationUSAtext.show()
        self.pronunciationUKtext.show()
        self.pronunciationUSA.setIcon(QIcon("voiceButtonIcon.png"));
        self.pronunciationUK.setIcon(QIcon("voiceButtonIcon.png"));


    def keyPressEvent(self, event):
        if event.Enter == 10:
            self.search_button_function()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = SignInWindow()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    widget.setFixedWidth(600)
    widget.setFixedHeight(800)
    widget.show()
    sys.exit(app.exec_())
