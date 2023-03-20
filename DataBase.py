import sqlite3
import os.path

class DataBase:
    current_user_id = None
    sqlite_connection = None
    cursor = None

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
            for i in range(500):
                columns += "word" + str(i) + ' TEXT, '
            columns += "word500 TEXT"

            sqlite_create_table_query = f'''CREATE TABLE users_data (
                                id INTEGER PRIMARY KEY,
                                amount_of_words INTEGER,
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
        cls.sqlite_connection = sqlite3.connect('registration_info.db')
        cls.cursor = cls.sqlite_connection.cursor()

    @classmethod
    def create_user(cls, new_login: str, new_password: str):
        cls.cursor.execute("INSERT INTO registration_info (login, password) VALUES(?, ?)", (new_login, new_password))
        cls.sqlite_connection.commit()


    @classmethod
    def check_if_user_exists(cls, login_text: str, password: str) -> int:
        info = cls.cursor.execute("SELECT id FROM registration_info WHERE login=? and password=?", (login_text, password))
        # cls.sqlite_connection.commit()
        if info.fetchone() is None:
            return -1
        else:
            return info.fetchone()

    @classmethod
    def close_connection(cls):
        cls.cursor.close()
        cls.sqlite_connection.close()
