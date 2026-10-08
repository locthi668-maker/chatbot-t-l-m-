from dataclasses import dataclass

ROLE_HUMAN = "human"
ROLE_AI = "ai"
ALLOWED_ROLES = (ROLE_HUMAN, ROLE_AI)


@dataclass(frozen=True)
class Message:
    """Một tin trong lịch sử hội thoại. Đóng băng để không sửa ngoài ý muốn."""

    role: str
    content: str

    def __post_init__(self) -> None:
        if not isinstance(self.role, str) or self.role not in ALLOWED_ROLES:
            raise ValueError("role phải là 'human' hoặc 'ai'")
        if not isinstance(self.content, str) or self.content.strip() == "":
            raise ValueError("content phải là chuỗi không rỗng")
