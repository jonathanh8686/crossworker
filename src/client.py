import discord

intents = discord.Intents.default()
intents.message_content = True

def is_dfa_link(link: str) -> bool:
  pass

class CrossworkerClient(discord.Client):
  async def on_ready(self):
    print(f'Logged on as {self.user}!')

  async def on_message(self, message: discord.Message):
    if message.author == self.user:
      return
    
    await message.channel.send(f"Hi, {message.author}")
  