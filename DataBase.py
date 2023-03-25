import sqlite3
import os.path
import Exerciser
import Word


class DataBase:
    current_user_id = None
    sqlite_connection_with_db_users_data = None
    cursor_for_users_data = None
    sqlite_connection_with_db_registration_info = None
    cursor_for_registration_info = None

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

        sqlite_connection = sqlite3.connect(f'{name}.db')
        cursor = sqlite_connection.cursor()
        try:
            cursor.execute(sqlite_create_table_query)
        except sqlite3.Error as error:
            print("BD has already created")

    @classmethod
    def check_whether_data_bases_exist(cls):
        if not os.path.exists("users_data.db"):
            cls.create_data_base("users_data")
        if not os.path.exists("registration_info.db"):
            cls.create_data_base("registration_info")
        cls.sqlite_connection_with_db_registration_info = sqlite3.connect('registration_info.db')
        cls.cursor_for_registration_info = cls.sqlite_connection_with_db_registration_info.cursor()
        cls.sqlite_connection_with_db_users_data = sqlite3.connect('users_data.db')
        cls.cursor_for_users_data = cls.sqlite_connection_with_db_users_data.cursor()

    @classmethod
    def create_user(cls, new_login: str, new_password: str):
        cls.cursor_for_registration_info.execute("INSERT INTO registration_info (login, password) VALUES(?, ?)",
                                                 (new_login, new_password))
        cls.sqlite_connection_with_db_registration_info.commit()

        cls.cursor_for_users_data.execute("INSERT INTO users_data DEFAULT VALUES")
        cls.sqlite_connection_with_db_users_data.commit()

    @classmethod
    def check_if_user_exists(cls, login_text: str, password: str) -> int:
        info = cls.cursor_for_registration_info.execute("SELECT id FROM registration_info WHERE login=? and password=?",
                                                        (login_text, password))
        response = info.fetchone()
        if response is None:
            return -1
        else:
            return response[0]

    @classmethod
    def close_connection(cls):
        cls.cursor_for_registration_info.close()
        cls.sqlite_connection_with_db_registration_info.close()
        cls.cursor_for_users_data.close()
        cls.sqlite_connection_with_db_users_data.close()

    @classmethod
    def add_new_word(cls):
        word: str = Word.Word.current_word
        temp = cls.cursor_for_users_data.execute("SELECT amount_of_words FROM users_data WHERE id=?",
                                                 (DataBase.current_user_id,))
        n: int = temp.fetchone()[0]
        number_of_new_word = "word" + str(n)
        sqlite_add_word_query = f"UPDATE users_data SET {number_of_new_word}=?, " \
                                f"amount_of_words = amount_of_words + 1 WHERE id=?"
        DataBase.cursor_for_users_data.execute(sqlite_add_word_query, (word, DataBase.current_user_id))
        cls.sqlite_connection_with_db_users_data.commit()

    @classmethod
    def set_the_list_of_added_words(cls):
        for i in range(1, 501):
            current_word = 'word' + str(i)
            sqlite_query = f'SELECT {current_word} FROM users_data WHERE id=?'
            temp_word = DataBase.cursor_for_users_data.execute(sqlite_query,
                                                               (DataBase.current_user_id, )).fetchone()
            if temp_word[0] is not None:
                Exerciser.Exerciser.current_list_of_added_words[temp_word[0]] = i
            else:
                break
