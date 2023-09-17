import matplotlib.pyplot as plt
import matplotlib


from ..discord_bot.message_types import GameEvent, GameModel


class Statistics:
    def __init__(self, game: GameModel, history: dict[str, list[GameEvent]]):
        self.game = game
        self.history = history

    def get_visualization(self):
        fig, ax = plt.subplots(1, 1)