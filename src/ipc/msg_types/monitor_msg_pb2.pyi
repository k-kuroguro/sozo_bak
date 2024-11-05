from typing import ClassVar as _ClassVar
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class MonitorMsg(_message.Message):
    __slots__ = ("timestamp", "concentration_status", "error")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    CONCENTRATION_STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    concentration_status: ConcentrationStatus
    error: Error
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., concentration_status: _Optional[_Union[ConcentrationStatus, _Mapping]] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ConcentrationStatus(_message.Message):
    __slots__ = ("overall_score", "sleeping_confidence")
    OVERALL_SCORE_FIELD_NUMBER: _ClassVar[int]
    SLEEPING_CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    overall_score: float
    sleeping_confidence: float
    def __init__(self, overall_score: _Optional[float] = ..., sleeping_confidence: _Optional[float] = ...) -> None: ...

class Error(_message.Message):
    __slots__ = ("type", "msg")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[Error.Type]
    UNKNOWN: Error.Type
    TYPE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    type: Error.Type
    msg: str
    def __init__(self, type: _Optional[_Union[Error.Type, str]] = ..., msg: _Optional[str] = ...) -> None: ...
