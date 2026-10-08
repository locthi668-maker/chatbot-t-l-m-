from pathlib import Path

DEFAULT_SYSTEM_PROMPT = (
    "Bạn là trợ lý học tập của lớp học Python.\n"
    "Trả lời ngắn gọn, rõ ràng, đúng tiếng Việt có dấu."
)


def load_system_prompt(path) -> str:
    """Đọc lệnh hệ thống; thiếu tệp hoặc rỗng thì trả lệnh mặc định, không sập."""
    target = Path(path)
    try:
        text = target.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError):
        return DEFAULT_SYSTEM_PROMPT
    cleaned = text.replace("\ufeff", "").strip()
    if not cleaned:
        return DEFAULT_SYSTEM_PROMPT
    return cleaned
