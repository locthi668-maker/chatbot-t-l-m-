from src.chatbot.application.validate_message import validate_message
from src.chatbot.application.validate_session_id import validate_session_id
from src.chatbot.domain.errors import ApiKeyMissing, UpstreamError
from src.chatbot.domain.message import Message
from src.chatbot.domain.ports.api_key_store import ApiKeyStore
from src.chatbot.domain.ports.chat_model import ChatModel
from src.chatbot.domain.ports.memory_repository import MemoryRepository
from src.chatbot.domain.trim_history import trim_history

EMPTY_REPLY_STATUS = 502
EMPTY_REPLY_MESSAGE = "Mô hình trả lời rỗng"


def send_message(
    repo: MemoryRepository,
    model: ChatModel,
    store: ApiKeyStore,
    system_prompt: str,
    max_messages: int,
    session_id: str,
    text: str,
) -> str:
    """Thứ tự cứng: kiểm đầu vào, kiểm khóa, đọc bộ nhớ, gọi mô hình, rồi mới ghi."""
    sid = validate_session_id(session_id)
    message = validate_message(text)
    if not store.is_configured():
        raise ApiKeyMissing("Chưa có khóa API, cần nhập khóa trước")
    history = trim_history(repo.get(sid), max_messages)
    reply = model.reply(system_prompt, history, message)
    if not isinstance(reply, str) or not reply.strip():
        raise UpstreamError(EMPTY_REPLY_STATUS, EMPTY_REPLY_MESSAGE)
    repo.append(sid, [Message("human", message), Message("ai", reply)])
    return reply
