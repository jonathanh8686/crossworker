import matplotlib.pyplot as plt
import pandas as pd
from loguru import logger

from ..discord_bot.message_types import GameEvent, GameModel, UpdateCellModel

def get_correct_map(game: GameModel, history: dict[str, list[GameEvent]]):
    current_grid = [
        [0 for _ in range(len(game.solution[0]))]
        for _ in range(len(game.solution))
    ]
    
    for cellChangeEvent in history["updateCell"]:
        assert isinstance(cellChangeEvent, UpdateCellModel)
        r, c = cellChangeEvent.params.cell.r, cellChangeEvent.params.cell.c

        current_grid[r][c] = cellChangeEvent.params.value

        solved_blanks = 0
        for row_ind in range(len(game.solution)):
            for col_ind in range(len(game.solution[row_ind])):
                solved_blanks += (
                    1
                    if game.solution[row_ind][col_ind]
                    == current_grid[row_ind][col_ind]
                    else 0
                )



