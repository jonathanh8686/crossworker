from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    timestamp: int
    id: Optional[int]

class Cell(BaseModel):
    r: int
    c: int

class UpdateCursorMessage(Message):
    cell: Cell

class UpdateCellMessage(Message):
    cell: Cell
    value: str
    pencil: bool

class UpdateDisplayNameMessage(Message):
    displayName: str

class RevealMessage(Message):
    cells: List[Cell]

class ResetMessage(Message):
    cells: List[Cell]

class CheckMessage(Message):
    cells: List[Cell]

class UpdateClockMessage(Message):
    action: str


