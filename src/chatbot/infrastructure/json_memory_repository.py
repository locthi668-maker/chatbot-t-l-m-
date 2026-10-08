import json
import threading
import time
from pathlib import Path

from ..domain.message import Message
from ..domain.ports.memory_repository import MemoryRepository
from .atomic_write_json import atomic_write_json


class JsonMemoryRepository(MemoryRepository):
    """Kho lịch sử hội thoại trong tệp JSON, mọi thao tác nằm sau khóa luồng."""

    def __init__(self, path):
        self._path = Path(path)
        self._lock = threading.Lock()

    def get(self, session_id):
        with self._lock:
            du_lieu = self._doc()
        tin = []
        for muc in du_lieu.get(session_id, []):
            try:
                tin.append(Message(muc["role"], muc["content"]))
            except (KeyError, TypeError, ValueError):
                continue
        return tin

    def append(self, session_id, messages):
        moi = [{"role": m.role, "content": m.content} for m in messages]
        with self._lock:
            du_lieu = self._doc()
            du_lieu.setdefault(session_id, []).extend(moi)
            atomic_write_json(self._path, du_lieu)

    def reset(self, session_id):
        with self._lock:
            du_lieu = self._doc()
            if session_id not in du_lieu:
                return
            del du_lieu[session_id]
            atomic_write_json(self._path, du_lieu)

    def _doc(self):
        if not self._path.exists():
            return {}
        try:
            du_lieu = json.loads(self._path.read_text(encoding="utf-8-sig"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            du_lieu = None
        if isinstance(du_lieu, dict):
            return du_lieu
        self._cach_ly()
        return {}

    def _cach_ly(self):
        ten = self._path.name + ".corrupt-" + str(int(time.time()))
        try:
            self._path.replace(self._path.with_name(ten))
        except OSError:
            pass
