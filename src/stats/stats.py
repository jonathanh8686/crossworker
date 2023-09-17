import matplotlib.pyplot as plt
from celluloid import Camera  # type: ignore
from loguru import logger

from src.stats.completion_line import get_completion_line
from src.stats.correct_map import get_correct_map

from ..discord_bot.message_types import GameEvent, GameModel


class Statistics:
    def __init__(self, game: GameModel, history: dict[str, list[GameEvent]]):
        self.game = game
        self.history = history

    def get_visualization(self):
        logger.info(
            f"Starting visualization generation on {self.game.info.title}"
        )
        fig, ((ax1, ax2)) = plt.subplots(2, 1, figsize=(10, 8))
        # fig.patch.set_visible(False)
        camera = Camera(fig)
        cnt = 0
        for update in self.history["updateCell"]:
            next(
                get_completion_line(
                    ax1, self.game, self.history, update.timestamp
                )
            )

            next(
                get_correct_map(ax2, self.game, self.history, update.timestamp)
            )
            camera.snap()
            cnt += 1
            logger.debug(f"Snapped for update {cnt} out of {len(self.history['updateCell'])}")

        animation = camera.animate()
        logger.debug(f"Exporting to test.mp4")
        animation.save("test.mp4")
        logger.info(f"Exported visualization to test.mp4")
