import sqlite3
import datetime
import pytz


class SQLiteDataBase:
    def __init__(self, db_path):
        self.__database = sqlite3.connect(db_path)
        self.__cur = self.__database.cursor()
        self.__cur.execute("CREATE TABLE IF NOT EXISTS users(chat_id INTEGER PRIMARY KEY, reg_date DATETIME)")
        self.__cur.execute("CREATE TABLE IF NOT EXISTS actions(chat_id, date DATETIME, video_id TEXT )")

    def add_user(self, chat_id):
        self.__cur.execute("INSERT OR IGNORE INTO users(chat_id, reg_date) VALUES(?, ?)", (chat_id,
                                                                                           datetime.datetime.now(pytz.timezone('Europe/Moscow')),))
        self.__database.commit()

    def add_action(self, chat_id, video_id):
        self.__cur.execute('INSERT OR IGNORE INTO actions(chat_id, date, video_id) VALUES(?, ?, ?)',
                           (chat_id, datetime.datetime.now(pytz.timezone('Europe/Moscow')), video_id,))
        self.__database.commit()