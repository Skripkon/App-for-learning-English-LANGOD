from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
import sqlite3
from PyQt5 import QtWidgets
import DataBase
from WindowsGraphics import Windows


class SignUpWindow(QDialog):
    __metaclass__ = Windows
    def __init__(self):
        super(SignUpWindow, self).__init__()
        loadUi("WindowsGraphics/SignUpWindow.ui", self)
        self.signupbutton.clicked.connect(self.create_new_user_button_function)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)
        Windows.Windows.sign_up_window = self

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
            Windows.Windows.sign_in_window.show()
            self.hide()
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
