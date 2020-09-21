import json
from app import create_app, CDN_Request_Result_Type
from app.db import get_db
from app.model.Log import Log
from tests.util import check_test_logfile_exists

def test_bytes_for_hits(app, client, test_logfile):
    check_test_logfile_exists(test_logfile)

    log = Log()
    with app.app_context():
        log.import_into_db(test_logfile)

    response = client.get("/report/bytes/hit")
    assert get_expected_response_bytes_report(test_logfile, CDN_Request_Result_Type.HIT) == json.loads(response.data.decode('utf8'))

    # Bad request
    response = client.get("/report/bytes/trash")
    assert response.status_code == 400

def get_expected_response_bytes_report(test_logfile, cdn_request_result_type):
    bytes_count = get_bytes_for_hits_or_miss_from_test_logfile(test_logfile, cdn_request_result_type)
    return { 'x-edge-response-result-type' : cdn_request_result_type, 'total_bytes' : bytes_count } 

def get_bytes_for_hits_or_miss_from_test_logfile(test_logfile, cdn_request_result_type):
    field_names = []
    bytes_count = 0
    with open(test_logfile, 'r') as f:
        for _ , current_line in enumerate(f):
            if Log.line_starts_with('#Fields', current_line):
                field_names = Log.get_field_names(current_line)
            elif not Log.line_starts_with('#', current_line):
                bytes_count += get_bytes(current_line, field_names, cdn_request_result_type)
    return bytes_count
    
def get_bytes(line, field_names, cdn_request_result_type):
    fields = line.split('\t')
    nvps = dict(zip(field_names, fields))
    if nvps['x-edge-response-result-type'] == cdn_request_result_type:
        return int(nvps['cs-bytes']) + int(nvps['sc-bytes'])
    return 0
