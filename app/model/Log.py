import sqlite3 
import re
from app.db import get_db

class Log:
    def import_into_db(self, filepath):
        self.filepath = filepath
        self.logname = filepath.split('/')[-1]
        self.logname = filepath.split('/')[-1]
        self.total_lines = self.count_lines()

        self._register_log_file(self.logname)
        self._set_log_id()
        self._register_log_entries(filepath)

    def _set_log_id(self):
        db = get_db()
        row = db.execute("SELECT max(id) FROM LOGFILE_NAMES").fetchone()
        if row and len(row) > 0:
            self.id = row[0]

    def _register_log_file(self, logname):
        db = get_db()

        db.execute("INSERT INTO LOGFILE_NAMES (file_name) values (?)", (self.logname,))
        db.commit()
        
    def _register_log_entries(self, filepath):
        with open(filepath, 'r') as f:
            fields_names = []
            current_line = f.readline()
            while current_line:
                if Log.line_starts_with("#", current_line):
                    fields_names = Log.get_field_names(current_line)
                elif fields_names:
                    self._register_log_entry(fields_names, current_line.split()) 
                current_line = f.readline()

    def _register_log_entry(self, fields_names, fields_values):
        db = get_db()
        fields_names = (str(fields_names)[1:-1] + ',\'logfile_name_id\'') # Remove brackets and include the foreign key column  
        fields_values = (*fields_values, self.id) # Include foreign key value
        db.execute("INSERT INTO LOGS ({}) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)".format(fields_names), fields_values);
        db.commit()

    def count_lines(self):
        if self.filepath:
            with open(self.filepath, 'r') as f:
                for i,line in enumerate(f):
                    pass
                return i+1
        return 0 

    def get_records_count(self):
        if self.total_lines > 2:
            return self.total_lines - 2 # exclude header lines
        return 0

    def get_bytes_for_cdn_request_type(self, cdn_request_type):
        db = get_db()
        row = db.execute("SELECT SUM(`cs-bytes`+`sc-bytes`) FROM LOGS WHERE `x-edge-response-result-type`= ?", (cdn_request_type.capitalize(),)).fetchone()
        return int((row and row[0]) or 0)

    @staticmethod
    def line_starts_with(pattern, line):
        return re.search("^"+pattern, line) 

    @staticmethod
    def get_field_names(current_line):
        fields_names = []
        if Log.line_starts_with('#Fields', current_line):
            fields_names = current_line.split()[1:]
        return fields_names

