import discord
from commands import commands
from utils import checkKey
from decouple import config

client = discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if message.content.startswith('$'):
    if checkKey(commands, message.content):
      print(message.content)
      await message.channel.send(commands[message.content])

client.run(config('DISCORD_TOKEN'))
