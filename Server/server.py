import asyncio
import os
import sqlite3
import tornado
from tornado import web
import json
import socket


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


class DataBase:
    sqlite_connection_with_db_registration_info = None
    cursor_for_registration_info = None
    cursor_for_list_of_wordlists = None
    sqlite_connection_with_db_list_of_wordlists = None
    cursor_for_words_in_wordlists = None
    sqlite_connection_with_db_words_in_wordlists = None


class AddNewWordHandler(tornado.web.RequestHandler):
    @classmethod
    def add_new_word(cls, word: str, user_id: str, wordlist: str) -> int:
        name: str = user_id + '_' + wordlist
        temp = DataBase.cursor_for_words_in_wordlists.execute(
            "SELECT amount_of_words FROM words_in_wordlists WHERE id_wordlist=?",
            (name,))
        n: int = temp.fetchone()[0]
        number_of_new_word = "word" + str(n)
        sqlite_add_word_query = f"UPDATE words_in_wordlists SET {number_of_new_word}=?, " \
                                f"amount_of_words = amount_of_words + 1 WHERE id_wordlist=?"
        DataBase.cursor_for_words_in_wordlists.execute(sqlite_add_word_query, (word, name))
        DataBase.sqlite_connection_with_db_words_in_wordlists.commit()
        return n

    def get(self):
        word = self.request.headers["Word"]
        user_id = self.request.headers["UserId"]
        wordlist = self.request.headers["Wordlist"]
        n: int = self.add_new_word(word, user_id, wordlist)
        self.write(str(n))


class GetTheListOfAddedWordsFromParticularWordlistHandler(tornado.web.RequestHandler):
    words_str: str = ""

    @classmethod
    def get_the_list_of_words(cls, name_of_wordlist: str):
        words: list[str] = []
        for i in range(1, 301):
            current_word = 'word' + str(i)
            sqlite_query = f'SELECT {current_word} FROM words_in_wordlists WHERE id_wordlist=?'
            temp_word = DataBase.cursor_for_words_in_wordlists.execute(sqlite_query,
                                                                       (name_of_wordlist,)).fetchone()
            if temp_word[0] is not None:
                words.append(temp_word[0])
            else:
                break
        cls.words_str = json.dumps(words)

    def get(self):
        name_of_wordlist: str = self.request.headers["Wordlist"]
        self.get_the_list_of_words(name_of_wordlist=name_of_wordlist)
        self.write(self.words_str)


class GetTheListOfAddedWordsHandler(tornado.web.RequestHandler):
    words_str: str = ""
    privacy_types_str: str = ""

    @classmethod
    def get_the_list_of_added_words(cls, user_id):
        query = 'SELECT id_wordlist, privacy FROM words_in_wordlists WHERE id_wordlist LIKE \'' + user_id + '%\''
        list_of_wordlists = DataBase.cursor_for_words_in_wordlists.execute(query).fetchall()
        dict_of_wordlists = {}
        dict_of_privacies = {}
        for wordlist in list_of_wordlists:
            name_of_wordlist_with_index = wordlist[0]
            type_of_privacy: str = wordlist[1]
            start_index: int = len(user_id) + 1
            name_of_wordlist = name_of_wordlist_with_index[start_index::]
            for i in range(1, 301):
                current_word = 'word' + str(i)
                sqlite_query = f'SELECT {current_word} FROM words_in_wordlists WHERE id_wordlist=?'
                temp_word = DataBase.cursor_for_words_in_wordlists.execute(sqlite_query,
                                                                           (name_of_wordlist_with_index,)).fetchone()
                if temp_word[0] is not None:
                    if name_of_wordlist not in dict_of_wordlists:
                        dict_of_wordlists[name_of_wordlist] = [temp_word[0]]
                        dict_of_privacies[name_of_wordlist] = type_of_privacy
                    else:
                        dict_of_wordlists[name_of_wordlist].append(temp_word[0])
                elif name_of_wordlist not in dict_of_wordlists:
                    dict_of_wordlists[name_of_wordlist] = []
                    dict_of_privacies[name_of_wordlist] = type_of_privacy
                    break
                else:
                    break
        cls.words_str = json.dumps([dict_of_wordlists, dict_of_privacies])

    def get(self):
        user_id = self.request.headers["UserId"]
        self.get_the_list_of_added_words(user_id)
        self.write(self.words_str)


