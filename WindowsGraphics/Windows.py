import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox


class Windows:
    widget: PyQt5.QtWidgets.QStackedWidget = None
    sign_in_window = None
    sign_up_window = None
    search_window = None
    exerciser_window = None
    revision_mode_window = None
    flashcards_mode_window = None
    context_mode_window = None
    my_wordlists_window = None

    @staticmethod
    def open_the_window(title_of_the_window: str, information: str):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setText(information)
        msg_box.setWindowTitle(title_of_the_window)
        msg_box.setIcon(QtWidgets.QMessageBox.Information)
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg_box.exec_()

    @staticmethod
    def open_window_after_all_words_reviewed() -> str:
        message_box = QMessageBox()
        message_box.setWindowTitle("A study completed")
        message_box.setText("You went over all of your words!\n"
                            "\nYou might review your words again or try other mods!")
        message_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        buttonContinue = message_box.button(QMessageBox.Ok)
        buttonContinue.setText('Continue')
        buttonExit = message_box.button(QMessageBox.Cancel)
        buttonExit.setText('Exit')

        message_box.setStyleSheet(
            """
            QMessageBox {
                background-color: #E8F1FD;
                color: #333333;
                font: 19pt "Yrsa";
                border: 1px solid #87AEDF;
            }
            QMessageBox QLabel {
                color: #333333;
                font: 19pt "Yrsa";
            }
            QMessageBox QPushButton {
                background-color: #87AEDF;
                color: #FFFFFF;
                padding: 6px;
                border: 1px;
                font: 19pt "Yrsa";
            }
            QMessageBox QPushButton:hover {
                background-color: #6393C3;
            }
            QMessageBox QPushButton:pressed {
                background-color: #426C99;
            }
            """
        )
        message_box.exec()
        if message_box.clickedButton() == buttonContinue:
            return "continue"
        elif message_box.clickedButton() == buttonExit:
            return "break"
