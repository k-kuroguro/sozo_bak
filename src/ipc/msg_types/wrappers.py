import datetime
from dataclasses import dataclass
from enum import Enum

from google.protobuf.message import DecodeError as _DecodeError
from google.protobuf.message import EncodeError as _EncodeError

from .monitor_msg_pb2 import ConcentrationStatus as _ConcentrationStatus
from .monitor_msg_pb2 import Error as _MonitorError
from .monitor_msg_pb2 import MonitorMsg as _MonitorMsg


@dataclass(slots=True, frozen=True)
class ConcentrationStatus:
    overall_score: float
    sleeping_confidence: float


@dataclass(slots=True, frozen=True)
class MonitorError:
    class Type(int, Enum):
        UNKNOWN = _MonitorError.Type.UNKNOWN

        def __str__(self) -> str:
            return self.name

    type: Type
    msg: str


Payload = ConcentrationStatus | MonitorError


@dataclass(slots=True, frozen=True)
class MonitorMsg:
    """A message for the monitoring result or error.

    Args:
        timestamp (datetime.datetime): Timestamp indicating when the monitoring result was recorded.
        payload (Payload): Monitoring result or error.
    """

    timestamp: datetime.datetime
    payload: Payload

    def serialize(self) -> bytes:
        """Serialize the message to bytes.

        Returns:
            bytes: The serialized message.

        Raises:
            ValueError: If serialization fails.
        """

        proto = _MonitorMsg()
        proto.timestamp.FromDatetime(self.timestamp)
        if isinstance(self.payload, ConcentrationStatus):
            proto.payload.concentration_status.CopyFrom(
                _ConcentrationStatus(
                    overall_score=self.payload.overall_score,
                    sleeping_confidence=self.payload.sleeping_confidence,
                )
            )
        else:
            proto.payload.error.CopyFrom(
                _MonitorError(
                    type=self.payload.type.value,
                    msg=self.payload.msg,
                )
            )

        try:
            return proto.SerializeToString()
        except _EncodeError as e:
            raise ValueError(str(e))

    @classmethod
    def deserialize(cls, buf: bytes) -> "MonitorMsg":
        """Deserialize the message from bytes.

        Args:
            buf (bytes): The serialized message.

        Returns:
            MonitorMsg: The deserialized message.

        Raises:
            ValueError: If deserialization fails.
        """

        proto = _MonitorMsg()
        try:
            proto.ParseFromString(buf)
        except _DecodeError as e:
            raise ValueError(str(e))

        payload: Payload
        if proto.HasField("concentration_status"):
            payload = ConcentrationStatus(
                overall_score=proto.payload.concentration_status.overall_score,
                sleeping_confidence=proto.payload.concentration_status.sleeping_confidence,
            )
        else:
            payload = MonitorError(
                type=MonitorError.Type(proto.payload.error.type),
                msg=proto.payload.error.msg,
            )

        return MonitorMsg(
            timestamp=proto.timestamp.ToDatetime(),
            payload=payload,
        )
