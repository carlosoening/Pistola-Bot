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
      if (message.author.guild_permissions.administrator):  
        message_split = message.content.split(' ', 2)
        command = message_split[1]
        value = message_split[2]
        if (len(command) == 0 or len(value) == 0):
          await message.channel.send('Invalid command')
          return
        insert_return = db.insert(command, value)
        await message.channel.send(insert_return)
        return
      else:
        await message.channel.send('You do not have permission to use this command')
        return
    if (message.content.startswith('$remove')):
      if (message.author.guild_permissions.administrator):
        message_split = message.content.split(' ')
        command = message_split[1]
        if (len(command) == 0):
          await message.channel.send('Invalid command')
          return
        remove_return = db.remove(command)
        await message.channel.send(remove_return)
        return
        
    await message.channel.send(db.get(message.content))

client.run(config('DISCORD_TOKEN'))