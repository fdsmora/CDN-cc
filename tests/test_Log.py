from app.db import get_db
from app.model.Log import Log
from tests.util import count_log_records_in_db, get_log_name, get_latest_filename_from_db, check_test_logfile_exists

def test_import_log_into_db(app, test_logfile):
    check_test_logfile_exists(test_logfile)

    log = Log()
    with app.app_context():
        log.import_into_db(test_logfile)

        db = get_db()

        assert get_latest_filename_from_db(db) == get_log_name(test_logfile) 
        assert 7800 == count_log_records_in_db(db)

def test_count_log_records(app, test_logfile):
    check_test_logfile_exists(test_logfile)

    log = Log()
    with app.app_context():
        log.import_into_db(test_logfile)
        assert log.get_records_count() == 7800
