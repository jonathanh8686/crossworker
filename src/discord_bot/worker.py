import json

from . import message_parser as mp
from enum import Enum
from loguru import logger
from .message_types import GameEvent, UpdateCellModel
from .socker_handler import WebsocketClient
from typing import Optional
from ..stats import stats


class WorkerState(Enum):
    Startup = 0
    InGame = 1
    Finishing = 2


class Worker:
    def __init__(self, game_id: str) -> None:
        logger.info(f"Creating worker for game {game_id}")
        self.game_id = game_id
        self.state = WorkerState.Startup

        self.solution: Optional[list[list[str]]] = None
        self.grid: list[list[str]] = []

        self.history: dict[str, list[GameEvent]] = {}

        self.event_map: dict[str, GameEvent] = {}
        logger.info(f"Testing stats import: {stats.print_data('Hello World')}")

    async def attach(self):
        await WebsocketClient().join_game(self.game_id, self.on_game_message)

    def __process_update_cell(self, event: UpdateCellModel):
        cell = event.params.cell
        self.grid[cell.r][cell.c] = event.params.value

    async def on_game_message(self, msg: str) -> None:
        if self.state == WorkerState.Startup and mp.is_sync_message(msg):
            create_event = await mp.parse_sync_event(msg)

            self.solution = create_event[0].params.game.solution
            self.grid = [
                ["." for _ in range(len(self.solution[0]))]
                for _ in range(len(self.solution))
            ]
            self.state = WorkerState.InGame

            for prior in create_event[1]:
                if prior[0] not in self.history:
                    self.history[prior[0]] = []
                self.history[prior[0]].append(prior[1])
                if prior[0] == "updateCell":
                    assert isinstance(prior[1], UpdateCellModel)
                    self.__process_update_cell(prior[1])

        if self.state == WorkerState.InGame and mp.is_game_event(msg):
            event_json = await mp.parse_game_event(msg)

            if event_json[0] not in self.history:
                self.history[event_json[0]] = []
            self.history[event_json[0]].append(event_json[1])

            if event_json[0] == "updateCell":
                assert isinstance(event_json[1], UpdateCellModel)
                self.__process_update_cell(event_json[1])

            solved = True
            assert self.solution is not None
            for r_ind in range(len(self.solution)):
                for c_ind in range(len(self.solution[r_ind])):
                    if self.solution[r_ind][c_ind] != self.grid[r_ind][c_ind]:
                        solved = False
                        break
                if not solved:
                    break

            if solved:
                self.state = WorkerState.Finishing

        if self.state == WorkerState.Finishing:
            stats.print_data(self.history)
