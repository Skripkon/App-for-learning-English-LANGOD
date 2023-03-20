import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QMessageBox, QVBoxLayout, QHBoxLayout, QSpacerItem, \
    QSizePolicy
from PyQt5.uic import loadUi
import sqlite3
import DataBase


class SignUpWindow(QDialog):
    def __init__(self):
        super(SignUpWindow, self).__init__()
        loadUi("SignUpWindow.ui", self)
        self.loginbutton.clicked.connect(self.login_button_function)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.sign_in_button_function)

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
    def sign_in_button_function(cls):
        sign_in = SignInWindow()
        widget.addWidget(sign_in)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    @classmethod
    def open_the_window(cls, title_of_the_window: str, information: str):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setText(information)
        msg_box.setWindowTitle(title_of_the_window)
        msg_box.setIcon(QtWidgets.QMessageBox.Information)
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg_box.exec_()


class SignInWindow(QDialog):
    def __init__(self):
        super(SignInWindow, self).__init__()
        loadUi("SignInWindow.ui", self)
        self.signupbutton.clicked.connect(self.createaccfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)

    @classmethod
    def correct_password(cls, password: str) -> str:
        # TODO
        return "NO ERROR"

    def createaccfunction(self):
        DataBase.DataBase.check_whether_data_bases_exist()
        login_text = self.email.text()
        if self.password.text() == self.confirmpass.text():
            password = self.password.text()
            IsPasswordCorrect: str = self.correct_password(password)
            if IsPasswordCorrect != "NO ERROR":
                self.open_the_window("Error", IsPasswordCorrect)
                return None
            try:
                DataBase.DataBase.create_user(login_text, password)
            except sqlite3.Error:
                self.open_the_window("Error", "User with this login already exists")
                return None
            self.open_the_window("OK", "Have fun using our app!")
            login = SignUpWindow()
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

        self.vlayout = QVBoxLayout()
        self.hlayout = QHBoxLayout()

        self.vlayout.addWidget(self.searchfield)
        self.vlayout.addWidget(self.searchbutton)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.vlayout.addItem(spacer)

        self.hlayout.addLayout(self.vlayout)
        self.hlayout.addStretch()
        self.centralWidget = QtWidgets.QWidget()
        self.centralWidget.setLayout(self.hlayout)
        self.setCentralWidget(self.centralWidget)

        self.searchbutton.clicked.connect(self.search)

    def search(self):
        search_text = self.searchfield.text()
        msgBox = QMessageBox()
        msgBox.setText(search_text)
        msgBox.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = SignUpWindow()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    widget.setFixedWidth(600)
    widget.setFixedHeight(800)
    widget.show()
    sys.exit(app.exec_())
