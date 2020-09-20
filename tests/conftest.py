import os
import pytest
import tempfile

from app import create_app
from pathlib import Path
from shutil import copy, rmtree
from app.db import init_db

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()

    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def test_logfile(app):
    tmp_dir = tempfile.mkdtemp()
    parent_dir = Path(os.path.abspath(__file__)).parent.parent
    test_log = "{}/testlog_1".format(parent_dir) 
    copy(test_log, tmp_dir)
 
    yield test_log 

    rmtree(tmp_dir)
