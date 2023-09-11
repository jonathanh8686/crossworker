import discord
import re
from socker_handler import WebsocketClient
from loguru import logger

intents = discord.Intents.default()
intents.message_content = True

def is_dfa_link(link: str) -> bool:
  return re.match(r'https://downforacross.com/beta/game/.+', link) is not None

def get_dfa_code(link: str) -> str:
  return re.sub(r'https://downforacross.com/beta/game/', '', link)

class CrossworkerClient(discord.Client):
  async def on_ready(self):
    logger.success("Logged on as {self.user}")

  async def on_message(self, message: discord.Message):
    # ignore messages sent by the bot
    if message.author == self.user:
      return
    
    if is_dfa_link(message.content):
      dfa_code = get_dfa_code(message.content)
      logger.info(f"Detected DFA link, Parsed code as: {dfa_code}")
      await message.channel.send(f'Joining crossword {dfa_code}!')
      await WebsocketClient().join_game(dfa_code)