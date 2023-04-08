import os
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets
from WindowsGraphics import SignInWindow, Windows, SignUpWindow
import nltk


def download_data():
    nltk.download('wordnet')
    nltk.download('words')


if __name__ == "__main__":
    # first time you have to download this DataBase in order to use the App
    # download_data()
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