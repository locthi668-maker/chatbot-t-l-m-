from flask import jsonify
from werkzeug.exceptions import HTTPException

from src.chatbot.domain.errors import (
    ApiKeyMissing,
    ChatbotError,
    InvalidApiKey,
    InvalidMessage,
    InvalidSession,
    UpstreamError,
)

EMPTY_REPLY_STATUS = 502
EMPTY_REPLY_CODE = "empty_reply"
EMPTY_REPLY_MESSAGE = "Mô hình trả về nội dung rỗng."

RULES = (
    (InvalidSession, 400, "invalid_session", "Mã phiên không hợp lệ."),
    (InvalidMessage, 400, "invalid_message", "Nội dung tin không hợp lệ."),
    (InvalidApiKey, 400, "invalid_api_key", "Khóa API không đúng hình thức."),
    (ApiKeyMissing, 409, "api_key_missing", "Chưa nhập khóa API."),
)

UPSTREAM_CODES = {
    401: "invalid_api_key",
    502: "upstream_unreachable",
    503: "rate_limited",
    504: "upstream_timeout",
}


def error_payload(code, message):
    """Khoá khóa đúng hai trường của mọi phản hồi lỗi."""
    return {"error": code, "message": message}


def resolve_chatbot_error(exc):
    """Ánh xạ lỗi tầng domain sang cặp (status, code, message)."""
    if isinstance(exc, UpstreamError):
        if exc.message == EMPTY_REPLY_MESSAGE or "rỗng" in exc.message:
            return EMPTY_REPLY_STATUS, EMPTY_REPLY_CODE, exc.message
        code = UPSTREAM_CODES.get(exc.status, "upstream_error")
        return exc.status, code, exc.message
    for cls, status, code, message in RULES:
        if isinstance(exc, cls):
            return status, code, message
    return 500, "internal_error", "Có lỗi không mong đợi."


def register_error_handlers(app):
    """Gắn bốn trình xử lý lỗi vào ứng dụng Flask."""

    @app.errorhandler(ChatbotError)
    def handle_chatbot_error(exc):
        status, code, message = resolve_chatbot_error(exc)
        return jsonify(error_payload(code, message)), status

    @app.errorhandler(413)
    def handle_too_large(_exc):
        return jsonify(error_payload("payload_too_large", "Thân yêu cầu vượt quá 16 KB.")), 413

    @app.errorhandler(HTTPException)
    def handle_http_exception(exc):
        code = exc.name.lower().replace(" ", "_")
        return jsonify(error_payload(code, exc.description)), exc.code

    @app.errorhandler(Exception)
    def handle_unexpected(exc):
        app.logger.error("loi_khong_mong_doi: %s", type(exc).__name__)
        return jsonify(error_payload("internal_error", "Có lỗi không mong đợi.")), 500
