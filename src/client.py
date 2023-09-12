import discord
import re
import ws_listener as ws

intents = discord.Intents.default()
intents.message_content = True

def is_dfa_link(link: str) -> bool:
  return re.match(r'https://downforacross.com/beta/game/.+', link)

def get_dfa_code(link: str) -> bool:
  return re.sub(r'https://downforacross.com/beta/game/', '', link)

class CrossworkerClient(discord.Client):
  async def on_ready(self):
    print(f'Logged on as {self.user}!')

  async def on_message(self, message: discord.Message):
    if message.author == self.user:
      return
    
    if is_dfa_link(message.content):
      dfa_code = get_dfa_code(message.content)
      print(f'Joining game {dfa_code}')
      await message.channel.send(f'Joining crossword {dfa_code}!')
      client = ws.WebsocketClient()
      client.join_game(dfa_code)
      client.listen_game(dfa_code)

    
    # await message.channel.send(f"Hi, {message.author}")

  
    
  