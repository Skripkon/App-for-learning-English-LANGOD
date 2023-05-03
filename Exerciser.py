import random
import requests
import connection
import json


class Exerciser:
    dict_of_added_words: dict = {}
    array_of_added_words = []
    dict_of_wordlists: dict = {}
    array_of_created_wordlists = []

    def __init__(self):
        # DataBase.DataBase.set_the_list_of_added_words()
        Exerciser.dict_of_added_words.clear()
        Exerciser.array_of_added_words.clear()
        Exerciser.array_of_created_wordlists.clear()
        url1: str = "http://" + connection.IP.ip + f":{connection.IP.port}/GetTheListOfAddedWords"
        response = requests.get(url1, headers={'UserId': str(connection.IP.user_id)})
        Exerciser.dict_of_wordlists = json.loads(response.text)
        Exerciser.array_of_added_words = list(Exerciser.dict_of_wordlists.keys())
        print(Exerciser.array_of_added_words)
        print(Exerciser.dict_of_wordlists)
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
