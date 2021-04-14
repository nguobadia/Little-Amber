#!/usr/bin/python

import discord
import datetime
import json
import re

from discord.ext import commands
from discord.ext.commands import Bot

CHANNEL_NAMES = ["philosophy", "religion", "psychology", "sociology", "economics", "us-politics",
                 "global-politics", "history", "science", "lgbt", "rhetoric", "art-analysis", "miscellaneous", "bot-testing"]

CHANNEL_LIBRARY = [826749300993425419,
                   827467898804502538,
                   828164039874969610,
                   828164009365733406,
                   826749319079002153,
                   828110549489025094,
                   826749445701369886,
                   826751598671167498,
                   826877724449701958,
                   827328040702836736,
                   826749736400584766,
                   826749577344057414,
                   830770149657280532,
                   831716059555692584]

CHANNEL_LINKS = [830772056702058547,
                 830772486903300116,
                 830772094031626268,
                 830772121047007243,
                 830772160401899560,
                 830772337741398067,
                 830772370842058752,
                 830772403059032104,
                 830772431953854465,
                 830772459506106369,
                 830772586701914143,
                 830772625105485874,
                 831728489152512040,
                 831715977020309514]

CHANNEL_MAPPING = dict(zip(CHANNEL_LIBRARY, CHANNEL_LINKS))

LINK_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

with open("config/config.json", "r") as j:
    bot_info = json.load(j)
    
PREFIX = bot_info["prefix"]
TOKEN = bot_info["token"]
CLIENT = commands.Bot(command_prefix = PREFIX)
START_TIME = datetime.datetime.utcnow()


@CLIENT.event
async def on_message(message):
    if message.channel.id in CHANNEL_LIBRARY:
        link_id = CHANNEL_MAPPING[message.channel.id]
        links = re.findall(LINK_REGEX, message.content) 
        
        # if the message contains a link
        if len(links) > 0:
            channel = CLIENT.get_channel(link_id)
            await channel.send(message.content)
            await CLIENT.process_commands(message)
            
        # print(links)
        # if message.attachments.content_type:




















@CLIENT.event
async def on_ready():
    print('Logged in as')
    print(CLIENT.user.name)
    print('------')
    await CLIENT.change_presence(activity=discord.Game(name='Studying...', type=1))


@CLIENT.command(name='uptime',
                description='Returns how long the bot has been running for.')
async def uptime(ctx):
    '''
    Source: https://stackoverflow.com/questions/52155265/my-uptime-function-isnt-able-to-go-beyond-24-hours-on-heroku
    '''
    now = datetime.datetime.utcnow() # Timestamp of when uptime function is run
    delta = now - START_TIME
    
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    
    if days:
        time_format = "**{d}** days, **{h}** hours, **{m}** minutes, and **{s}** seconds."
        
    else:
        time_format = "**{h}** hours, **{m}** minutes, and **{s}** seconds."
        
    uptime_stamp = time_format.format(d=days, h=hours, m=minutes, s=seconds)
    await ctx.send('{} has been up for {}'.format(CLIENT.user.name, uptime_stamp))
    
CLIENT.run(TOKEN)