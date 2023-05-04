import random
import requests
import connection


class Exerciser:
    dict_of_added_words: dict = {}
    array_of_words_for_exercise: list[str] = []

    def __init__(self):
        Exerciser.dict_of_added_words.clear()
        url1: str = "http://" + connection.IP.ip + f":{connection.IP.port}/GetTheListOfAddedWords"
        response = requests.get(url1, headers={'UserId': str(connection.IP.user_id)})
        Exerciser.dict_of_added_words = response.json()

    # random shuffle algorithm
    @staticmethod
    def random_shuffle(words: list[str]):
        for index in range(len(words)):
            random_index = random.randint(0, index)
            words[index], words[random_index] = \
                words[random_index], words[index]
