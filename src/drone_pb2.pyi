from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DroneData(_message.Message):
    __slots__ = ("node", "signal", "value", "timestamp")
    NODE_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    node: str
    signal: str
    value: float
    timestamp: int
    def __init__(self, node: _Optional[str] = ..., signal: _Optional[str] = ..., value: _Optional[float] = ..., timestamp: _Optional[int] = ...) -> None: ...

class Ack(_message.Message):
    __slots__ = ("ok", "reason")
    OK_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    ok: bool
    reason: str
    def __init__(self, ok: bool = ..., reason: _Optional[str] = ...) -> None: ...

class AlertEvent(_message.Message):
    __slots__ = ("source_node", "message", "timestamp")
    SOURCE_NODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    source_node: str
    message: str
    timestamp: int
    def __init__(self, source_node: _Optional[str] = ..., message: _Optional[str] = ..., timestamp: _Optional[int] = ...) -> None: ...

class ClientQuery(_message.Message):
    __slots__ = ("request",)
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    request: str
    def __init__(self, request: _Optional[str] = ...) -> None: ...

class ServerReply(_message.Message):
    __slots__ = ("reply",)
    REPLY_FIELD_NUMBER: _ClassVar[int]
    reply: str
    def __init__(self, reply: _Optional[str] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
