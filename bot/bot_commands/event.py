
import discord
from discord.ext import commands

from bot.core.classes import Cog_Extension
from django.conf import settings

from bot.models import Info_guild, Info_guildConfig, JoinGuildCipher

# log
import logging
import time

import asyncio

logger = logging.getLogger('bot')


class Event(Cog_Extension):
    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_id = Info_guild.objects.get(guild_id=member.guild.id)
        guildConfig = Info_guildConfig.objects.get(guild_id=guild_id)
        if guildConfig.join_msg_is_valid:
            channel = self.bot.get_channel(guildConfig.join_guild_msg_channel)
            if channel:
                embed=discord.Embed(
                    title='歡迎加入伺服器～',
                    description='請先到報到區報到喔！',
                    color=0x0000FF)
                embed.set_thumbnail(url="{}".format(member.avatar_url_as()))
                embed.add_field(name="帳號", value="{}".format(member.mention), inline=True)
                embed.add_field(name="時間", value="{}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), inline=False)
                await channel.send(embed=embed)
            else:
                guildConfig.join_msg_is_valid = False
                guildConfig.save()

        if guildConfig.join_guild_cipher_is_valid:
            cipher = JoinGuildCipher.objects.get(guild_id=guild_id)
            msgs = [cipher.msg1, cipher.msg2, cipher.msg3, cipher.msg4, cipher.msg5]
            for msg in msgs:
                if msg:
                    await member.send(msg)
                await asyncio.sleep(2)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild_id = Info_guild.objects.get(guild_id=member.guild.id)
        guildConfig = Info_guildConfig.objects.get(guild_id=guild_id)
        if guildConfig.leave_msg_is_valid:
            channel = self.bot.get_channel(guildConfig.leave_guild_msg_channel)
            if channel:
                embed=discord.Embed(
                    title='我們懷念他QAQ',
                    color=0xff0000)
                embed.set_thumbnail(url="{}".format(member.avatar_url_as()))
                embed.add_field(name="帳號", value="{}".format(member.mention), inline=True)
                embed.add_field(name="暱稱", value="{}".format(member.display_name), inline=True)
                embed.add_field(name="時間", value="{}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), inline=False)
                await channel.send(embed=embed)
            else:
                guildConfig.leave_msg_is_valid = False
                guildConfig.save()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        # bot 進群
        logger.info("{}, {}, {}".format('join', guild, type(guild)))
        await self.checkCreateData(guild)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        # bot 離群
        # TODO 移除所有guild有關的data
        logger.info("{}, {}, {}".format('remove', guild, type(guild)))

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Logged in as %s, id: %s, guild num: %s', self.bot.user.name, self.bot.user.id, len(self.bot.guilds))
        
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{settings.PREFIX}help (測試版不定時刪資料庫)"))
        for guild in self.bot.guilds:
            await self.checkCreateData(guild)

    async def checkCreateData(self, guild):
        guild_data = Info_guild.objects.filter(guild_id=guild.id)
        if guild_data:
            guild = guild_data.values()[0]['guild']
            if guild != str(guild):
                logger.info(f'update guild name: {guild} > {str(guild)}')
                guild_data.update(guild=str(guild))
        else:
            Info_guild.objects.create(guild=str(guild), guild_id=guild.id)
            guild_data = Info_guild.objects.filter(guild_id=guild.id)

        guildConfig = Info_guildConfig.objects.filter(guild_id=guild_data[0])
        if not guildConfig:
            Info_guildConfig.objects.create(guild_id=guild_data[0])

        joinGuildCipher = JoinGuildCipher.objects.filter(guild_id=guild_data[0])
        if not joinGuildCipher:
            JoinGuildCipher.objects.create(guild_id=guild_data[0])



def setup(bot):
    bot.add_cog(Event(bot))





