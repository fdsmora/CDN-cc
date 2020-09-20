import sqlite3 
import re
from app.db import get_db

class Log:
    def __init__(self, filepath):
        self.filepath = filepath
        self.logname = filepath.split('/')[-1]
        self.total_lines = self.count_lines()

        self.register_log_file(self.logname)
        self.set_log_id()
        self.register_log_entries(filepath)

    def set_log_id(self):
        db = get_db()
        row = db.execute("SELECT max(id) FROM LOGFILE_NAMES").fetchone()
        if row and len(row) > 0:
            self.id = row[0]

    def register_log_file(self, logname):
        db = get_db()

        db.execute("INSERT INTO LOGFILE_NAMES (file_name) values (?)", (self.logname,))
        db.commit()
        
    def register_log_entries(self, filepath):
        with open(filepath, 'r') as f:
            fields_names = []
            current_line = f.readline()
            while current_line:
                if self.line_starts_with("#", current_line):
                    fields_names = self.get_field_names(current_line)
                elif fields_names:
                    self.register_log_entry(fields_names, current_line.split()) 
                current_line = f.readline()

    def register_log_entry(self, fields_names, fields_values):
        db = get_db()
        fields_names = (str(fields_names)[1:-1] + ',\'logfile_name_id\'') # Remove brackets and include the foreign key column  
        fields_values = (*fields_values, self.id) # Include foreign key value
        db.execute("INSERT INTO LOGS ({}) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)".format(fields_names), fields_values);
        db.commit()

    def line_starts_with(self, pattern, line):
        return re.search("^"+pattern, line) 

    def get_field_names(self, current_line):
        fields_names = []
        if self.line_starts_with('#Fields', current_line):
            fields_names = current_line.split()[1:]
        return fields_names

    def count_lines(self):
        with open(self.filepath, 'r') as f:
            for i,line in enumerate(f):
                pass
        return i+1

    def get_records_count(self):
        return self.total_lines - 2 # exclude header lines
