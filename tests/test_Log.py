from app.db import get_db
from app.model.Log import Log
from tests.util import count_logfile_lines, count_lines, count_log_records_in_db

def test_import_log_into_db(app, test_logfile):
    with app.app_context():
        log = Log(test_logfile)

        db = get_db()
        logfile_name = test_logfile.split('/')[-1]

        assert get_latest_filename_from_db(db) == logfile_name 
        assert count_logfile_lines(test_logfile) == count_log_records_in_db(db)

def get_latest_filename_from_db(db):
    row = db.execute('SELECT * FROM LOGFILE_NAMES').fetchone()
    return row['file_name']
