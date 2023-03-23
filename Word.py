from gtts import gTTS
from playsound import playsound
import requests
from reverso_context_api import Client
import shutil
import os
import requests


class Word:
    current_word: str = ""
    name_of_folder_with_pronunciations: str = "sounds"

    @classmethod
    def create_folder_to_store_mp4_files(cls):
        if not os.path.exists(cls.name_of_folder_with_pronunciations):
            os.mkdir(cls.name_of_folder_with_pronunciations)

    @classmethod
    def get_the_meaning_of_a_word(cls):
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{cls.current_word}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()[0]
            meanings = []
            for meaning in data['meanings']:
                part_of_speech = meaning['partOfSpeech']
                definitions = [definition['definition'] for definition in meaning['definitions']]
                meanings.append((part_of_speech, definitions))
            return meanings
        else:
            return "Error"

    @classmethod
    def get_the_usage_of_a_word(cls, number_of_examples=15) -> list[str]:
        client = Client('en', 'ru')
        cnt = 0
        # check whether such word exists
        if len(list(client.get_translations(cls.current_word))) == 0:
            return []
        examples = []
        for example in client.get_translation_samples(cls.current_word, cleanup=True):
            if cnt > number_of_examples:
                break
            examples.append(example[0])
            cnt += 1
        return examples

    @classmethod
    def get_the_pronunciation_of_a_word_with_American_accent(cls):
        target_path_of_the_file = cls.name_of_folder_with_pronunciations + '/' + cls.current_word + "US.mp3"
        if not os.path.exists(target_path_of_the_file):
            pronunciation_of_a_word_with_American_accent = gTTS(cls.current_word, tld="us")
            file_source: str = cls.current_word + "US.mp3"
            pronunciation_of_a_word_with_American_accent.save(file_source)
            shutil.move(file_source, cls.name_of_folder_with_pronunciations)
            playsound(target_path_of_the_file)
        else:
            playsound(target_path_of_the_file)

    @classmethod
    def get_the_pronunciation_of_a_word_with_British_accent(cls):
        target_path_of_the_file = cls.name_of_folder_with_pronunciations + '/' + cls.current_word + "UK.mp3"
        if not os.path.exists(target_path_of_the_file):
            pronunciation_of_a_word_with_British_accent = gTTS(cls.current_word, tld="co.uk")
            file_source: str = cls.current_word + "UK.mp3"
            pronunciation_of_a_word_with_British_accent.save(file_source)
            shutil.move(file_source, cls.name_of_folder_with_pronunciations)
            playsound(target_path_of_the_file)
        else:
            playsound(target_path_of_the_file)

    @classmethod
    def get_the_video_with_a_word(cls):
        phraseEncoded = ""
        for char in cls.current_word:
            if char == ' ':
                phraseEncoded += "%20"
            elif char == "'":
                phraseEncoded += "%27"
            elif char == "!":
                phraseEncoded += "%21"
            elif char == ":":
                phraseEncoded += "%3A"
            else:
                phraseEncoded += char
        URL: str = "https://yarn.co/yarn-find?text=" + phraseEncoded
        request = requests.get(URL)
        HTML: str = request.text
        index: int = request.text.find('/yarn-clip/') + 11
        video_url: str = ""
        while (HTML[index] != '"'):
            video_url += HTML[index]
            index += 1
        new_request_URL: str = "https://y.yarn.co/" + video_url + ".mp4"
        new_request = requests.get(new_request_URL)
        name: str = cls.current_word + ".mp4"
        file = open(name, "wb")
        file.write(new_request.content)
        file.close()
