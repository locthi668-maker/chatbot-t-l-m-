from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.get("/api/health")
def health():
    """Trả đúng đối tượng ok."""
    return jsonify({"ok": True})
