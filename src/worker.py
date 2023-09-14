import asyncio
import message_parser as mp
from loguru import logger


from database_handler import DatabaseClient
from socker_handler import WebsocketClient


class Worker:
    def __init__(self, game_id: str) -> None:
        self.game_id = game_id
        self.id_to_username: dict[str, str] = {}
        logger.info(f"Creating worker for game {game_id}")

    async def attach(self):
        await WebsocketClient().join_game(self.game_id, self.on_game_message)

    async def on_game_message(self, msg: str) -> None:

        if mp.is_game_event(msg):
            event_json = await mp.game_event_to_json(msg)
            #json always contains: type, timestamp, cell, id,

            match event_json['type']:
                case "updateDisplayName":
                    self.id_to_username[event_json['id']] = event_json['displayName']
                    logger.info(f"user id {event_json['id']} changed username to {event_json['displayName']}")
                    
                case "updateCell":
                    logger.info(f"Cell ({event_json['cell']['r']}, {event_json['cell']['c']}) updated to {event_json['value']}")


            with open("test.dat", "a") as f:
                f.write("\n" + msg)