from flask import Blueprint, request, abort

from app.model.Log import Log
from app import CDN_Request_Type

bp = Blueprint('report', __name__)

@bp.route('/report/bytes/<cdn_request_type>', methods=('GET',))
def report_bytes(cdn_request_type):
    cdn_request_type = cdn_request_type.capitalize()
    if cdn_request_type and cdn_request_type in (CDN_Request_Type.HIT, CDN_Request_Type.MISS):
        return str(Log().get_bytes_for_cdn_request_type(cdn_request_type))

    abort(400, description="Invalid or missing CDN Request type")
