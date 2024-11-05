from ipc import ConcentrationStatus


class Store:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Store, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self._status: ConcentrationStatus | None = None

    def update_status(self, status: ConcentrationStatus | None) -> None:
        self._status = status

    def get_status(self) -> ConcentrationStatus | None:
        return self._status


store = Store()
