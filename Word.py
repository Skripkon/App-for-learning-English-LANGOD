from gtts import gTTS
from playsound import playsound
import requests
from reverso_context_api import Client
import shutil
import os
import requests
from nltk.corpus import wordnet


class Word:
    current_word: str = ""
    name_of_folder_with_pronunciations: str = "sounds"
    client = Client('en', 'ru')

    @classmethod
    def create_folder_to_store_mp4_files(cls):
        if not os.path.exists(cls.name_of_folder_with_pronunciations):
            os.mkdir(cls.name_of_folder_with_pronunciations)

    @classmethod
    def get_the_meaning_of_a_word(cls):
        output = ""
        synsets = wordnet.synsets(cls.current_word)
        for synset in synsets:
            pos = synset.pos()
            output += "["
            output += pos
            output += "] "
            definition = synset.definition()
            output += definition
            output += "\n"
        return output

    @classmethod
    def check_whether_the_word_is_valid(cls):
        if len(list(cls.client.get_translations(cls.current_word))) == 0:
            return False
        return True

    @classmethod
    def get_the_usage_of_a_word(cls, number_of_examples=15) -> str:
        cnt = 0
        output = ""
        for example in cls.client.get_translation_samples(cls.current_word, cleanup=True):
            if cnt > number_of_examples:
                break
            output += '- '
            output += example[0]
            output += '\n'
            cnt += 1
        return output

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
