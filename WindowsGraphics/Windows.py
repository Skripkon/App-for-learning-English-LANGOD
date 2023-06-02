from time import time

import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
import Exerciser
import math
from time import time

import Word


class Windows:
    widget: PyQt5.QtWidgets.QStackedWidget = None
    sign_in_window = None
    sign_up_window = None
    search_window = None
    exerciser_window = None
    revision_mode_window = None
    flashcards_mode_window = None
    context_mode_window = None
    audition_mode_window = None
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
    style_sheet_for_message_box = \
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
    style_sheet_for_input_field: str = 'font: 19pt "Yrsa";' \
                                       'color:black;' \
                                       'selection-background-color:' \
                                       'rgb(255, 255, 255);' \
                                       'border-style: outset;' \
                                       'border-width: 1px;' \
                                       'border-radius: 15px;' \
                                       'border-color: black;' \
                                       'padding: 4px;' \
                                       'selection-color: rgb(101, 145, 232);'
    style_sheet_after_correct_answer = 'background-color:rgb(205, 247, 190);' + style_sheet_for_input_field
    style_sheet_by_default = 'background-color:rgb(200, 211, 223);' + style_sheet_for_input_field
    style_sheet_after_wrong_answer = 'background-color:rgb(255, 192, 192);' + style_sheet_for_input_field

    @classmethod
    def open_the_window(cls, title_of_the_window: str, information: str):  # mostly for errors
        msg_box = QtWidgets.QMessageBox()
        msg_box.setText(information)
        msg_box.setWindowTitle(title_of_the_window)
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg_box.setStyleSheet(cls.style_sheet_for_message_box)
        msg_box.exec_()

    @classmethod
    def open_window_after_all_words_reviewed(cls, len_of_array_of_mistakes: int, len_of_words: int) -> str:
        message_box = QMessageBox()
        percent_of_right_answers = 100 - 100 * round(len_of_array_of_mistakes / len_of_words, 2)
        message_box.setWindowTitle(" ")
        message_box.setText("You went over all of your words!\n"
                            f"Your result is {percent_of_right_answers} %\n")
        if percent_of_right_answers == 100:
            message_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        else:
            message_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Retry | QMessageBox.Cancel)
            buttonRevise = message_box.button(QMessageBox.Retry)
            buttonRevise.setText('Learn your mistakes')
        buttonContinue = message_box.button(QMessageBox.Ok)
        buttonContinue.setText('Restart')
        buttonExit = message_box.button(QMessageBox.Cancel)
        buttonExit.setText('Exit')

        message_box.setStyleSheet(cls.style_sheet_for_message_box)
        message_box.exec()
        if message_box.clickedButton() == buttonContinue:
            return "Restart"
        elif message_box.clickedButton() == buttonExit:
            return "break"
        else:
            return "Learn your mistakes"

    @classmethod
    def play_sound_with_uk_accent(cls):
        cls.time_required(Word.Word.get_the_pronunciation_of_a_word_with_British_accent())
        # getattr(Windows, window).setFocus()
        Windows.widget.setFocus()

    @classmethod
    def play_sound_with_us_accent(cls):
        cls.time_required(Word.Word.get_the_pronunciation_of_a_word_with_American_accent())
        # getattr(Windows, window).setFocus()
        Windows.widget.setFocus()

    @staticmethod
    def time_required(f):
        last = [time()]

        def decorator():
            if time() - last[0] < 1:
                return None
            last[0] = time()
            return f()

        return decorator
