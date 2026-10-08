from src.chatbot.domain.errors import InvalidMessage

MAX_MESSAGE_LENGTH = 4000


def validate_message(text: str) -> str:
    """Cắt khoảng trắng hai đầu, rồi kiểm tra rỗng và độ dài."""
    if not isinstance(text, str):
        raise InvalidMessage("message phải là chuỗi")
    value = text.strip()
    if not value:
        raise InvalidMessage("message không được rỗng")
    if len(value) > MAX_MESSAGE_LENGTH:
        raise InvalidMessage(f"message dài tối đa {MAX_MESSAGE_LENGTH} ký tự")
    return value
