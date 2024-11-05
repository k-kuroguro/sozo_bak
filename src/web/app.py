from typing import Any

from flask import Flask

from ipc import BaseSubscriber, ConcentrationStatus, MonitorMsg

from . import routes
from .store import store


class App:
    def __init__(self, subscriber: BaseSubscriber[MonitorMsg]) -> None:
        self._subscriber = subscriber

        self._flask_app = Flask(__name__)
        self._flask_app.register_blueprint(routes.bp)

    def run(
        self,
        host: str | None = None,
        port: int | None = None,
        debug: bool | None = None,
        load_dotenv: bool = True,
        **options: Any,
    ) -> None:
        self._subscriber.start(self._update_status)
        self._flask_app.run(host, port, debug, load_dotenv, **options)

    def _update_status(self, msg: MonitorMsg) -> None:
        if isinstance(msg.payload, ConcentrationStatus):
            store.update_status(msg.payload)
        else:
            store.update_status(None)