class AddNewWordlistHandler(tornado.web.RequestHandler):
    @classmethod
    def add_new_wordlist(cls, user_id: str, wordlist: str):
        user_id = int(user_id)
        temp = DataBase.cursor_for_list_of_wordlists.execute(
            "SELECT amount_of_wordlists FROM list_of_wordlists WHERE id=?",
            (user_id,))
        n: int = temp.fetchone()[0]
        number_of_new_wordlist = "wordlist" + str(n)
        sqlite_add_wordlist_query = f"UPDATE list_of_wordlists SET {number_of_new_wordlist}=?, " \
                                    f"amount_of_wordlists = amount_of_wordlists + 1 WHERE id=?"
        DataBase.cursor_for_list_of_wordlists.execute(sqlite_add_wordlist_query, (wordlist, user_id))
        DataBase.sqlite_connection_with_db_list_of_wordlists.commit()

        name: str = str(user_id) + '_' + wordlist
        DataBase.cursor_for_words_in_wordlists.execute(
            "INSERT INTO words_in_wordlists (id_wordlist) VALUES(?)", (name,))
        DataBase.sqlite_connection_with_db_words_in_wordlists.commit()
        return n

    def get(self):
        user_id = self.request.headers["UserId"]
        wordlist: str = self.request.headers['Wordlist']
        self.add_new_wordlist(user_id, wordlist)


class CheckIfUserExistsHandler(tornado.web.RequestHandler):
    @staticmethod
    def check_if_user_exists(login_text: str, password: str) -> str:
        info = DataBase.cursor_for_registration_info.execute(
            "SELECT id FROM registration_info WHERE login=? and password=?",
            (login_text, password))
        response = info.fetchone()
        if response is None:
            return "-1"
        else:
            return str(response[0])

    def get(self):
        login = self.request.headers["Login"]
        password = self.request.headers["Password"]
        response: str = self.check_if_user_exists(login, password)
        self.write(response)


class SignUpHandler(tornado.web.RequestHandler):
    @classmethod
    def create_user(cls, new_login: str, new_password: str) -> str:
        try:
            DataBase.cursor_for_registration_info.execute(
                "INSERT INTO registration_info (login, password) VALUES(?, ?)",
                (new_login, new_password))
            DataBase.sqlite_connection_with_db_registration_info.commit()
            DataBase.cursor_for_list_of_wordlists.execute("INSERT INTO list_of_wordlists DEFAULT VALUES")
            DataBase.sqlite_connection_with_db_list_of_wordlists.commit()
            user_id = DataBase.cursor_for_registration_info.execute(
                "SELECT id FROM registration_info WHERE login=? AND password=?", (new_login, new_password)).fetchone()[
                0]
            wordlist = 'My words'
            name: str = str(user_id) + '_' + wordlist
            DataBase.cursor_for_words_in_wordlists.execute(
                "INSERT INTO words_in_wordlists (id_wordlist) VALUES(?)", (name,))
            DataBase.sqlite_connection_with_db_words_in_wordlists.commit()

        except sqlite3.Error:
            return "error"
        return "okay"

    def get(self):
        login = self.request.headers["Login"]
        password = self.request.headers["Password"]
        response: str = self.create_user(login, password)
        self.write(response)


