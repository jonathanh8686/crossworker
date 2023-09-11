import os
import discord

from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv('DISCORD_TOKEN')
if BOT_TOKEN is None:
  raise ValueError("BOT_TOKEN not found")

class CrossworkerClient(discord.Client):
  async def on_ready(self):
      print(f'Logged on as {self.user}!')

  async def on_message(self, message):
      print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default()
intents.message_content = True

client = CrossworkerClient(intents=intents)
client.run(BOT_TOKEN)

