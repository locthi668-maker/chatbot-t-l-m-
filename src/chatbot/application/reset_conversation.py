from src.chatbot.application.validate_session_id import validate_session_id
from src.chatbot.domain.ports.memory_repository import MemoryRepository


def reset_conversation(repo: MemoryRepository, session_id: str) -> None:
    """Xóa lịch sử một phiên; phiên chưa tồn tại thì thành công im lặng."""
    repo.reset(validate_session_id(session_id))
