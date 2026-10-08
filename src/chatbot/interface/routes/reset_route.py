from flask import Blueprint, current_app, jsonify, request

from src.chatbot.application.reset_conversation import reset_conversation
from src.chatbot.interface.require_json import require_json

reset_bp = Blueprint("reset", __name__)


@reset_bp.post("/api/reset")
def reset():
    """Xoá phiên đã có hay chưa có đều trả thành công im lặng."""
    bad_request = require_json()
    if bad_request is not None:
        return bad_request
    deps = current_app.config["deps"]
    payload = request.get_json(silent=True)
    reset_conversation(deps["repo"], payload.get("session_id", ""))
    return jsonify({"ok": True})
