import matplotlib.pyplot as plt

from ..discord_bot.message_types import GameEvent, GameModel
from ..stats.completion_line import get_completion_line


class Statistics:
    def __init__(self, game: GameModel, history: dict[str, list[GameEvent]]):
        self.game = game
        self.history = history

    def get_visualization(self):
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

        get_completion_line(
            ax1,
            self.game,
            self.history,
            self.history["updateCell"][-1].timestamp,
        )

        fig.show()

        input()