class GetTheListOfAddedWordlistsHandler(tornado.web.RequestHandler):
    words_str: str = ""

    @classmethod
    def get_the_list_of_added_wordlists(cls, user_id: int):
        user_id = int(user_id)
        cls.words_str = ""
        for i in range(1, 101):
            current_wordlist = 'wordlist' + str(i)
            sqlite_query = f'SELECT {current_wordlist} FROM list_of_wordlists WHERE id=?'
            temp_wordlist = DataBase.cursor_for_list_of_wordlists.execute(sqlite_query,
                                                                          (user_id,)).fetchone()
            if temp_wordlist[0] is not None:
                cls.words_str += temp_wordlist[0]
                cls.words_str += ';'
            else:
                break

    def get(self):
        user_id: int = self.request.headers["UserId"]
        self.get_the_list_of_added_wordlists(user_id)
        self.write(self.words_str)


class CreateDataBasesHandler(tornado.web.RequestHandler):

    @classmethod
    def check_whether_data_bases_exist(cls):
        if not os.path.exists("Server/list_of_wordlists.db"):
            cls.create_data_base("list_of_wordlists")
        if not os.path.exists("Server/registration_info.db"):
            cls.create_data_base("registration_info")
        if not os.path.exists("Server/words_in_wordlists.db"):
            cls.create_data_base("words_in_wordlists")
        DataBase.sqlite_connection_with_db_registration_info = sqlite3.connect('Server/registration_info.db')
        DataBase.cursor_for_registration_info = DataBase.sqlite_connection_with_db_registration_info.cursor()
        DataBase.sqlite_connection_with_db_words_in_wordlists = sqlite3.connect('Server/words_in_wordlists.db')
        DataBase.cursor_for_words_in_wordlists = DataBase.sqlite_connection_with_db_words_in_wordlists.cursor()
        DataBase.sqlite_connection_with_db_list_of_wordlists = sqlite3.connect('Server/list_of_wordlists.db')
        DataBase.cursor_for_list_of_wordlists = DataBase.sqlite_connection_with_db_list_of_wordlists.cursor()

    @classmethod
    def create_data_base(cls, name):
        global sqlite_create_table_query
        if name == "registration_info":
            sqlite_create_table_query = '''CREATE TABLE registration_info (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    login TEXT UNIQUE NOT NULL,
                                    password TEXT NOT NULL);'''
        elif name == 'words_in_wordlists':
            columns: str = ""
            for i in range(1, 300):
                columns += "word" + str(i) + ' TEXT, '
            columns += "word300 TEXT"
            sqlite_create_table_query = f'''CREATE TABLE words_in_wordlists (
                                    id_wordlist TEXT NOT NULL PRIMARY KEY,
                                    privacy TEXT DEFAULT 'public',
                                    amount_of_words INTEGER NOT NULL DEFAULT 1,
                                    {columns});'''
        elif name == 'list_of_wordlists':
            columns: str = "wordlist1 TEXT DEFAULT \'My words\', "
            for i in range(2, 100):
                columns += "wordlist" + str(i) + ' TEXT, '
            columns += "wordlist100 TEXT"
            sqlite_create_table_query = sqlite_create_table_query = f'''CREATE TABLE list_of_wordlists (
                                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                    amount_of_wordlists INTEGER NOT NULL DEFAULT 2,
                                    {columns});'''
        sqlite_connection = sqlite3.connect(f'Server/{name}.db')
        cursor = sqlite_connection.cursor()
        try:
            cursor.execute(sqlite_create_table_query)
        except sqlite3.Error as error:
            print("BD has already created")

    def get(self):
        self.check_whether_data_bases_exist()


class ChangePrivacySettingsHandler(tornado.web.RequestHandler):

    @staticmethod
    def change_privacy_settings(privacy_type: str, id_wordlist: str):
        sqlite_change_privacy_query = f"UPDATE words_in_wordlists SET privacy=? WHERE id_wordlist=?"
        DataBase.cursor_for_words_in_wordlists.execute(sqlite_change_privacy_query, (privacy_type, id_wordlist))
        DataBase.sqlite_connection_with_db_words_in_wordlists.commit()

    def get(self):
        privacy_type: str = self.request.headers["PrivacyType"]
        id_wordlist: str = self.request.headers["IdWordlist"]
        self.change_privacy_settings(privacy_type=privacy_type, id_wordlist=id_wordlist)


