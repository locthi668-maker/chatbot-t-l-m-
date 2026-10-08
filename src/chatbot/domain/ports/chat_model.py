import abc

from ..message import Message


class ChatModel(abc.ABC):
    """Nguồn sinh câu trả lời."""

    @abc.abstractmethod
    def reply(self, system_prompt: str, history: list[Message], user_text: str) -> str:
        """Trả về nội dung trả lời dạng chuỗi không rỗng."""
