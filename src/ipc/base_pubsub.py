from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

Msg = TypeVar("Msg")


class BasePublisher(Generic[Msg], metaclass=ABCMeta):
    @abstractmethod
    def publish(self, msg: Msg) -> None:
        """Publish a message to subscribers.

        Raises:
            ValueError: If the communication channel is already closed.
        """
        ...

    @abstractmethod
    def close(self) -> None:
        """Close the communication channel."""
        ...


class BaseSubscriber(metaclass=ABCMeta):
    @abstractmethod
    def start(self) -> None:
        """Begin an event loop to handle incoming messages.

        This must be called at most once.

        Raises:
            RuntimeError: If this method is called more than once.
            ValueError: If the communication channel is already closed.
        """
        ...

    @abstractmethod
    def close(self) -> None:
        """End an event loop and close the communication channel."""
        ...
