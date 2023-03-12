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
        USA.save('USA.mp3')
        playsound("USA.mp3")
    
    
    @classmethod
    def get_the_pronunciation_of_a_word_with_British_accent(cls):
        pronunciation_of_a_word_with_British_accen = gTTS(cls.current_word, tld="en")
        file: str = cls.current_word + "UK.mp3"
        USA.save('UK.mp3')
        playsound("UK.mp3")
    
    
    @classmethod
    def get_the_video_with_a_word(cls):
        pass
