import sqlite3 
import re
from app.db import get_db

class Log:

    def import_into_db(self, filepath):
        logname = filepath.split('/')[-1]
      
        if not self.is_log_imported(logname): 
            self.logname = logname
            self.filepath = filepath
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
        
    def _register_log_entries(self, file_path):
        fields_names = []

        with open(file_path, 'r') as f:
            f.readline()
            fields_names = f.readline().split()[1:]

        fields_names = (str(fields_names)[1:-1] + ',\'logfile_name_id\'') # Remove brackets and include the foreign key column  

        def get_record(file_path):
            with open(file_path, 'r') as f:
                current_line = f.readline()
                while current_line:
                    if not Log.line_starts_with("#", current_line):
                        yield (*current_line.split('\t'), self.id) # Include foreign key value
                        
                    current_line = f.readline()

        self._insert_log_record_into_db(get_record, file_path, fields_names)

    def _insert_log_record_into_db(self, get_record, file_path, fields_names):
        db = get_db()
        try:
            db.executemany("INSERT INTO LOGS ({}) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)".format(fields_names), get_record(file_path));
            db.commit()
        except sqlite3.Error as e:
            # If DB gets locked, nothing much we can do, so ignore and continue
            #fausto
            import pdb
            pdb.set_trace()
            pass 
        

    def _register_log_entry(self, fields_names, fields_values):
        db = get_db()
        fields_names = (str(fields_names)[1:-1] + ',\'logfile_name_id\'') # Remove brackets and include the foreign key column  
        fields_values = (*fields_values, self.id) # Include foreign key value
        try:
            db.execute("INSERT INTO LOGS ({}) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)".format(fields_names), fields_values);
            db.commit()
        except sqlite3.Error as e:
            # If DB gets locked, nothing much we can do, so ignore and continue
            pass 

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

    def is_log_imported(self, file_name):
        db = get_db()
        row = db.execute("SELECT 1 FROM LOGFILE_NAMES WHERE file_name = ?", (file_name,)).fetchone()
        return int((row and row[0]) or 0)

    def get_total_success_requests(self):
        db = get_db()
        row = db.execute("select count(*) from logs where `sc-status` = 200").fetchone()
        return int((row and row[0]) or 0)

    def get_total_failed_requests(self):
        db = get_db()
        row = db.execute("select count(*) from logs where `x-edge-response-result-type` like '%error%'").fetchone()
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

