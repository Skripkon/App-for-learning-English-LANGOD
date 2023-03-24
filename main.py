import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets

import DataBase
from WindowsGraphics import SignInWindow, Windows, SignUpWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    SignInWindow.SignInWindow()
    Windows.Windows.widget = QtWidgets.QStackedWidget()
    Windows.Windows.widget.addWidget(Windows.Windows.sign_in_window)
    Windows.Windows.widget.setFixedWidth(1200)
    Windows.Windows.widget.setFixedHeight(800)
    Windows.Windows.widget.setWindowTitle("LaNGod")
    Windows.Windows.widget.show()
    sys.exit(app.exec_())

