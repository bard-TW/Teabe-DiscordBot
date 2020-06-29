# -*- coding: utf-8 -*-
"""
Main entry point for the bot.
This module performs the start-up, login and reads out the settings to configure
the bot.
"""
# os
import os
from datetime import datetime

# log
import logging

# django
import django
from django.conf import settings

# discord
import discord
from discord.ext import commands

# thread
import threading
from subprocess import Popen, PIPE

# 紀錄log
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teabe.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
logger = logging.getLogger('bot')
django.setup()

# 啟動django
p = Popen(['python', 'manage.py', 'runserver'])
logger.info(f'Starting up django, pid: {p.pid}')

logger.info('Starting up bot')
bot = commands.Bot(command_prefix=settings.PREFIX)
bot.remove_command('help')
@bot.event
async def on_ready():
    logger.info('Logged in as %s, id: %s', bot.user.name, bot.user.id)
    await bot.change_presence(activity=discord.Game(name=f"{settings.PREFIX}help"))

@bot.command()
async def load(ctx, extension):
    if ctx.author.id == settings.HOLDER_ID:
        bot.load_extension('bot.bot_commands.{}'.format(extension))
        await ctx.message.add_reaction(settings.REACTION_SUCCESS)

@bot.command()
async def unload(ctx, extension):
    if ctx.author.id == settings.HOLDER_ID:
        bot.unload_extension('bot.bot_commands.{}'.format(extension))
        await ctx.message.add_reaction(settings.REACTION_SUCCESS)

@bot.command()
async def reload(ctx, extension):
    if ctx.author.id == settings.HOLDER_ID:
        bot.reload_extension('bot.bot_commands.{}'.format(extension))
        await ctx.message.add_reaction(settings.REACTION_SUCCESS)

for filename in os.listdir('./bot/bot_commands'):
    if filename.endswith('.py'):
        bot.load_extension('bot.bot_commands.{}'.format(filename[:-3]))

if __name__ == '__main__':
    bot.run(settings.TOKEN)

