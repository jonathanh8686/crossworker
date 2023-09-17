import re

import discord
from loguru import logger
from typing import Callable

from .worker import Worker

intents = discord.Intents.default()
intents.message_content = True


def is_dfa_link(link: str) -> bool:
    return (
        re.match(r"https://downforacross.com/beta/game/.+", link) is not None
    )


def get_dfa_code(link: str) -> str:
    return re.sub(r"https://downforacross.com/beta/game/", "", link)


class CrossworkerClient(discord.Client):
    def __init__(self, intents: discord.Intents):
        super().__init__(intents=intents)
        self.active_workers: list[Worker] = []

    def __get_destroy(self, dfa_code: str) -> Callable[[], None]:
        def destroy():
            logger.info(f"Destroying workers attached to game {dfa_code}")
            self.active_workers = list(
                filter(lambda x: x.game_id != dfa_code, self.active_workers)
            )

        return destroy

    async def on_ready(self) -> None:
        logger.success(f"Logged on as {self.user}")

        dfa_code = "3890747-bruss"
        self.active_workers.append(
            Worker(dfa_code, self.__get_destroy(dfa_code))
        )
        await self.active_workers[-1].attach()

    async def on_message(self, message: discord.Message) -> None:
        # ignore messages sent by the bot
        if message.author == self.user:
            return

        if is_dfa_link(message.content):
            dfa_code = get_dfa_code(message.content)
            logger.info(f"Detected DFA link, Parsed code as: {dfa_code}")
            await message.channel.send(f"Joining crossword {dfa_code}!")
            self.active_workers.append(
                Worker(dfa_code, self.__get_destroy(dfa_code))
            )
            await self.active_workers[-1].attach()
