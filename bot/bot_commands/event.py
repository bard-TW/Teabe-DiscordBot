
import discord
from discord.ext import commands

from bot.core.classes import Cog_Extension
from django.conf import settings



class Event(Cog_Extension):
    @commands.Cog.listener()
    async def on_member_join(self, member):
        pass
























def setup(bot):
    bot.add_cog(Event(bot))





