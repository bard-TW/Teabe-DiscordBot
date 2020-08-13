import discord
from discord.ext import commands
from bot.core.classes import Cog_Extension
import asyncio
from datetime import datetime

from bot.core.cache import CACHE_REACTION

class CleanCache(Cog_Extension):
    '''刪除快取'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        async def cleanCache():
            await self.bot.wait_until_ready()
            while not self.bot.is_closed():
                await asyncio.sleep(300)
                now = datetime.now()
                for msg_id in list(CACHE_REACTION):
                    rea = CACHE_REACTION[msg_id]
                    if (now - rea.time).seconds > 600:
                        del(CACHE_REACTION[msg_id])
                        print(msg_id, rea.buttonActionDict.keys())
                        for react in rea.buttonActionDict.keys():
                            await rea.msg.remove_reaction(react, self.bot.user)
                    del rea
        self.bg_task = self.bot.loop.create_task(cleanCache())


def setup(bot):
    bot.add_cog(CleanCache(bot))