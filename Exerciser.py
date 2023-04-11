import random
import DataBase


class Exerciser:
    dict_of_added_words: dict = {}
    array_of_added_words = []

    def __init__(self):
        DataBase.DataBase.set_the_list_of_added_words()

    # random shuffle algorithm
    @staticmethod
    def random_shuffle(words: list[str]):
        for index in range(len(words)):
            random_index = random.randint(0, index)
            words[index], words[random_index] = \
                words[random_index], words[index]
