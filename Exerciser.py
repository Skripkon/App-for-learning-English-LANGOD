import random

import DataBase


class Exerciser:
    current_list_of_added_words: dict = {}
    current_array_of_added_words = []
    index_of_the_current_word = 0
    # the following two variables are needed to
    # return from the shuffled order to the ordered one
    copy_index_of_the_current_word = 0
    copy_array_of_added_words = []

    def __init__(self):
        DataBase.DataBase.set_the_list_of_added_words()

    # random shuffle algorithm
    @classmethod
    def random_shuffle(cls):
        for index in range (len(cls.current_array_of_added_words)):
            random_index = random.randint(0, index)
            cls.current_array_of_added_words[index], cls.current_array_of_added_words[random_index] = \
                cls.current_array_of_added_words[random_index], cls.current_array_of_added_words[index]
