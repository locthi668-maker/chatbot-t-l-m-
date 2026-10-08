from flask import jsonify, request

from src.chatbot.interface.json_error import error_payload

LOCAL_ADDRESSES = {"127.0.0.1", "::1"}


def require_localhost():
    """Trả None khi địa chỉ nguồn hợp lệ, ngược lại trả (response, 403)."""
    if request.remote_addr not in LOCAL_ADDRESSES:
        body = error_payload("forbidden", "Chỉ chấp nhận yêu cầu từ máy cục bộ.")
        return jsonify(body), 403
    return None
