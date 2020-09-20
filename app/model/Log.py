import sqlite3 
from app.db import get_db

class Log:
    def __init__(self, filepath):
        self.filepath = filepath
        self.logname = filepath.split('/')[-1]

        db = get_db()
        
        db.execute("INSERT INTO LOGFILES (file_name) values (?)", (self.logname,))
