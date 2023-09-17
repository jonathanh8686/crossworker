import json

import message_parser as mp
from enum import Enum
from loguru import logger
from message_types import GameEvent
from socker_handler import WebsocketClient


class WorkerState(Enum):
    Startup = 0
    InGame = 1
    Finishing = 2


class Worker:
    def __init__(self, game_id: str) -> None:
        logger.info(f"Creating worker for game {game_id}")
        self.game_id = game_id
        self.state = WorkerState.Startup

        self.event_map: dict[str, GameEvent] = {}

    async def attach(self):
        await WebsocketClient().join_game(self.game_id, self.on_game_message)

    async def on_game_message(self, msg: str) -> None:
        if self.state == WorkerState.Startup and mp.is_sync_message(msg):
            create_event = await mp.parse_sync_event(msg)
            print(create_event)

        if mp.is_game_event(msg):
            event_json = await mp.parse_game_event(msg)
            print(event_json)
