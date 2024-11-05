import datetime
from dataclasses import dataclass
from enum import Enum

from google.protobuf.message import DecodeError as _DecodeError

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

    type: Type
    msg: str


Payload = ConcentrationStatus | MonitorError


class MonitorMsg:
    """A message for the monitoring result or error."""

    def __init__(
        self,
        timestamp: datetime.datetime,
        payload: Payload,
    ) -> None:
        """Create a message.

        Args:
            timestamp (datetime.datetime): The timestamp indicating when the monitoring result was recorded.
            payload (Payload): The payload containing the monitoring result or error.
        """
        self._msg = _MonitorMsg()
        self._msg.timestamp.FromDatetime(timestamp)
        if isinstance(payload, ConcentrationStatus):
            self._msg.concentration_status.CopyFrom(
                _ConcentrationStatus(
                    overall_score=payload.overall_score,
                    sleeping_confidence=payload.sleeping_confidence,
                )
            )
        else:
            self._msg.error.CopyFrom(_MonitorError(type=payload.type.value, msg=payload.msg))

    def serialize(self) -> bytes:
        """Serialize the message to bytes.

        Returns:
            bytes: The serialized message.

        Raises:
            ValueError: If the message is not valid.
        """
        if not self._msg.HasField("timestamp"):
            raise ValueError("timestamp field is required")
        if not self._msg.HasField("concentration_status") and not self._msg.HasField("error"):
            raise ValueError("Either concentration_status or error field is required")

        return self._msg.SerializeToString()

    @classmethod
    def deserialize(cls, buf: bytes) -> "MonitorMsg":
        """Deserialize a message from bytes.

        Args:
            buf (bytes): The serialized message.

        Returns:
            MonitorMsg: The deserialized message.

        Raises:
            ValueError: If the deserialization fails.
        """
        msg = cls.__new__(cls)
        msg._msg = _MonitorMsg()

        try:
            msg._msg.ParseFromString(buf)
        except _DecodeError as e:
            raise ValueError(str(e))

        return msg

    @property
    def timestamp(self) -> datetime.datetime:
        return self._msg.timestamp.ToDatetime()

    @property
    def payload(self) -> Payload:
        return (
            ConcentrationStatus(
                overall_score=self._msg.concentration_status.overall_score,
                sleeping_confidence=self._msg.concentration_status.sleeping_confidence,
            )
            if self._msg.HasField("concentration_status")
            else MonitorError(
                type=MonitorError.Type(self._msg.error.type),
                msg=self._msg.error.msg,
            )
        )

    def __str__(self) -> str:
        return self._msg.__str__()
