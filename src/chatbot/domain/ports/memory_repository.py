import abc

from ..message import Message


class MemoryRepository(abc.ABC):
    """Kho lịch sử theo session_id."""

    @abc.abstractmethod
    def get(self, session_id: str) -> list[Message]:
        """Trả lịch sử của một phiên, rỗng nếu chưa có."""

    @abc.abstractmethod
    def append(self, session_id: str, messages: list[Message]) -> None:
        """Nối thêm tin vào cuối phiên."""

    @abc.abstractmethod
    def reset(self, session_id: str) -> None:
        """Xoá sạch một phiên; phiên chưa tồn tại vẫn coi là thành công."""
