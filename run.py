import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from src.chatbot.config.load_settings import load_settings
from src.chatbot.config.settings_error import SettingsError
from src.chatbot.infrastructure.env_api_key_store import EnvApiKeyStore
from src.chatbot.infrastructure.json_memory_repository import JsonMemoryRepository
from src.chatbot.infrastructure.langchain_chat_model import LangChainChatModel
from src.chatbot.infrastructure.load_system_prompt import load_system_prompt
from src.chatbot.interface.create_app import create_app


def build_deps(settings):
    """Dựng đúng năm phụ thuộc mà tầng interface cần."""
    store = EnvApiKeyStore(ROOT / ".env")
    return {
        "settings": settings,
        "store": store,
        "repo": JsonMemoryRepository(ROOT / settings.memory_file),
        "model": LangChainChatModel(settings, store),
        "system_prompt_loader": lambda path: load_system_prompt(ROOT / path),
        "static_dir": ROOT / "static",
    }


def main():
    """Trả 0 khi chạy tốt, trả 1 khi cấu hình sai hoặc cổng bận."""
    try:
        settings = load_settings(ROOT / ".env")
    except SettingsError as exc:
        print(f"Lỗi cấu hình trong tệp .env: {exc}")
        return 1
    app = create_app(build_deps(settings))
    print(f"Chatbot đang chạy tại http://{settings.host}:{settings.port}")
    try:
        app.run(host=settings.host, port=settings.port, debug=False)
    except OSError:
        print(f"Cổng {settings.port} đang bận. Hãy đổi PORT trong tệp .env rồi chạy lại.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
