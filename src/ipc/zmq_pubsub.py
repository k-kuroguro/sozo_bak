from threading import Thread

import zmq

from .base_pubsub import BasePublisher, BaseSubscriber
from .msg_types import MonitorMsg


class ZMQPublisher(BasePublisher[MonitorMsg]):
    def __init__(self, addr: str, topic: str):
        self._topic = topic

        self._ctx = zmq.Context()
        self._socket = self._ctx.socket(zmq.PUB)
        self._socket.bind(addr)

    def publish(self, msg: MonitorMsg) -> None:
        if self._socket.closed:
            raise ValueError("Publisher is closed")

        self._socket.send_multipart([self._topic.encode(), msg.serialize()])

    def close(self) -> None:
        self._socket.close()
        self._ctx.term()


class ZMQSubscriber(BaseSubscriber[MonitorMsg]):
    def __init__(self, addr: str, topic: str):
        self._topic = topic
        self._thread: Thread | None = None
        self._is_running = False

        self._ctx = zmq.Context()
        self._socket = self._ctx.socket(zmq.SUB)
        self._socket.connect(addr)
        self._socket.subscribe(topic.encode())

    def start(self, callback) -> None:
        if self._is_running:
            raise RuntimeError("Subscriber is already running")
        if self._socket.closed:
            raise ValueError("Subscriber is closed")

        self._is_running = True
        self._thread = Thread(target=self._run, args=(callback,), daemon=True)
        self._thread.start()

    def _run(self, callback) -> None:
        poller = zmq.Poller()
        poller.register(self._socket, zmq.POLLIN)
        while self._is_running:
            if self._socket in dict(poller.poll(100)):
                _, msg = self._socket.recv_multipart()
                callback(MonitorMsg.deserialize(msg))

    def close(self) -> None:
        self._is_running = False
        if self._thread and self._thread.is_alive():
            self._thread.join()
        self._socket.close()
        self._ctx.term()