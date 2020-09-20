import os

def get_log_name(logpath):
    return logpath.split('/')[-1]

def count_log_records_in_db(db):
    row = db.execute('SELECT COUNT(*) FROM LOGS').fetchone()    
    return row[0]

def get_latest_filename_from_db(db):
    row = db.execute('SELECT * FROM LOGFILE_NAMES').fetchone()
    return row['file_name']

def check_test_logfile_exists(test_logfile):
    assert os.path.isfile(test_logfile) == True, "Test logfile '{}' must exist in order to run this test".format(test_logfile)
