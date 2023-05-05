import PyQt5
from PyQt5 import QtWidgets


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

    @classmethod
    def open_the_window(cls, title_of_the_window: str, information: str):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setText(information)
        msg_box.setWindowTitle(title_of_the_window)
        msg_box.setIcon(QtWidgets.QMessageBox.Information)
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg_box.exec_()
