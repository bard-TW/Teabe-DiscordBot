# discord
import discord
from discord.ext import commands
from discord.errors import Forbidden
from discord.ext.commands import has_permissions, MissingPermissions

from bot.core.classes import Cog_Extension
from django.conf import settings

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
    @has_permissions(manage_roles=True)
    async def clean(self, ctx, num: int):
        try:
            if num<=200:
                await ctx.channel.purge(limit=num+1)
            else:
                await ctx.send('請小於200條')
        except Forbidden:
            await ctx.send(f'{settings.BOT_NAME}沒有權限刪除 QAQ')

    @clean.error
    async def clean_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send('您缺少權限！')



    @commands.command()
    async def change_presence(self, ctx, status=0, *, msg=None):
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