import os

import discord
from .client import CrossworkerClient
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("DISCORD_TOKEN")
if BOT_TOKEN is None:
    raise ValueError("BOT_TOKEN not found")

intents = discord.Intents.default()
intents.message_content = True

client = CrossworkerClient(intents=intents)
client.run(BOT_TOKEN)
