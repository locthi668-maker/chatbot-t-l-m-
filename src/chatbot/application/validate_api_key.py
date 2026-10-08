from src.chatbot.domain.errors import InvalidApiKey

MIN_KEY_LENGTH = 20
MAX_KEY_LENGTH = 200


def _is_printable_ascii(value: str) -> bool:
    return all(32 <= ord(char) <= 126 for char in value)


def validate_api_key(api_key: str) -> str:
    """Kiểm tra hình thức khóa, KHÔNG kiểm tiền tố nhà cung cấp."""
    if not isinstance(api_key, str):
        raise InvalidApiKey("api_key phải là chuỗi")
    value = api_key.strip()
    if not MIN_KEY_LENGTH <= len(value) <= MAX_KEY_LENGTH:
        raise InvalidApiKey(
            f"api_key phải dài {MIN_KEY_LENGTH} đến {MAX_KEY_LENGTH} ký tự"
        )
    if any(char.isspace() for char in value):
        raise InvalidApiKey("api_key không được chứa khoảng trắng bên trong")
    if not _is_printable_ascii(value):
        raise InvalidApiKey("api_key chỉ gồm ký tự ASCII in được")
    return value
