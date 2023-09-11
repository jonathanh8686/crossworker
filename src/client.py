import discord
import re
from socker_handler import WebsocketClient
import asyncio

from loguru import logger

intents = discord.Intents.default()
intents.message_content = True

def is_dfa_link(link: str) -> bool:
  return re.match(r'https://downforacross.com/beta/game/.+', link) is not None

def get_dfa_code(link: str) -> str:
  return re.sub(r'https://downforacross.com/beta/game/', '', link)

class CrossworkerClient(discord.Client):
  async def on_ready(self):
    print(f'Logged on as {self.user}!')

    dfa_code = "3853980-bruss"
    print(f'Joining game {dfa_code}')
    await WebsocketClient().join_game(dfa_code)

  async def on_message(self, message: discord.Message):
    if message.author == self.user:
      # ignore messages sent by the bot
      return
    
    if is_dfa_link(message.content) or True:
      # dfa_code = get_dfa_code(message.content)
      dfa_code = "3853980-bruss"
      print(f'Joining game {dfa_code}')
      await message.channel.send(f'Joining crossword {dfa_code}!')
      await WebsocketClient().join_game(dfa_code)

      # client = ws.WebsocketClient()
      # client.join_game(dfa_code)
      # client.listen_game(dfa_code)

    # await message.channel.send(f"Hi, {message.author}")

  
    
  