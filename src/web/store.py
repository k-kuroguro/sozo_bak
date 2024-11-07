from asyncio import Event
from threading import Lock

from ipc import MonitorMsg


class IncomingDataStore:
    """Singleton class to store the incoming data via IPC."""

    _instance: "IncomingDataStore | None" = None
    _lock = Lock()

    def __new__(cls) -> "IncomingDataStore":
        if cls._instance is None:
            with cls._lock:
                cls._instance = super(IncomingDataStore, cls).__new__(cls)
                cls._instance._initialized = False  # type: ignore
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:  # type: ignore
            return
        self._initialized = True
        self._latest_monitor_msg: MonitorMsg | None = None
        self._changed_event = Event()

    @property
    def latest_monitor_msg(self) -> MonitorMsg | None:
        return self._latest_monitor_msg

    @latest_monitor_msg.setter
    def latest_monitor_msg(self, value: MonitorMsg | None) -> None:
        self._latest_monitor_msg = value
        self._changed_event.set()
        self._changed_event.clear()
