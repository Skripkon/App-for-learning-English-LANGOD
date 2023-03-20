import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QMessageBox, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.uic import loadUi
import sqlite3
import DataBase

class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.gotocreate)

    def loginfunction(self):
        DataBase.DataBase.check_whether_data_bases_exist()
        login_text = self.email.text()
        password = self.password.text()
        if DataBase.DataBase.check_if_user_exists(login_text, password) != -1:
            self.accept()
            self.window = MainWindow()
            self.window.show()
        else:
            self.open_the_window("ERROR", "Such user hasn't found")


    def gotocreate(self):
        createacc = CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def open_the_window(self, title_of_the_window: str, information: str):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setText(information)
        msg_box.setWindowTitle(title_of_the_window)
        msg_box.setIcon(QtWidgets.QMessageBox.Information)
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg_box.exec_()


class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc, self).__init__()
        loadUi("createacc.ui", self)
        self.signupbutton.clicked.connect(self.createaccfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)


    @classmethod
    def correct_password(cls, password: str) -> str:
        # TODO
        pass

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
            login = Login()
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


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('main.ui', self)

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


app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(1000)
widget.setFixedHeight(1500)
widget.show()
sys.exit(app.exec_())