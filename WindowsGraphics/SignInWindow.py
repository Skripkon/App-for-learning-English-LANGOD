from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
import Exerciser
import connection
from WindowsGraphics import Windows, SearchWindow, SignUpWindow
import requests


class SignInWindow(QDialog):

    def __init__(self):
        super(SignInWindow, self).__init__()
        loadUi("WindowsGraphics/SignInWindow.ui", self)
        self.loginbutton.clicked.connect(self.login_button_function)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.sign_up_button_function)
        Windows.Windows.sign_in_window = self

    def keyPressEvent(self, event):
        if event.nativeScanCode() == 36:  # button Enter pressed
            self.login_button_function()

    def login_button_function(self):
        url: str = "http://" + connection.IP.ip + f":{connection.IP.port}/CreateDB"
        requests.get(url)
        login_text = self.email.text()
        password = self.password.text()

        URL: str = "http://" + connection.IP.ip + f":{connection.IP.port}/CheckIfUserExists"
        response = requests.get(URL, headers={"Login": login_text, "Password": password})
        if response.text != "-1":
            connection.IP.user_id = int(response.text)
            Exerciser.Exerciser()

            if Windows.Windows.search_window is None:
                SearchWindow.SearchWindow()
                Windows.Windows.widget.addWidget(Windows.Windows.search_window)
                Windows.Windows.widget.setCurrentIndex(Windows.Windows.widget.currentIndex() + 1)
            Windows.Windows.sign_in_window.hide()
            Windows.Windows.search_window.show()
            Windows.Windows.widget.setFocus()
        else:
            Windows.Windows.open_the_window("ERROR", "Such user hasn't found")
        Windows.Windows.sign_in_window.setFocus()

    def sign_up_button_function(self):
        if Windows.Windows.sign_up_window is None:
            SignUpWindow.SignUpWindow()
            Windows.Windows.widget.addWidget(Windows.Windows.sign_up_window)
            Windows.Windows.widget.setCurrentIndex(Windows.Windows.widget.currentIndex() + 1)
        Windows.Windows.sign_up_window.show()
        Windows.Windows.sign_in_window.hide()
        self.email.clear()
        self.password.clear()
        Windows.Windows.widget.setFocus()
