import re

from src.chatbot.domain.errors import InvalidSession

PATTERN = re.compile(r"^[A-Za-z0-9-]{8,64}$")


def validate_session_id(session_id: str) -> str:
    """Kiểm tra session_id rồi trả về nguyên bản, KHÔNG cắt khoảng trắng."""
    if not isinstance(session_id, str):
        raise InvalidSession("session_id phải là chuỗi")
    if not PATTERN.fullmatch(session_id):
        raise InvalidSession(
            "session_id phải dài 8 đến 64 ký tự, chỉ gồm chữ, số và dấu gạch ngang"
        )
    return session_id
