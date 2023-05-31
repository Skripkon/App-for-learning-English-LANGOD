import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
import Exerciser
import math

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
    find_wordlists_window = None
    style_sheet_for_button: str = "selection-background-color: rgb(255, 255, 255);" \
                                  "border-style: outset;" \
                                  "border-width: 1px;" \
                                  "border-radius: 15px;" \
                                  "border-color: black;" \
                                  "padding: 4px;}" \
                                  "QPushButton:hover {background-color: rgb(20, 75, 130);}"

    style_sheet_for_shuffle_button_off = "QPushButton {" \
                                         "background-color:rgb(30, 85, 138);" \
                                         "font: 19pt \"Yrsa\";" \
                                         "color:white; " + style_sheet_for_button
    style_sheet_for_shuffle_button_on = "QPushButton {" \
                                        "background-color:rgb(30, 85, 138);" \
                                        "font: 19pt \"Yrsa\";" \
                                        "color:yellow; " + style_sheet_for_button

    @staticmethod
    def open_the_window(title_of_the_window: str, information: str):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setText(information)
        msg_box.setWindowTitle(title_of_the_window)
        msg_box.setIcon(QtWidgets.QMessageBox.Information)
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg_box.exec_()

    @classmethod
    def open_window_after_all_words_reviewed(cls, array_of_mistakes: list[str]) -> str:
        message_box = QMessageBox()
        percent_of_right_answers = 100 - 100 * round(len(array_of_mistakes) / len(Exerciser.Exerciser.array_of_words_for_exercise), 2)
        message_box.setWindowTitle(f"A study completed, your result is {percent_of_right_answers}%")
        if percent_of_right_answers == 100:
            message_box.setText("You went over all of your words!\n"
                                "\nYou might review all your words again or try other mods!")
            message_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        else:
            message_box.setText("You went over all of your words!\n"
                                "\nYou might review your words again, revise mistake words or try other mods!")
            message_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Retry | QMessageBox.Cancel)
            buttonRevise = message_box.button(QMessageBox.Retry)
            buttonRevise.setText('Retry')
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
        else:
            return "revise"
