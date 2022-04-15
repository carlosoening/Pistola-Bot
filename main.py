import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.utils import get
from decouple import config
import db
import youtube_dl
from reserved_commands import reserved_commands
db.init()

client = commands.Bot(command_prefix='$')

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
   
# Handles PLAY an audio in a voice channel command
@client.command(pass_context = True)
async def play(ctx, video_url:str):
  if (ctx.author.voice == None):
    await ctx.channel.send("Tu não tá num canal de voz seu animal")
    return
  channel = ctx.message.author.voice.channel
  voice = get(client.voice_clients, guild=ctx.guild)
  if (voice == None):
    voice = await channel.connect()

  YDL_OPTS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
  }

  FFMPEG_OPTS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
  }

  if not voice.is_playing():
    with youtube_dl.YoutubeDL(YDL_OPTS) as ydl:
      info = ydl.extract_info(video_url, download=False)
    URL = info['formats'][0]['url']
    voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTS))
    voice.is_playing()
  else:
    await ctx.send("Already playing song")
    return

# Handles STOP audio bot command
@client.command(pass_context = True)
async def stop(ctx):
  voice = get(client.voice_clients, guild=ctx.guild)
  if (voice != None):
    voice.stop()
    return

# Handles LEAVE audio bot command
@client.command(pass_context = True)
async def leave(ctx):
  voice = get(client.voice_clients, guild=ctx.guild)
  if (voice != None):
    await voice.disconnect()
    return

# Handles ADD command
@client.command(pass_context = True)
async def add(ctx):
  if (ctx.message.author.guild_permissions.administrator):  
    message_split = ctx.message.content.split(' ', 2)
    command = message_split[1]
    value = message_split[2]
    if (len(command) == 0 or len(value) == 0):
      await ctx.send('Invalid command')
      return
    insert_return = db.insert(ctx.message.guild.id, command, value)
    await ctx.send(insert_return)
    return
  else:
    await ctx.send('You do not have permission to use this command')
    return

# Handles REMOVE command
@client.command(pass_context = True)
async def remove(ctx):
  if (ctx.message.author.guild_permissions.administrator):
    message_split = ctx.message.content.split(' ')
    command = message_split[1]
    if (len(command) == 0):
      await ctx.send('Invalid command')
      return
    remove_return = db.remove(ctx.message.guild.id, command)
    await ctx.send(remove_return)
    return

@client.event
async def on_message(message):
  if (message.author == client.user):
    return
  
  if (message.content.startswith('$')):

    if (message.content.startswith(reserved_commands)):
      await client.process_commands(message)
      return

    print(message.content)

    result = db.get(message.guild.id, message.content)
    if (result == None): return
    await message.channel.send(result)

client.run(config('DISCORD_TOKEN'))