from src.chatbot.application.validate_api_key import validate_api_key
from src.chatbot.domain.ports.api_key_store import ApiKeyStore


def configure_api_key(store: ApiKeyStore, api_key: str) -> None:
    """Kiểm tra rồi lưu khóa; lỗi ghi của store lan lên người gọi."""
    store.save(validate_api_key(api_key))
