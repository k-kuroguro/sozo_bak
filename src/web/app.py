from typing import Any

from flask import Flask

from . import routes


class App:
    def __init__(self, flask_app: Flask) -> None:
        self._flask_app = flask_app

    def run(
        self,
        host: str | None = None,
        port: int | None = None,
        debug: bool | None = None,
        load_dotenv: bool = True,
        **options: Any,
    ) -> None:
        self._flask_app.run(host, port, debug, load_dotenv, **options)


def create_app() -> App:
    flask_app = Flask(__name__)

    flask_app.register_blueprint(routes.bp)

    app = App(flask_app)
    return app
