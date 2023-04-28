from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
import sqlite3
from PyQt5 import QtWidgets
import connection
from WindowsGraphics import Windows
import requests
import connection


class SignUpWindow(QDialog):

    def __init__(self):
        super(SignUpWindow, self).__init__()
        loadUi("WindowsGraphics/SignUpWindow.ui", self)
        self.signupbutton.clicked.connect(self.create_new_user_button_function)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)
        Windows.Windows.sign_up_window = self
        self.back_to_sign_in_button.clicked.connect(self.back_to_sign_in_button_function)

    @staticmethod
    def back_to_sign_in_button_function():
        Windows.Windows.sign_up_window.hide()
        Windows.Windows.sign_in_window.show()
        Windows.Windows.sign_up_window.setFocus()

    @staticmethod
    def correct_password_and_login(password: str, login: str) -> str:
        if len(password) < 6:
            return "Too short password (You have to use 6 or more symbols)"
        if len(password) > 20:
            return "Too long password (You have to use no more than 20 characters)"
        if len(login) == 0:
            return "Login field cannot be empty"
        if len(login) > 20:
            return "Too long login (You need to use no more than 20 characters)"
        for i in range(len(login)):
            ord_login = ord(login[i])
            if not (47 < ord_login < 58 or 64 < ord_login < 91 or 96 < ord_login < 123):
                return "Login contains incorrect symbol"
        for i in range(len(password)):
            ord_pass = ord(password[i])
            if not (47 < ord_pass < 58 or 64 < ord_pass < 91 or 96 < ord_pass < 123):
                return "Password contains unacceptable symbol"
        if login == password:
            return "Password and login are the same"
        return "NO ERROR"

    def keyPressEvent(self, event):
        if event.nativeScanCode() == 36:  # button Enter pressed
            self.create_new_user_button_function()

    def create_new_user_button_function(self):
        # DataBase.DataBase.check_whether_data_bases_exist()
        URL: str = "http://" + connection.IP.ip + ":12345/CreateDB"
        response = requests.get(URL)
        login_text = self.email.text()
        if self.password.text() == self.confirmpass.text():
            password = self.password.text()
            is_password_correct: str = self.correct_password_and_login(password, login_text)
            if is_password_correct != "NO ERROR":
                self.open_the_window("Error", is_password_correct)
                return None
            try:
                # DataBase.DataBase.create_user(login_text, password)
                URL: str = "http://" + connection.IP.ip + ":12345/SignUp"
                response = requests.get(URL, headers={"Login":login_text, "Password":password})
            except sqlite3.Error:
                self.open_the_window("Error", "User with this login already exists")
                return None
            self.open_the_window("OK", "Have fun using our app!")
            Windows.Windows.sign_in_window.show()
            self.hide()
        else:
            self.open_the_window("Error", "Passwords aren't the same")
        Windows.Windows.sign_up_window.setFocus()

    def open_the_window(self, title_of_the_window: str, information: str):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setText(information)
        msg_box.setWindowTitle(title_of_the_window)
        msg_box.setIcon(QtWidgets.QMessageBox.Information)
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg_box.exec_()
        self.password.clear()
        self.confirmpass.clear()
        Windows.Windows.sign_up_window.setFocus()