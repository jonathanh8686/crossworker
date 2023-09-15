from pydantic import BaseModel

class Cell(BaseModel):
    r: int
    c: int

class UpdateCursorMessage(BaseModel):
    id: int
    timestamp: int
    cell: Cell
