import datetime
from dataclasses import dataclass
from enum import Enum, auto


@dataclass(slots=True, frozen=True)
class ConcentrationStatus:
    """Represents the mearured concentration score

    Args:
        overall_score (float): Overall concentration score.
        sleeping_confidence (float): Confidence score of the sleeping state.
    """

    overall_score: float
    sleeping_confidence: float


@dataclass(slots=True, frozen=True)
class MonitorError:
    """Represents an error in measurement.

    Args:
        type (Type): Type of the error.
        msg (str): Error message.
    """

    class Type(int, Enum):
        """Enumerate types of errors in measurement."""

        UNKNOWN = auto()
        """Unknown error."""

    type: Type
    msg: str


Payload = ConcentrationStatus | MonitorError


@dataclass(slots=True, frozen=True)
class MonitorMsg:
    """Represents a monitoring result or error.

    Args:
        timestamp (datetime.datetime): Timestamp indicating when the monitoring result was recorded.
        payload (Payload): Monitoring result or error.
    """

    timestamp: datetime.datetime
    payload: Payload
