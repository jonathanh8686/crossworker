import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from loguru import logger
from matplotlib.axes import Axes

from ..discord_bot.message_types import GameEvent, GameModel, UpdateCellModel


def get_correct_map(
    axis: Axes,
    game: GameModel,
    history: dict[str, list[GameEvent]],
    timestamp: int,
):
    color_map = {
        -1: np.array([255, 0, 0]),
        1: np.array([0, 255, 0]),
        0: np.array([0, 0, 0]),
    }

    current_grid = np.array(
        [
            [0 for i in range(len(game.solution[0]))]
            for j in range(len(game.solution))
        ]
    )

    axis.axis("off")  # type: ignore
    color_grid = np.ndarray(
        shape=(current_grid.shape[0], current_grid.shape[1], 3), dtype=int
    )
    for cellChangeEvent in history["updateCell"]:
        assert isinstance(cellChangeEvent, UpdateCellModel)
        r, c = cellChangeEvent.params.cell.r, cellChangeEvent.params.cell.c

        current_grid[r][c] = (
            1 if game.solution[r][c] == cellChangeEvent.params.value else -1
        )
        color_grid[r][c] = color_map[current_grid[r][c]]
        axis.imshow(color_grid, cmap="RdYlGn")

        if cellChangeEvent.timestamp == timestamp:
            yield
