from pydantic import BaseModel
from typing import Any, List, Optional


class CellModel(BaseModel):
    r: int
    c: int


class ParentCellModel(BaseModel):
    across: int
    down: int


# game create models
class GridCellModel(BaseModel):
    black: bool
    edits: list[Any]
    number: Optional[int]
    parents: Optional[ParentCellModel] = None
    value: str


class ClockModel(BaseModel):
    lastUpdated: int
    paused: bool
    totalTime: int
    trueTotalTime: int


class ClueModel(BaseModel):
    across: list[Optional[str]]
    down: list[Optional[str]]


class InfoModel(BaseModel):
    author: str
    description: str
    title: str
    type: str


class ChatMessageModel(BaseModel):
    messages: list[str]


class GameModel(BaseModel):
    chat: ChatMessageModel
    circles: list[Any]  # unknown type
    clock: ClockModel
    clues: ClueModel
    cursor: Any  # unknown type
    grid: list[list[GridCellModel]]
    info: InfoModel
    solution: list[list[str]]


class CreateParams(BaseModel):
    pid: int
    version: int
    game: GameModel


class CreateEvent(BaseModel):
    timestamp: int
    type: str
    user: str
    params: CreateParams


class GameEvent(BaseModel):
    id: str
    timestamp: int
    type: str


# update cursor
class UpdateCursorParamsModel(BaseModel):
    id: str
    cell: CellModel
    timestamp: int


class UpdateCursorModel(GameEvent):
    params: UpdateCursorParamsModel


# update cell
class UpdateCellParamsModel(BaseModel):
    id: str
    cell: CellModel
    color: str
    pencil: bool
    value: str


class UpdateCellModel(GameEvent):
    params: UpdateCellParamsModel


# update display name
class UpdateDisplayNameParamsModel(BaseModel):
    displayName: str
    id: str


class UpdateDispayNameModel(GameEvent):
    params: UpdateDisplayNameParamsModel


# chat message
class ChatParamsModel(BaseModel):
    sender: str
    senderId: str
    text: str


class ChatModel(GameEvent):
    params: ChatParamsModel


# send chat messaage
class SendChatMessageParamsModel(BaseModel):
    id: str
    message: str
    sender: str


class SendChatMessageModel(GameEvent):
    params: SendChatMessageParamsModel


# reveal
class RevealParamsModel(BaseModel):
    scope: list[CellModel]


class RevealModel(GameEvent):
    params: RevealParamsModel


# check
class CheckParamsModel(BaseModel):
    scope: list[CellModel]


class CheckModel(GameEvent):
    params: CheckParamsModel


# updateColor
class UpdateColorParamsModel(BaseModel):
    color: str
    id: str


class UpdateColorModel(GameEvent):
    params: UpdateColorParamsModel


# updateClock
class UpdateClockParamsModel(BaseModel):
    action: str
    timestamp: int


class UpdateClockModel(GameEvent):
    params: UpdateClockParamsModel


# reset
class ResetParamsModel(BaseModel):
    force: bool
    scope: list[CellModel]


class ResetModel(GameEvent):
    params: ResetParamsModel


# add ping
class AddPingParamsModel(BaseModel):
    timestamp: int
    cell: CellModel
    id: str
class AddPingModel(GameEvent):
    params: AddPingParamsModel