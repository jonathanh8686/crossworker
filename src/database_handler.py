import json
from typing import TypedDict

import pyrebase # type: ignore

class ClueDict(TypedDict):
  across: list[str]
  down: list[str]

class DatabaseConnection():
  def __init__(self):
    config = json.loads(open("firebase_creds.json", "r").read())
    self.firebase = pyrebase.initialize_app(config)

  def get_clues(self, puzzle_id: str) -> ClueDict:
    return self.firebase.database().child("puzzle/30077").get().val()["clues"]

  def get_solution(self, puzzle_id: str) -> list[list[str]]:
    return self.firebase.database().child("puzzle/30077").get().val()["grid"]