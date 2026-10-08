from src.chatbot.domain.ports.api_key_store import ApiKeyStore


def get_setup_status(store: ApiKeyStore) -> dict:
    """Báo đã cấu hình khóa hay chưa, KHÔNG trả về khóa."""
    return {"configured": bool(store.is_configured())}
