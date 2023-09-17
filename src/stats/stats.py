from ..discord_bot.message_types import GameEvent, GameModel
from ..stats.completion_line import get_completion_line


class Statistics:
    def __init__(self, game: GameModel, history: dict[str, list[GameEvent]]):
        self.game = game
        self.history = history

    def get_visualization(self):
        get_completion_line(self.game, self.history)
