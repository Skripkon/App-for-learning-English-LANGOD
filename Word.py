from gtts import gTTS
from playsound import playsound
import requests
from reverso_context_api import Client
from PyDictionary import PyDictionary


class Word:
    api_key = "12371fe7-2adf-4ced-9985-1ce6bd6ba9b0"
    current_word: str = ""
        
        
    @classmethod
    def get_the_meaning_of_a_word(cls):
        url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{cls.current_word}?key={cls.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                definitions = data[0].get('shortdef', [])
                return definitions
        return []

    @classmethod
    def get_the_usage_of_a_word(cls, number_of_examples=10) -> list[str]:
        client = Client('en', 'ru')
        cnt = 0
        examples = []
        for example in client.get_translation_samples(cls.current_word, cleanup=True):
            if cnt > number_of_examples:
                break
            examples.append(example[0])
            cnt += 1
        return examples
    
    # def get_the_meaning_of_a_word(self) -> dict:
    #     dict = PyDictionary()
    #     return dict.meaning(self.word)
    
    @classmethod
    def get_the_pronunciation_of_a_word_with_American_accent(cls):
        pronunciation_of_a_word_with_American_accent = gTTS(cls.current_word, tld="us")
        file: str = cls.current_word + "US.mp3"
        pronunciation_of_a_word_with_American_accent.save(file)
        playsound(file)
    
    
    @classmethod
    def get_the_pronunciation_of_a_word_with_British_accent(cls):
        pronunciation_of_a_word_with_British_accent = gTTS(cls.current_word, tld="co.uk")
        file: str = cls.current_word + "UK.mp3"
        pronunciation_of_a_word_with_British_accent.save(file)
        playsound(file)
    
    
    @classmethod
    def get_the_video_with_a_word(cls):
        phraseEncoded = ""
        for char in cls.current_word:
            if (char == ' '):
                phraseEncoded += "%20"
            elif (char == "'"):
                phraseEncoded += "%27"
            elif (char == "!"):
                phraseEncoded += "%21"
            elif (char == ":"):
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
        file=open(name,"wb")
        file.write(new_request.content)
        file.close()
