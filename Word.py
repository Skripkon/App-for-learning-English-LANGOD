from gtts import gTTS
from playsound import playsound
import requests

class Word:
    current_word: str = ""
        
        
    @classmethod
    def get_the_meaning_of_a_word(cls):
        pass
    
    
    @classmethod
    def get_the_usage_of_a_word(cls):
        pass
    
    
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
