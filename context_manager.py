import sqlite3 as db

class ContextManager():

    def __init__(self, dbname: str):
        self.dbname=dbname

    def __enter__(self):
        self.connection=db.connect(self.dbname)
        self.cursor=self.connection.cursor()
        self.cursor.execute("PRAGMA foreign_keys=1")

        return self

    def __exit__(self, exec_type, exec_val, exec_tb):
        self.connection.close()
