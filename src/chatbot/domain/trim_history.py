from .message import Message


def trim_history(messages: list[Message], limit: int) -> list[Message]:
    """Trả list MỚI chứa tối đa `limit` tin CUỐI, giữ nguyên thứ tự."""
    if isinstance(limit, bool) or not isinstance(limit, int) or limit <= 0:
        raise ValueError("limit phải là số nguyên lớn hơn 0")
    if len(messages) == 0:
        return []
    return list(messages[-limit:])
