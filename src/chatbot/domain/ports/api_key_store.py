import abc


class ApiKeyStore(abc.ABC):
    """Nơi giữ khóa API duy nhất, không ghi ra log."""

    @abc.abstractmethod
    def is_configured(self) -> bool:
        """True khi đã có khóa không rỗng."""

    @abc.abstractmethod
    def get(self) -> str:
        """Trả khóa hiện tại, có thể rỗng."""

    @abc.abstractmethod
    def save(self, api_key: str) -> None:
        """Ghi khóa mới; lỗi ghi phải ném lại."""
