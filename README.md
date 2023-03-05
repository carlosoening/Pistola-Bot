# Pistola Bot

## Introduction

This is a bot for Discord made with Python.\
I made this bot for practicing my python programming skills.\
You can use it to respond to simple commands and you can add commands to the bot as well, using the command `$add <command> <value>`
if you are an administrator of the Discord server.\
You can also use it to play an audio from a youtube video in a voice channel using the command `$play <video_url>`.

## Modules

The following modules were used in this project:

* [discord](https://pypi.org/project/discord.py/) - A Python Discord API that facilitates the integration with Discord
* [psycopg2](https://www.psycopg.org/docs/) - A PostgreSQL database adapter library for Python
* [youtube_dl](https://youtube-dl.org/) - An open source download manager library for Youtube video and audio

## Setup

Install Python 3.x if you haven't done that yet;

You will need to install some python modules to be able to run the project. Run the following commands to install them:

* pip install discord
* pip install -U discord.py[voice]
* pip install python-decouple
* pip install youtube_dl
* pip install psycopg2

-- For Google API
* pip install gspread
* pip install oauth2client

If you want to use the playing music feature, you will need to [install the FFMPEG software on your machine](https://phoenixnap.com/kb/ffmpeg-windows). 

### Configuration file

You will need to create a `.env` file on the root of the project folder with the following content:

```
DISCORD_TOKEN=<discord_token>
DB_HOST=<host>
DB_PORT=<port>
DB_NAME=<database_name>
DB_USER=<username>
DB_PASSWORD=<password>
```

### Configuration Google API

You will need create a service account in Google Clound Plataform and download de JSON file with the credentials and add in project. Be sure the file name is "credentials.json".

Finally, to run the project you just need to run the following command: `python main.py`
