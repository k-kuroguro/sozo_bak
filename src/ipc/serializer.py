from typing import Generic, Type, TypeVar

from msgspec.msgpack import Decoder, Encoder

Msg = TypeVar("Msg")


class Serializer(Generic[Msg]):
    def __init__(self, type: Type[Msg] | None = None):
        self._encoder = Encoder()
        self._decoder = Decoder(type)

    def serialize(self, msg: Msg) -> bytes:
        return self._encoder.encode(msg)

    def desetialize(self, data: bytes) -> Msg:
        return self._decoder.decode(data)
