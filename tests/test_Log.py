import os
from app.db import get_db
from app.model.Log import Log
from tests.util import count_log_records_in_db, get_log_name, get_latest_filename_from_db

def test_import_log_into_db(app, test_logfile):
    check_test_logfile_exists(test_logfile)
    with app.app_context():
        log = Log(test_logfile)

        db = get_db()

        assert get_latest_filename_from_db(db) == get_log_name(test_logfile) 
        assert 7800 == count_log_records_in_db(db)

def test_count_log_records(app, test_logfile):
    check_test_logfile_exists(test_logfile)
    with app.app_context():
        log = Log(test_logfile)
        assert log.get_records_count() == 7800

def check_test_logfile_exists(test_logfile):
    assert os.path.isfile(test_logfile) == True, "Test logfile '{}' must exist in order to run this test".format(test_logfile)
