import os
from pathlib import Path

from ..domain.ports.api_key_store import ApiKeyStore
from .atomic_write_text import atomic_write_text

TEN_KHOA = "OPENAI_API_KEY"


class EnvApiKeyStore(ApiKeyStore):
    """Đọc và ghi khóa API trong tệp .env bằng ghi nguyên tử."""

    def __init__(self, env_path):
        self._path = Path(env_path)

    def is_configured(self):
        return bool(self.get())

    def get(self):
        if self._path.exists():
            for dong in self._doc().splitlines():
                if self._la_dong_khoa(dong):
                    return dong.strip().split("=", 1)[1].strip()
        return os.environ.get(TEN_KHOA, "")

    def save(self, api_key):
        dong_cu = [d for d in self._doc().splitlines() if d.strip()] if self._path.exists() else []
        vi_tri = next((i for i, d in enumerate(dong_cu) if self._la_dong_khoa(d)), None)
        giu_lai = [d for d in dong_cu if not self._la_dong_khoa(d)]
        giu_lai.insert(len(giu_lai) if vi_tri is None else vi_tri, TEN_KHOA + "=" + api_key)
        atomic_write_text(self._path, "\n".join(giu_lai) + "\n")
        os.environ[TEN_KHOA] = api_key

    def _doc(self):
        try:
            raw = self._path.read_bytes()
            return raw.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
        except (OSError, UnicodeDecodeError):
            return ""

    def _la_dong_khoa(self, dong):
        return dong.strip().startswith(TEN_KHOA + "=")
