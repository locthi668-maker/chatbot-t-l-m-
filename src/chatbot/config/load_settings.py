from pathlib import Path

from dotenv import dotenv_values

from src.chatbot.config.settings import Settings
from src.chatbot.config.settings_error import SettingsError

DEFAULTS = {
    "OPENAI_API_KEY": "",
    "OPENAI_MODEL": "gpt-4o-mini",
    "OPENAI_TEMPERATURE": "0.3",
    "OPENAI_TIMEOUT": "30",
    "HOST": "127.0.0.1",
    "PORT": "2610",
    "MEMORY_FILE": "memory.json",
    "MAX_MESSAGES": "5",
    "SYSTEM_PROMPT_FILE": "system-prompt.txt",
}

ALLOWED_HOSTS = ("127.0.0.1", "localhost")


def _as_text(key: str, raw: str) -> str:
    value = (raw or "").strip()
    if value == "":
        raise SettingsError(f"Khóa {key} không được để trống.")
    return value


def _as_int(key: str, raw: str, low: int, high: int) -> int:
    try:
        value = int(str(raw).strip())
    except (TypeError, ValueError):
        raise SettingsError(
            f"Khóa {key} phải là số nguyên từ {low} đến {high}; "
            f"giá trị đọc được không phải số nguyên."
        ) from None
    if not low <= value <= high:
        raise SettingsError(
            f"Khóa {key} phải nằm trong khoảng {low} đến {high}; nhận được {value}."
        )
    return value


def _as_float(key: str, raw: str, low: float, high: float) -> float:
    try:
        value = float(str(raw).strip())
    except (TypeError, ValueError):
        raise SettingsError(
            f"Khóa {key} phải là số thực từ {low} đến {high}; "
            f"giá trị đọc được không phải số thực."
        ) from None
    if not low <= value <= high:
        raise SettingsError(
            f"Khóa {key} phải nằm trong khoảng {low} đến {high}; nhận được {value}."
        )
    return value


def _read_env(env_path) -> dict:
    path = Path(env_path)
    if not path.is_file():
        return {}
    values = dotenv_values(path, encoding="utf-8-sig")
    return {k: v for k, v in values.items() if k}


def load_settings(env_path=".env") -> Settings:
    raw = _read_env(env_path)
    host = _as_text("HOST", raw.get("HOST", DEFAULTS["HOST"])).lower()
    if host not in ALLOWED_HOSTS:
        raise SettingsError(
            f"Khóa HOST chỉ chấp nhận 127.0.0.1 hoặc localhost; nhận được {host}."
        )
    return Settings(
        openai_api_key=(raw.get("OPENAI_API_KEY", "") or "").strip(),
        openai_model=_as_text("OPENAI_MODEL", raw.get("OPENAI_MODEL", DEFAULTS["OPENAI_MODEL"])),
        openai_temperature=_as_float("OPENAI_TEMPERATURE", raw.get("OPENAI_TEMPERATURE", DEFAULTS["OPENAI_TEMPERATURE"]), 0.0, 2.0),
        openai_timeout=_as_int("OPENAI_TIMEOUT", raw.get("OPENAI_TIMEOUT", DEFAULTS["OPENAI_TIMEOUT"]), 1, 300),
        host=host,
        port=_as_int("PORT", raw.get("PORT", DEFAULTS["PORT"]), 1024, 65535),
        memory_file=_as_text("MEMORY_FILE", raw.get("MEMORY_FILE", DEFAULTS["MEMORY_FILE"])),
        max_messages=_as_int("MAX_MESSAGES", raw.get("MAX_MESSAGES", DEFAULTS["MAX_MESSAGES"]), 1, 50),
        system_prompt_file=_as_text("SYSTEM_PROMPT_FILE", raw.get("SYSTEM_PROMPT_FILE", DEFAULTS["SYSTEM_PROMPT_FILE"])),
    )
