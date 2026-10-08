from flask import jsonify, request

from src.chatbot.interface.json_error import error_payload


def require_json():
    """Trả None khi đạt, trả (response, status) khi không đạt."""
    if request.mimetype != "application/json":
        body = error_payload("unsupported_media_type", "Thiếu Content-Type: application/json.")
        return jsonify(body), 415
    if not isinstance(request.get_json(silent=True), dict):
        body = error_payload("invalid_json", "Thân yêu cầu phải là đối tượng JSON.")
        return jsonify(body), 400
    return None
