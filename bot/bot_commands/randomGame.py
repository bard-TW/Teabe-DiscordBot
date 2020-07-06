import discord
from discord.ext import commands

from bot.core.classes import Cog_Extension

import random
import asyncio
from discord.ext.commands import has_permissions, MissingPermissions

class RandomGame(Cog_Extension):
    @commands.command()
    async def 骰子(self, ctx):
        await ctx.send("{} 點".format(random.randint(1,6)))

    @commands.command()
    async def 數字(self, ctx):
        await ctx.send("{}".format(random.randint(1,100)))

    @commands.command()
    async def 抽獎(self, ctx ,*arg):
        print(arg)
        if len(arg) > 0:
            await ctx.send("{}".format(random.choice(arg)))
        else:
            await ctx.send('要輸入獎項喔!!')

    @commands.command()
    async def 是否(self, ctx):
        await ctx.send("{}".format(random.choice(['是', '否'])))

    @commands.command()
    async def 可以不可以(self, ctx):
        await ctx.send("{}".format(random.choice(['可以', '不可以'])))

    @commands.command()
    async def 塔(self, ctx, icon=None, num=None):
        high = int(num)
        if high <= 5:
            tar = ''
            for i in range(high):
                tar += "> "
                tar += "    "*(high-i)
                tar += "{}  ".format(icon)*(i+1)
                tar += "\n"
            await ctx.send(tar)
        else:
            await ctx.send('請輸入5以下數字')

    @commands.command()
    async def 進化塔(self, ctx, icon=None, num=None):
        high = int(num)
        if high <= 20:
            for i in range(high):
                tar = ''
                tar += "> "
                tar += "    "*(high-i)
                tar += "{}  ".format(icon)*(i+1)
                tar += "\n"
                await asyncio.sleep(0.5)
                await ctx.send(tar)
        else:
            await ctx.send('請輸入20以下數字')

def setup(bot):
    bot.add_cog(RandomGame(bot))







