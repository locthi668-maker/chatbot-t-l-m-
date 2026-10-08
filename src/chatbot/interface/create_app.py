from pathlib import Path

from flask import Flask, send_from_directory

from src.chatbot.interface.json_error import register_error_handlers
from src.chatbot.interface.routes.chat_route import chat_bp
from src.chatbot.interface.routes.health_route import health_bp
from src.chatbot.interface.routes.reset_route import reset_bp
from src.chatbot.interface.routes.setup_route import setup_bp
from src.chatbot.interface.routes.setup_status_route import setup_status_bp

MAX_CONTENT_LENGTH = 16 * 1024
INDEX_FILE = "index.html"


def resolve_static_dir(deps):
    """Lấy thư mục static, suy từ MEMORY_FILE khi deps không khai báo."""
    given = deps.get("static_dir")
    if given is not None:
        return Path(given)
    memory_file = Path(deps["settings"].memory_file)
    return memory_file.resolve().parent / "static"


def create_app(deps=None, **kwargs) -> Flask:
    """Khoá chặt cấu hình, nạp blueprint, đăng ký xử lý lỗi."""
    if deps is None:
        deps = kwargs
    elif kwargs:
        deps = {**deps, **kwargs}
    app = Flask(__name__, static_folder=str(resolve_static_dir(deps)), static_url_path="/static")
    app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
    app.config["deps"] = deps
    for blueprint in (health_bp, setup_status_bp, setup_bp, chat_bp, reset_bp):
        app.register_blueprint(blueprint)
    register_error_handlers(app)

    @app.get("/")
    def index():
        """Phục vụ trang nhập khóa API và khung chat."""
        return send_from_directory(app.static_folder, INDEX_FILE)

    return app
