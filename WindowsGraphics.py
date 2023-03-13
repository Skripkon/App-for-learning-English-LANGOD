import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QMessageBox, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.uic import loadUi


class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.gotocreate)

    def loginfunction(self):
        email = self.email.text()
        password = self.password.text()
        if email == 'a' and password == 'p':
            self.accept()
            self.window = MainWindow()
            self.window.show()
        else:
            print("Wrong username or password")

    def gotocreate(self):
        createacc = CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc, self).__init__()
        loadUi("createacc.ui", self)
        self.signupbutton.clicked.connect(self.createaccfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)

    def createaccfunction(self):
        email = self.email.text()
        if self.password.text() == self.confirmpass.text():
            password = self.password.text()
            msg_box = QtWidgets.QMessageBox()
            msg_box.setText("Krasavchik")
            msg_box.setWindowTitle("Success")
            msg_box.setIcon(QtWidgets.QMessageBox.Information)
            msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg_box.exec_()
            login = Login()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex() + 1)


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