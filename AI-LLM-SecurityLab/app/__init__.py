from flask import Flask
from pathlib import Path


def create_app():
    project_root = Path(__file__).resolve().parent.parent

    app = Flask(
        __name__,
        template_folder=str(project_root / "templates"),
        static_folder=str(project_root / "static")
    )

    from app.routes import main
    app.register_blueprint(main)

    return app