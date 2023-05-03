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
    sqlite_connection_with_db_users_data = None
    cursor_for_users_data = None
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


class GetTheListOfAddedWordsHandler(tornado.web.RequestHandler):
    words_str: str = ''

    @classmethod
    def get_the_list_of_added_words(cls, user_id):
        query = 'SELECT id_wordlist FROM words_in_wordlists WHERE id_wordlist LIKE \'' + user_id + '%\''
        list_of_wordlists = DataBase.cursor_for_words_in_wordlists.execute(query).fetchall()
        print(list_of_wordlists)
        cls.words_str = ''
        dict_of_wordlists = {}
        for id_wordlists in list_of_wordlists:
            id_wordlists = id_wordlists[0]
            for i in range(1, 301):
                current_word = 'word' + str(i)
                sqlite_query = f'SELECT {current_word} FROM words_in_wordlists WHERE id_wordlist=?'
                temp_word = DataBase.cursor_for_words_in_wordlists.execute(sqlite_query,
                                                                           (id_wordlists,)).fetchone()
                if temp_word[0] is not None:
                    if temp_word[0] not in dict_of_wordlists:
                        dict_of_wordlists[temp_word[0]] = [id_wordlists]
                    else:
                        dict_of_wordlists[temp_word[0]].append(id_wordlists)
                else:
                    break
        cls.words_str = json.dumps(dict_of_wordlists)
        print(cls.words_str)

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
            DataBase.cursor_for_users_data.execute("INSERT INTO users_data DEFAULT VALUES")
            DataBase.sqlite_connection_with_db_users_data.commit()
            DataBase.cursor_for_list_of_wordlists.execute("INSERT INTO list_of_wordlists DEFAULT VALUES")
            DataBase.sqlite_connection_with_db_list_of_wordlists.commit()
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
                cls.words_str += ' '
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
        if not os.path.exists("Server/users_data.db"):
            cls.create_data_base("users_data")
        if not os.path.exists("Server/registration_info.db"):
            cls.create_data_base("registration_info")
        if not os.path.exists("Server/words_in_wordlists.db"):
            cls.create_data_base("words_in_wordlists")
        DataBase.sqlite_connection_with_db_registration_info = sqlite3.connect('Server/registration_info.db')
        DataBase.cursor_for_registration_info = DataBase.sqlite_connection_with_db_registration_info.cursor()
        DataBase.sqlite_connection_with_db_users_data = sqlite3.connect('Server/users_data.db')
        DataBase.cursor_for_users_data = DataBase.sqlite_connection_with_db_users_data.cursor()

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

        elif name == "users_data":
            columns: str = ""
            for i in range(1, 500):
                columns += "word" + str(i) + ' TEXT, '
            columns += "word500 TEXT"
            sqlite_create_table_query = f'''CREATE TABLE users_data (
                                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                amount_of_words INTEGER NOT NULL DEFAULT 1,
                                {columns});'''
        elif name == 'words_in_wordlists':
            columns: str = ""
            for i in range(1, 300):
                columns += "word" + str(i) + ' TEXT, '
            columns += "word300 TEXT"
            sqlite_create_table_query = f'''CREATE TABLE words_in_wordlists (
                                id_wordlist TEXT NOT NULL PRIMARY KEY,
                                amount_of_words INTEGER NOT NULL DEFAULT 1,
                                {columns});'''

        elif name == 'list_of_wordlists':
            columns: str = ""
            for i in range(1, 100):
                columns += "wordlist" + str(i) + ' TEXT, '
            columns += "wordlist100 TEXT"
            sqlite_create_table_query = sqlite_create_table_query = f'''CREATE TABLE list_of_wordlists (
                                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                amount_of_wordlists INTEGER NOT NULL DEFAULT 1,
                                {columns});'''
        sqlite_connection = sqlite3.connect(f'Server/{name}.db')
        cursor = sqlite_connection.cursor()
        try:
            cursor.execute(sqlite_create_table_query)
        except sqlite3.Error as error:
            print("BD has already created")

    def get(self):
        self.check_whether_data_bases_exist()


# class DeleteWordHandler(tornado.web.RequestHandler):
#     def delete_word_function(self, ):
#         pass
#         word = Word.Word.current_word
#         last_word = DataBase.cursor_for_words_in_wordlists.execute('SELECT amount_of_words FROM words_in_wordlists WHERE ')
#         query = f'UPDATE words_in_wordlists SET '
#
#     def get(self):
#         self.delete_word_function()


def make_app():
    return tornado.web.Application([
        (r"/SignUp", SignUpHandler),
        (r"/CreateDB", CreateDataBasesHandler),
        (r"/CheckIfUserExists", CheckIfUserExistsHandler),
        (r"/GetTheListOfAddedWords", GetTheListOfAddedWordsHandler),
        (r"/AddNewWord", AddNewWordHandler),
        (r"/AddNewWordlist", AddNewWordlistHandler),
        (r"/GetTheListOfAddedWordlists", GetTheListOfAddedWordlistsHandler),
        (r"/DeleteWord", DeleteWordHandler)
    ])


async def main():
    app = make_app()
    app.listen(port=23904, address=ip_address)
    await asyncio.Event().wait()


if __name__ == "__main__":
    ip_address = get_ip_address()
    asyncio.run(main())
