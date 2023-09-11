import json

import pyrebase  # type: ignore
from typing import TypedDict
from loguru import logger


class ClueDict(TypedDict):
    across: list[str]
    down: list[str]

class DatabaseClient:
    def __init__(self):
        config = json.loads(open("firebase_creds.json", "r").read())
        self.firebase = pyrebase.initialize_app(config)
        logger.info("Connected to Firebase")

    def get_clues(self, puzzle_id: str) -> ClueDict:
        return (
            self.firebase.database().child(f"puzzle/{puzzle_id}").get().val()["clues"]
        )

    def get_solution(self, puzzle_id: str) -> list[list[str]]:
        return (
            self.firebase.database().child(f"puzzle/{puzzle_id}").get().val()["grid"]
        )