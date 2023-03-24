import DataBase


class Exerciser:
    current_list_of_added_words = []
    def __init__(self):
        DataBase.DataBase.set_the_list_of_added_words()
        print(self.current_list_of_added_words)


