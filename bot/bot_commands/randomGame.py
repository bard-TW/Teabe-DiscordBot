import discord
from discord.ext import commands

from bot.core.classes import Cog_Extension

import random
import asyncio
from discord.ext.commands import has_permissions, MissingPermissions

class RandomGame(Cog_Extension):
    @commands.command(name='dice', aliases=['骰子'])
    async def dice(self, ctx):
        await ctx.send("{} 點".format(random.randint(1,6)))

    @commands.command(name='number', aliases=['數字'])
    async def number(self, ctx):
        await ctx.send("{}".format(random.randint(1,100)))

    @commands.command(name='luckyDraw', aliases=['抽獎', 'ld'])
    async def luckyDraw(self, ctx ,*arg):
        if len(arg) > 0:
            await ctx.send("{}".format(random.choice(arg)))
        else:
            await ctx.send('要輸入獎項喔!!')

    @commands.command(name='whether', aliases=['是否'])
    async def whether(self, ctx):
        await ctx.send("{}".format(random.choice(['是', '否'])))

    @commands.command(name='canyou', aliases=['可不可以'])
    async def canyou(self, ctx):
        await ctx.send("{}".format(random.choice(['可以', '不可以'])))

    @commands.command(name='tower', aliases=['塔'])
    async def tower(self, ctx, icon=None, num=None):
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

    @commands.command(name='evolutiontower', aliases=['進化塔', 'et'])
    async def evolutiontower(self, ctx, icon=None, num=None):
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







