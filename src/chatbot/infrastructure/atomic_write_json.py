import json

from .atomic_write_text import atomic_write_text


def atomic_write_json(path, data):
    """Ghi JSON UTF-8 thụt lề 2 rồi chuyển sang atomic_write_text."""
    noi_dung = json.dumps(data, ensure_ascii=False, indent=2)
    return atomic_write_text(path, noi_dung + "\n")
