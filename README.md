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
* [tinydb](https://tinydb.readthedocs.io/en/latest/) - A document oriented database to store data in JSON file
* [youtube_dl](https://youtube-dl.org/) - An open source download manager library for Youtube video and audio

## Setup

You will need to install some python modules to be able to run the project. Run the following commands to install them:

* pip install discord
* pip install -U discord.py[voice]
* pip install python-decouple
* pip install youtube_dl
* pip install psycopg2

If you want to use the playing music feature, you will need to [install the FFMPEG software on your machine](https://phoenixnap.com/kb/ffmpeg-windows). 
