import matplotlib.pyplot as plt
import pandas as pd
from loguru import logger

from ..discord_bot.message_types import GameEvent, GameModel, UpdateCellModel


def get_completion_line(game: GameModel, history: dict[str, list[GameEvent]]):
    df = pd.DataFrame(columns=["timestamp", "completion"])
    current_grid = [
        ["." for _ in range(len(game.solution[0]))]
        for _ in range(len(game.solution))
    ]

    total_blanks = 0
    for row_ind in range(len(game.solution)):
        for col_ind in range(len(game.solution[row_ind])):
            if game.solution[row_ind][col_ind] != ".":
                total_blanks += 1

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

        df = pd.concat(
            [
                df,
                pd.DataFrame(
                    [
                        {
                            "timestamp": cellChangeEvent.timestamp,
                            "completion": solved_blanks / total_blanks,
                        }
                    ]
                ),
            ],
            ignore_index=True,
        )

    plt.plot(df["timestamp"].tolist(), df["completion"].tolist())
    plt.show()
