from typing import Optional
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import pandas as pd
from loguru import logger
from matplotlib.axes import Axes

from ..discord_bot.message_types import GameEvent, GameModel, UpdateCellModel


def get_completion_line(
    axis: Axes,
    game: GameModel,
    history: dict[str, list[GameEvent]],
    timestamp: int,
):
    plot_data: list[tuple[float, float]] = []
    current_grid = [
        ["." for _ in range(len(game.solution[0]))]
        for _ in range(len(game.solution))
    ]

    first_timestamp: Optional[int] = None

    total_blanks = 0
    for row_ind in range(len(game.solution)):
        for col_ind in range(len(game.solution[row_ind])):
            if game.solution[row_ind][col_ind] != ".":
                total_blanks += 1

    for cellChangeEvent in history["updateCell"]:
        if first_timestamp is None:
            first_timestamp = cellChangeEvent.timestamp

        if cellChangeEvent.timestamp > timestamp:
            yield

        assert isinstance(cellChangeEvent, UpdateCellModel)
        r, c = cellChangeEvent.params.cell.r, cellChangeEvent.params.cell.c

        current_grid[r][c] = cellChangeEvent.params.value

        solved_blanks = 0
        for row_ind in range(len(game.solution)):
            for col_ind in range(len(game.solution[row_ind])):
                if game.solution[row_ind][col_ind] == ".":
                    continue
                solved_blanks += (
                    1
                    if game.solution[row_ind][col_ind]
                    == current_grid[row_ind][col_ind]
                    else 0
                )

        plot_data.append(
            (
                cellChangeEvent.timestamp - first_timestamp,
                solved_blanks / total_blanks,
            )
        )

        times, percents = zip(*plot_data)
        axis.plot(times, percents, marker="", linestyle="-", color="green")

    yield
