from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
import numpy as np
from loguru import logger

from ..discord_bot.message_types import GameEvent, GameModel, UpdateCellModel

def get_correct_map(axis: Axes, game: GameModel, history: dict[str, list[GameEvent]], timestamp: int):

    current_grid = np.array([
        [9 if game.solution[i][j] == '.' else 0 for i in range(len(game.solution[0]))]
        for j in range(len(game.solution))
    ])

    for cellChangeEvent in history["updateCell"]:
        assert isinstance(cellChangeEvent, UpdateCellModel)
        r, c = cellChangeEvent.params.cell.r, cellChangeEvent.params.cell.c

        current_grid[r][c] = 1 if game.solution[r][c] == cellChangeEvent.params.value else -1

        axis.imshow(current_grid)

        if cellChangeEvent.timestamp == timestamp:
            yield


