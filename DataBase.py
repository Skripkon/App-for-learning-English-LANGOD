import sqlite3
import os.path

class DataBase:
    @classmethod
    def create_data_base(cls, name):
        global sqlite_create_table_query
        if name == "registration_info":
            sqlite_create_table_query = '''CREATE TABLE registration_info (
                                login TEXT PRIMARY KEY,
                                password TEXT NOT NULL,
                                id INTEGER NOT NULL UNIQUE);'''
            
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
    def chech_whether_data_bases_exist(cls):
        if os.path.exists("users_data.db") == False:
            cls.create_data_base("users_data")
        if os.path.exists("registration_info.db") == False:
             cls.create_data_base("registration_info")
