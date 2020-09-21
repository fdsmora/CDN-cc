from flask import Blueprint, request, abort, jsonify, current_app

from app.model.Log import Log
from app import CDN_Request_Result_Type

bp = Blueprint('report', __name__)

@bp.route('/report/bytes/<cdn_request_result_type>', methods=('GET',))
def report_bytes(cdn_request_result_type):
    cdn_request_result_type = cdn_request_result_type.capitalize()
    if cdn_request_result_type and cdn_request_result_type in (CDN_Request_Result_Type.HIT, CDN_Request_Result_Type.MISS):
        log = Log()
        testlog_file1 = current_app.instance_path + '/testlog_1'
        log.import_into_db(testlog_file1)

        total_bytes = Log().get_bytes_for_cdn_request_type(cdn_request_result_type)

        return jsonify({ 'x-edge-response-result-type' : cdn_request_result_type, 'total_bytes' : total_bytes}) 

    abort(400, description="Invalid or missing CDN Request type")
