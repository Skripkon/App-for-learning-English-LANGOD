import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets
from nltk.corpus import wordnet
import connection
from WindowsGraphics import SignInWindow, Windows
import nltk


def download_data():
    nltk.download('wordnet')
    nltk.download('words')


def set_connection():
    wordnet.synsets("connect")


if __name__ == "__main__":
    # first time you have to download this DataBase in order to use the App
    # download_data()
    set_connection()
    connection.IP.set_ip()
    app = QApplication(sys.argv)
    SignInWindow.SignInWindow()
    Windows.Windows.widget = QtWidgets.QStackedWidget()
    Windows.Windows.widget.addWidget(Windows.Windows.sign_in_window)
    Windows.Windows.widget.setFixedWidth(1200)
    Windows.Windows.widget.setFixedHeight(800)
    Windows.Windows.widget.setWindowTitle("LaNGod")
    Windows.Windows.widget.show()
    Windows.Windows.widget.setFocus()
    sys.exit(app.exec_())
