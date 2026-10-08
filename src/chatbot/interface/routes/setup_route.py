from flask import Blueprint, current_app, jsonify, request

from src.chatbot.application.configure_api_key import configure_api_key
from src.chatbot.interface.json_error import error_payload
from src.chatbot.interface.require_json import require_json
from src.chatbot.interface.require_localhost import require_localhost

setup_bp = Blueprint("setup", __name__)


@setup_bp.post("/api/setup")
def setup():
    """Kiểm địa chỉ, kiểm JSON, lưu khóa, không bao giờ trả lại khóa."""
    denied = require_localhost()
    if denied is not None:
        return denied
    bad_request = require_json()
    if bad_request is not None:
        return bad_request
    api_key = request.get_json(silent=True).get("api_key", "")
    store = current_app.config["deps"]["store"]
    try:
        configure_api_key(store, api_key)
    except OSError:
        body = error_payload("save_failed", "Không ghi được tệp .env.")
        return jsonify(body), 500
    return jsonify({"ok": True})
