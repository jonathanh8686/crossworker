import asyncio
from loguru import logger

from database_handler import DatabaseClient
from socker_handler import WebsocketClient


class Worker:
    def __init__(self, game_id: str) -> None:
        self.game_id = game_id
        logger.info(f"Creating worker for game {game_id}")

    async def attach(self):
        await WebsocketClient().join_game(self.game_id, self.on_game_event)

    async def on_game_event(self, event: str) -> None:
        logger.debug(event)
