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

    @commands.command()
    async def sayd(self, ctx, *, msg):
        #刪除+複送
        try:
            await ctx.message.delete()
            await ctx.send(msg)
        except Forbidden:
            await ctx.send(f'{settings.BOT_NAME}沒有權限刪除 QAQ')

    @commands.command()
    async def 限時(self, ctx, num: int):
        try:
            if 0 < num <= 1800:
                await ctx.message.add_reaction(settings.REACTION_SUCCESS)
                await asyncio.sleep(num)
                await ctx.message.delete()
        except Forbidden:
            await ctx.send(f'{settings.BOT_NAME}沒有權限刪除 QAQ')

    @commands.command()
    @has_permissions(manage_roles=True)
    async def clean(self, ctx, num: int):
        try:
            if num<=200:
                await ctx.channel.purge(limit=num+1)
            else:
                await ctx.send('請輸入1~200')
        except Forbidden:
            await ctx.send(f'{settings.BOT_NAME}沒有權限刪除 QAQ')

    @commands.command()
    async def change_presence(self, ctx, status=0, *, msg=None):
        # TODO 需在改良
        if ctx.author.id == settings.HOLDER_ID:
            if status:
                if int(status)==1:
                    await self.bot.change_presence(status=discord.Status.offline)
                elif int(status)==2:
                    await self.bot.change_presence(status=discord.Status.idle, activity=discord.Game(name=msg))
                elif int(status)==3:
                    await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name=msg))
                else:
                    await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name=msg))
            else:
                await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name=f"{settings.PREFIX}help"))















def setup(bot):
    bot.add_cog(Base(bot))