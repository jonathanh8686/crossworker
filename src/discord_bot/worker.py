import json

from enum import Enum
from loguru import logger
from typing import Callable, Optional

from ..stats import stats
from . import message_parser as mp
from .message_types import GameEvent, GameModel, UpdateCellModel
from .socker_handler import WebsocketClient


class WorkerState(Enum):
    Startup = 0
    InGame = 1
    Finishing = 2


class Worker:
    def __init__(self, game_id: str, destroy: Callable[[], None]) -> None:
        logger.info(f"Creating worker for game {game_id}")
        self.game_id = game_id
        self.state = WorkerState.Startup

        self.game: Optional[GameModel] = None
        self.grid: list[list[str]] = []

        self.history: dict[str, list[GameEvent]] = {}

        self.event_map: dict[str, GameEvent] = {}
        self.destroy = destroy

        self.websocket_client = WebsocketClient()

    async def attach(self):
        await self.websocket_client.join_game(self.game_id, self.on_game_message)

    def __process_update_cell(self, event: UpdateCellModel):
        cell = event.params.cell
        self.grid[cell.r][cell.c] = event.params.value
    
    def __game_completed(self) -> bool:
        assert self.game is not None and self.game.solution is not None
        for r_ind in range(len(self.game.solution)):
            for c_ind in range(len(self.game.solution[r_ind])):
                if (
                    self.game.solution[r_ind][c_ind]
                    != self.grid[r_ind][c_ind]
                ):
                    return False
        return True

    async def on_game_message(self, msg: str) -> None:
        if self.state == WorkerState.Startup and mp.is_sync_message(msg):
            create_event = await mp.parse_sync_event(msg)

            self.game = create_event[0].params.game
            self.grid = [
                ["." for _ in range(len(self.game.solution[0]))]
                for _ in range(len(self.game.solution))
            ]
            self.state = WorkerState.InGame

            for prior in create_event[1]:
                if prior[0] not in self.history:
                    self.history[prior[0]] = []
                self.history[prior[0]].append(prior[1])
                if prior[0] == "updateCell":
                    assert isinstance(prior[1], UpdateCellModel)
                    self.__process_update_cell(prior[1])
            
            if self.__game_completed():
                self.state = WorkerState.Finishing

        if self.state == WorkerState.InGame and mp.is_game_event(msg):
            event_json = await mp.parse_game_event(msg)

            if event_json[0] not in self.history:
                self.history[event_json[0]] = []
            self.history[event_json[0]].append(event_json[1])

            if event_json[0] == "updateCell":
                assert isinstance(event_json[1], UpdateCellModel)
                self.__process_update_cell(event_json[1])

            if self.__game_completed():
                self.state = WorkerState.Finishing

        if self.state == WorkerState.Finishing:
            logger.info(f"Detected game {self.game_id} is finished")
            assert self.game is not None
            stats_object = stats.Statistics(self.game, self.history)
            stats_object.get_visualization()

            self.websocket_client.game_running = False
            assert self.websocket_client.listen_task is not None
            assert self.websocket_client.heartbeat_task is not None
            self.websocket_client.listen_task.cancel()
            self.websocket_client.heartbeat_task.cancel()
            self.destroy()