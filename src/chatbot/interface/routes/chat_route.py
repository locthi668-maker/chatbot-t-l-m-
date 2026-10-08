import time

from flask import Blueprint, current_app, jsonify, request

from src.chatbot.application.send_message import send_message
from src.chatbot.interface.require_json import require_json

chat_bp = Blueprint("chat", __name__)


@chat_bp.post("/api/chat")
def chat():
    """Chỉ đọc hai trường message và session_id, bỏ qua trường thừa."""
    bad_request = require_json()
    if bad_request is not None:
        return bad_request
    deps = current_app.config["deps"]
    payload = request.get_json(silent=True)
    started = time.perf_counter()
    loader = deps["system_prompt_loader"]
    try:
        system_prompt = loader(deps["settings"].system_prompt_file)
    except TypeError:
        system_prompt = loader()
    reply = send_message(
        deps["repo"],
        deps["model"],
        deps["store"],
        system_prompt,
        deps["settings"].max_messages,
        payload.get("session_id", ""),
        payload.get("message", ""),
    )
    elapsed_ms = int((time.perf_counter() - started) * 1000)
    model_name = deps["settings"].openai_model
    return jsonify({"reply": reply, "model": model_name, "ms": elapsed_ms})
