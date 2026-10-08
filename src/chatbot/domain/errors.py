class ChatbotError(Exception):
    """Lỗi gốc của chatbot."""


class ApiKeyMissing(ChatbotError):
    """Chưa có khóa API trong bộ nhớ tiến trình."""


class InvalidApiKey(ChatbotError):
    """Khóa API sai hình thức."""


class InvalidMessage(ChatbotError):
    """Tin người dùng rỗng hoặc quá dài."""


class InvalidSession(ChatbotError):
    """Mã phiên sai định dạng."""


class UpstreamError(ChatbotError):
    """Lỗi từ dịch vụ mô hình, mang theo mã trạng thái số nguyên."""

    def __init__(self, status: int, message: str) -> None:
        super().__init__(message)
        self.status = status
        self.message = message
