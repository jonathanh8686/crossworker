import discord
import re

from loguru import logger

intents = discord.Intents.default()
intents.message_content = True

def is_dfa_link(link: str) -> bool:
  return re.match(r'https://downforacross.com/beta/game/.+', link) is not None

class CrossworkerClient(discord.Client):
  async def on_ready(self):
    logger.success(f"Connected to server as {self.user}")

  async def on_message(self, message: discord.Message):
    if message.author == self.user:
      # ignore messages sent by the bot
      return
    
    if is_dfa_link(message.content):
      return
  
    
  