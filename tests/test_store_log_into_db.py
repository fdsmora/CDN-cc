import pytest
import os
import tempfile

from app.db import get_db
from app.model.Log import Log

def count_logfile_lines(logfile):
    total_lines_count = 0
    with open(logfile, 'r') as f:
        total_lines_count =  countLines(f) - 2 # discount header lines
    return total_lines_count

def countLines(file_handle):
    for i,line in enumerate(file_handle):
        pass
    return i+1

def count_log_records_in_db(db):
    row = db.execute('SELECT COUNT(*) FROM LOGFILE_NAMES').fetchone()    
    return row[0]

def test_setup_test_logs(test_logfile, app):
    logfile_name = test_logfile.split('/')[-1]

    with app.app_context():
        db = get_db()
        log = Log(test_logfile)
        row = db.execute('SELECT * FROM LOGFILE_NAMES').fetchone()
        assert row['file_name'] == logfile_name 

        total_file_lines = count_logfile_lines(test_logfile)
        total_db_records = count_log_records_in_db(db) 

        assert total_file_lines == total_db_records

