import discord
from utils import checkKey
from decouple import config
import db

client = discord.Client()
db.init()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if message.content.startswith('$'):
    print(message.content)

    if (message.content.startswith('$add')):
      message_split = message.content.split(' ')
      command = message_split[1]
      value = message_split[2]
      print(message_split)
      insert_return = db.insert(command, value)
      await message.channel.send(insert_return)
      return
    
    await message.channel.send(db.get(message.content))

client.run(config('DISCORD_TOKEN'))