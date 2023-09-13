import asyncio
import message_parser as mp
from loguru import logger


from database_handler import DatabaseClient
from socker_handler import WebsocketClient


class Worker:
    def __init__(self, game_id: str) -> None:
        self.game_id = game_id
        logger.info(f"Creating worker for game {game_id}")

    async def attach(self):
        await WebsocketClient().join_game(self.game_id, self.on_game_message)

    async def on_game_message(self, msg: str) -> None:

        if mp.is_game_event(msg):
            json = await mp.game_event_to_json(msg)
            if 'value' in json: #testing stuff below, value key is only used for storing character changes
                logger.info(json['value'])
            with open("test.dat", "a") as f:
                f.write("\n" + msg)