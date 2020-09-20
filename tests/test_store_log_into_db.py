import pytest
import os
import tempfile

from app.db import get_db
from app.model.Log import Log

def test_setup_test_logs(test_logfile, app):
    logfile_name = test_logfile.split('/')[-1]

    with app.app_context():
        db = get_db()
        log = Log(test_logfile)
        row = db.execute('SELECT * FROM Logfiles').fetchone()
        assert row['file_name'] == logfile_name 
