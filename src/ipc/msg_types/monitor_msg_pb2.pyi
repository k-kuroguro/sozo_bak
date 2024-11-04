from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MonitorMsg(_message.Message):
    __slots__ = ("timestamp", "study_state", "error")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    STUDY_STATE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    study_state: StudyState
    error: Error
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., study_state: _Optional[_Union[StudyState, _Mapping]] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class StudyState(_message.Message):
    __slots__ = ("concentration_score", "sleeping_confidence")
    CONCENTRATION_SCORE_FIELD_NUMBER: _ClassVar[int]
    SLEEPING_CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    concentration_score: float
    sleeping_confidence: float
    def __init__(self, concentration_score: _Optional[float] = ..., sleeping_confidence: _Optional[float] = ...) -> None: ...

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
