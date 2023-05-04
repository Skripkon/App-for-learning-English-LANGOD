import random
import requests
import connection


class Exerciser:
    dict_of_added_words: dict = {}
    array_of_created_wordlists = []

    def __init__(self):
        # DataBase.DataBase.set_the_list_of_added_words()
        Exerciser.dict_of_added_words.clear()
        url1: str = "http://" + connection.IP.ip + f":{connection.IP.port}/GetTheListOfAddedWords"
        response = requests.get(url1, headers={'UserId': str(connection.IP.user_id)})
        self.dict_of_added_words = response.json()
        url2: str = "http://" + connection.IP.ip + f":{connection.IP.port}/GetTheListOfAddedWordlists"
        response = requests.get(url2, headers={'UserId': str(connection.IP.user_id)})
        Exerciser.array_of_created_wordlists = response.text.split()


    # random shuffle algorithm
    @staticmethod
    def random_shuffle(words: list[str]):
        for index in range(len(words)):
            random_index = random.randint(0, index)
            words[index], words[random_index] = \
                words[random_index], words[index]
