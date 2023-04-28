import random
import requests
import connection


class Exerciser:
    dict_of_added_words: dict = {}
    array_of_added_words = []

    def __init__(self):
        # DataBase.DataBase.set_the_list_of_added_words()
        Exerciser.dict_of_added_words.clear()
        Exerciser.array_of_added_words.clear()
        URL: str = "http://" + connection.IP.ip + ":12345/GetTheListOfAddedWords"
        response = requests.get(URL)
        Exerciser.array_of_added_words = response.text.split()
        for i in range(0, len(Exerciser.array_of_added_words)):
            Exerciser.dict_of_added_words[Exerciser.array_of_added_words[i]] = i + 1

    # random shuffle algorithm
    @staticmethod
    def random_shuffle(words: list[str]):
        for index in range(len(words)):
            random_index = random.randint(0, index)
            words[index], words[random_index] = \
                words[random_index], words[index]
