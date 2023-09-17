import matplotlib
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

from src.stats.correct_map import get_correct_map

from ..discord_bot.message_types import GameEvent, GameModel, GameModel


class Statistics:
    def __init__(self, game: GameModel, history: dict[str, list[GameEvent]]):
        self.game = game
        self.history = history

    def get_visualization(self):
        
        for update in self.history['updateCell']:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
            next(get_correct_map(
                ax2,
                self.game,
                self.history,
                update.timestamp
            ))

            fig.show()
            input()