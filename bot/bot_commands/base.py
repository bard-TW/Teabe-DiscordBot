# discord
import discord
from discord.ext import commands
from discord.errors import Forbidden
from discord.ext.commands import has_permissions

from bot.core.classes import Cog_Extension
from django.conf import settings

import asyncio

class Base(Cog_Extension):
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('{} ms'.format(round(self.bot.latency*1000)))

    @commands.command(name='sayd', aliases=['偽裝'])
    async def sayd(self, ctx, *, msg):
        #刪除+複送
        try:
            await ctx.message.delete()
            await ctx.send(msg)
        except Forbidden:
            await ctx.send(f'{settings.BOT_NAME}沒有權限刪除 QAQ')

    @commands.command(name='timed', aliases=['限時'])
    async def timed(self, ctx, num: int):
        try:
            if 0 < num <= 1800:
                await ctx.message.add_reaction(settings.REACTION_SUCCESS)
                await asyncio.sleep(num)
                await ctx.message.delete()
        except Forbidden:
            await ctx.send(f'{settings.BOT_NAME}沒有權限刪除 QAQ')

    @commands.command(name='clean', aliases=['刪除'])
    @has_permissions(manage_messages=True)
    async def clean(self, ctx, num: int):
        try:
            if num<=200:
                await ctx.channel.purge(limit=num+1)
            else:
                await ctx.send('請輸入1~200')
        except Forbidden:
            await ctx.send(f'{settings.BOT_NAME}沒有權限刪除 QAQ')

    @commands.command()
    async def change_presence(self, ctx, status_str='', activity_str='', *, msg=None):
        if ctx.author.id == settings.HOLDER_ID:
            status = discord.Status.online
            if status_str == '上線':
                status = discord.Status.online
            elif status_str == '閒置':
                status = discord.Status.idle
            elif status_str == '忙碌':
                status = discord.Status.dnd
            elif status_str == '隱形':
                status = discord.Status.offline

            activity = discord.ActivityType.listening
            if activity_str == '音樂':
                activity = discord.ActivityType.listening
            elif activity_str == '遊戲':
                activity = discord.ActivityType.playing
            elif activity_str == '影片':
                activity = discord.ActivityType.watching

            if not msg:
                msg = f'{settings.PREFIX}help'

            await self.bot.change_presence(status=status, activity=discord.Activity(type=activity, name=msg))


def setup(bot):
    bot.add_cog(Base(bot))