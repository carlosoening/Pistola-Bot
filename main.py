import sys
from discord import FFmpegPCMAudio, Intents, File
from discord.ext import commands
from discord.utils import get
from decouple import config
import db
import youtube_dl
from reserved_commands import RESERVED_COMMANDS
import controller.sheetsAccess as sheetsAccess
import controller.confluenceAccess as confluenceAccess
import os
from json import JSONDecodeError

intents = Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='$', intents=intents)

pages_ids = {}

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
   
@client.command(pass_context = True)
async def play(ctx, video_url: str):
  """
  Handles PLAY an audio in a voice channel command
  """
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

@client.command(pass_context = True)
async def stop(ctx):
  """
  Handles STOP audio bot command
  """
  print(ctx)
  voice = get(client.voice_clients, guild=ctx.guild)
  if (voice != None):
    voice.stop()
  return

@client.command(pass_context = True)
async def leave(ctx):
  """
  Handles LEAVE audio bot command  
  """
  voice = get(client.voice_clients, guild=ctx.guild)
  if (voice != None):
    await voice.disconnect()
  return

@client.command(pass_context = True)
async def add(ctx):
  """
  Handles ADD command
  """
  if (ctx.message.author.guild_permissions.administrator):  
    message_split = ctx.message.content.split(' ', 2)
    command = message_split[1]
    value = message_split[2]
    if (len(command) == 0 or len(value) == 0):
      await ctx.send('Invalid command')
      return
    insert_return = db.insert(ctx.message.guild.id, command, value)
    await ctx.send(insert_return)
  else:
    await ctx.send('You do not have permission to use this command')
  return

@client.command(pass_context = True)
async def remove(ctx):
  """
  Handles REMOVE command
  """
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
  """
  Handles users custom commands
  """
  if (message.author == client.user):
    return
  if (message.content.startswith('$')):
    if (message.content.startswith(RESERVED_COMMANDS)):
      await client.process_commands(message)
      return
    print(message.content)
    result = db.get(message.guild.id, message.content)
    if (result == None): return
    await message.channel.send(result)

@client.command(pass_context = True)
async def sheet(ctx):
  """
  Handles connect to Google sheets
  """
  sheetsAccess.infoSheets(config('SPREADSHEET_ID'))
  return

@client.command(pass_context = True)
async def confluence(ctx):
  """
  This function searches by a keyword or sentence in the Confluence database and list the matching pages
  """
  global pages_ids
  pages_ids = {}
  message_split = ctx.message.content.split(' ')
  keyword = message_split[1]
  confluence = confluenceAccess.getConfluenceConnection()
  pages = confluence.cql('text ~ "' + keyword + '" and type = "page"')
  titles = ''
  index = 1
  for result in pages['results']:
    titles += F'{index}' + ' - ' + result['content']['title'] + '\n'
    pages_ids.update({F'{index}': result['content']['id']})
    index = index + 1
  print(pages_ids)
  await ctx.send(titles)
  return

@client.command(pass_context = True)
async def dc(ctx):
  """
  This function downloads a PDF from the Confluence database its ID
  """
  message_split = ctx.message.content.split(' ')
  index = message_split[1]
  global pages_ids
  if (index.isnumeric() == False):
    await ctx.send('O índice informado não é válido!')
    return
  id = pages_ids.get(index)
  if (id == None):
    await ctx.send('O índice informado não foi encontrado!')
    return
  await ctx.send('O arquivo está sendo preparado, por favor aguarde...')
  confluence = confluenceAccess.getConfluenceConnection()
  page = confluence.get_page_by_id(id)
  content = confluence.export_page(id)
  file_name = page['title'] + '.pdf'
  file_pdf = open(file_name, 'wb')
  file_pdf.write(content)
  file_pdf.close()
  async for message in ctx.channel.history(limit=2):
    if message.author == client.user:
      await message.delete()
      break
  await ctx.send(file=File(file_name))
  os.remove(file_name)
  pages_ids = {}
  return


def main():
  if (len(sys.argv) > 0):
    if ('nodb' not in sys.argv):
      db.init()
    client.run(config('DISCORD_TOKEN'))

if (__name__ == '__main__'):
  main()