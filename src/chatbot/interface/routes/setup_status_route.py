from flask import Blueprint, current_app, jsonify

from src.chatbot.application.get_setup_status import get_setup_status

setup_status_bp = Blueprint("setup_status", __name__)


@setup_status_bp.get("/api/setup/status")
def setup_status():
    """Đọc trạng thái từ cửa hàng khóa, không đọc tệp trực tiếp."""
    store = current_app.config["deps"]["store"]
    return jsonify(get_setup_status(store))
