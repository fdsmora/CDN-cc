from app.db import get_db
from app.model.Log import Log
from tests.util import count_logfile_lines, count_lines, count_log_records_in_db

def test_import_log_into_db(app, test_logfile):
    logfile_name = test_logfile.split('/')[-1]

    with app.app_context():
        db = get_db()
        log = Log(test_logfile)
        row = db.execute('SELECT * FROM LOGFILE_NAMES').fetchone()
        assert row['file_name'] == logfile_name 

        total_file_lines = count_logfile_lines(test_logfile)
        total_db_records = count_log_records_in_db(db) 

        assert total_file_lines == total_db_records