class FindWordlistsBySubstringHandler(tornado.web.RequestHandler):
    wordlists_str: str = ""

    @classmethod
    def find_wordlists_by_substring(cls, substring: str, user_id: str):
        user_id += '_'
        query = ' SELECT id_wordlist, amount_of_words FROM words_in_wordlists' \
                ' WHERE id_wordlist LIKE \'%' + substring + '%\' ' \
                                                            ' AND amount_of_words > 1' \
                                                            ' AND (privacy="public" OR id_wordlist LIKE \'' + user_id + '%\')'
        list_of_wordlists = DataBase.cursor_for_words_in_wordlists.execute(query).fetchall()
        cls.wordlists_str = json.dumps(list_of_wordlists)

    def get(self):
        substring = self.request.headers["Substring"]
        user_id = self.request.headers["UserId"]
        self.find_wordlists_by_substring(substring, user_id)
        self.write(self.wordlists_str)


class DeleteWordHandler(tornado.web.RequestHandler):
    @staticmethod
    def delete_word_function(word, id_wordlist):
        index_of_removable_word = 1
        while True:
            now_word = "word" + str(index_of_removable_word)
            cur_word = DataBase.cursor_for_words_in_wordlists.execute(f'SELECT {now_word}'
                                                                      f' FROM words_in_wordlists '
                                                                      f'WHERE id_wordlist=?', (id_wordlist,))
            responce = cur_word.fetchone()
            if responce[0] == word:
                break
            else:
                index_of_removable_word += 1
        delete_word_index = "word" + str(index_of_removable_word)
        amount_or_words = DataBase.cursor_for_words_in_wordlists.execute('SELECT amount_of_words'
                                                                         ' FROM words_in_wordlists '
                                                                         'WHERE id_wordlist=?',
                                                                         (id_wordlist,)).fetchone()[0]
        amount_or_words -= 1
        temp_word = "word" + str(amount_or_words)
        last_word = DataBase.cursor_for_words_in_wordlists.execute(f'SELECT {"word" + str(amount_or_words)} '
                                                                   f'FROM words_in_wordlists '
                                                                   f'WHERE id_wordlist=?', (id_wordlist,)).fetchone()[0]

        DataBase.cursor_for_words_in_wordlists.execute(f'UPDATE words_in_wordlists '
                                                       f'SET {delete_word_index}=?, '
                                                       f'amount_of_words = amount_of_words - 1, '
                                                       f'{temp_word}=NULL '
                                                       f'WHERE id_wordlist=?', (last_word, id_wordlist))
        DataBase.sqlite_connection_with_db_words_in_wordlists.commit()

    def get(self):
        word = self.request.headers["Word"]
        id_wordlist = self.request.headers["id_wordlist"]
        self.delete_word_function(word, id_wordlist)


def make_app():
    return tornado.web.Application([
        (r"/SignUp", SignUpHandler),
        (r"/CreateDB", CreateDataBasesHandler),
        (r"/CheckIfUserExists", CheckIfUserExistsHandler),
        (r"/GetTheListOfAddedWords", GetTheListOfAddedWordsHandler),
        (r"/AddNewWord", AddNewWordHandler),
        (r"/AddNewWordlist", AddNewWordlistHandler),
        (r"/GetTheListOfAddedWordlists", GetTheListOfAddedWordlistsHandler),
        (r"/DeleteWord", DeleteWordHandler),
        (r"/ChangePrivacySettings", ChangePrivacySettingsHandler),
        (r"/FindWordlistsBySubstring", FindWordlistsBySubstringHandler),
        (r"/GetTheListOfAddedWordsFromParticularWordlist", GetTheListOfAddedWordsFromParticularWordlistHandler)
    ])


async def main():
    app = make_app()
    app.listen(port=23905, address=ip_address)
    await asyncio.Event().wait()


if __name__ == "__main__":
    ip_address = get_ip_address()
    asyncio.run(main())
