
import discord
from discord.ext import commands

from bot.core.classes import Cog_Extension
from django.conf import settings
from django.db.models import Max
from discord.errors import Forbidden

from bot.models import Info_guild, Info_guildConfig, JoinAndLeaveGuild, BotReactionRoles, Info_roles
from bot.core.cache import CACHE_REACTION_ROLE

from discord.ext.commands import has_permissions, MissingPermissions, CommandInvokeError

# log
import logging
import time

import asyncio
import traceback
logger = logging.getLogger('bot')


class Event(Cog_Extension):
    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_id = Info_guild.objects.get(guild_id=member.guild.id)
        guildConfig = Info_guildConfig.objects.get(guild_id=guild_id)
        joinAndLeave = JoinAndLeaveGuild.objects.get(guild_id=guild_id)
        if guildConfig.join_msg_is_valid:
            channel = self.bot.get_channel(guildConfig.join_guild_msg_channel)
            if channel:
                embed=discord.Embed(
                    title=joinAndLeave.joinGuildTitle,
                    description=joinAndLeave.joinGuildDscription,
                    color=0x0000FF)
                embed.set_thumbnail(url="{}".format(member.avatar_url_as()))
                embed.add_field(name="帳號", value="{}".format(member.mention), inline=True)
                embed.add_field(name="時間", value="{}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), inline=False)
                await channel.send(embed=embed)
            else:
                guildConfig.join_msg_is_valid = False
                guildConfig.save()

        if guildConfig.join_guild_cipher_is_valid:
            msgs = [joinAndLeave.joinGuildCipher1, joinAndLeave.joinGuildCipher2, joinAndLeave.joinGuildCipher3, joinAndLeave.joinGuildCipher4, joinAndLeave.joinGuildCipher5]
            for msg in msgs:
                if msg:
                    await member.send(msg)
                await asyncio.sleep(2)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild_id = Info_guild.objects.get(guild_id=member.guild.id)
        guildConfig = Info_guildConfig.objects.get(guild_id=guild_id)
        joinAndLeave = JoinAndLeaveGuild.objects.get(guild_id=guild_id)
        if guildConfig.leave_msg_is_valid:
            channel = self.bot.get_channel(guildConfig.leave_guild_msg_channel)
            if channel:
                embed=discord.Embed(
                    title=joinAndLeave.leaveGuildTitle,
                    description=joinAndLeave.leaveGuildDescription,
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
        guild_data = Info_guild.objects.filter(guild_id=guild.id)
        guild_data.delete()
        logger.info("{}, {}, {}".format('remove', guild, type(guild)))

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('登入bot: %s, id: %s, 加入伺服器數量: %s', self.bot.user.name, self.bot.user.id, len(self.bot.guilds))
        
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{settings.PREFIX}help"))
        for guild in self.bot.guilds:
            await self.checkCreateData(guild)

        # CACHE_REACTION_ROLE 快取
        qs = (
            BotReactionRoles.objects
            .values('msg_id')
            .annotate(max_id=Max('msg_id'))
        )
        if qs:
            CACHE_REACTION_ROLE.extend(qs.values_list('msg_id', flat=True))
            logger.info('反應快取數量: {}'.format(len(CACHE_REACTION_ROLE)))

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

        joinAndLeave = JoinAndLeaveGuild.objects.filter(guild_id=guild_data[0])
        if not joinAndLeave:
            JoinAndLeaveGuild.objects.create(guild_id=guild_data[0])

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id in CACHE_REACTION_ROLE:
            # 加入表情反應
            guild_id = Info_guild.objects.get(guild_id=payload.guild_id)
            if payload.emoji.id:
                reaction = BotReactionRoles.objects.filter(guild_id=guild_id, msg_id=payload.message_id, emoji_id=payload.emoji.id)
            else:
                reaction = BotReactionRoles.objects.filter(guild_id=guild_id, msg_id=payload.message_id, emoji_name=payload.emoji.name)
            if reaction:
                guild = self.bot.get_guild(payload.guild_id)
                member = guild.get_member(payload.user_id)
                for rea in reaction:
                    role = discord.utils.get(guild.roles, id=rea.roles_id.roles_id)
                    if role:
                        await member.add_roles(role)
                    else:
                        roles = Info_roles.objects.filter(guild_id=guild_id, roles_id=rea.roles_id.roles_id)
                        roles.delete()

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        # 解除表情反應
        if payload.message_id in CACHE_REACTION_ROLE:
            guild_id = Info_guild.objects.get(guild_id=payload.guild_id)
            if payload.emoji.id:
                reaction = BotReactionRoles.objects.filter(guild_id=guild_id, msg_id=payload.message_id, emoji_id=payload.emoji.id)
            else:
                reaction = BotReactionRoles.objects.filter(guild_id=guild_id, msg_id=payload.message_id, emoji_name=payload.emoji.name)

            if reaction:
                guild = self.bot.get_guild(payload.guild_id)
                member = guild.get_member(payload.user_id)
                for rea in reaction:
                    role = discord.utils.get(guild.roles, id=rea.roles_id.roles_id)
                    if role:
                        await member.remove_roles(role)
                    else:
                        roles = Info_roles.objects.filter(guild_id=guild_id, roles_id=rea.roles_id.roles_id)
                        roles.delete()


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            if ctx.guild:
                msg = '您缺少以下權限：\n```'
                for missing_perm in error.missing_perms:
                    if missing_perm == 'manage_messages':
                        msg += '管理訊息\n'
                    elif missing_perm == 'manage_roles':
                        msg += '管理身分組\n'
                    else:
                        msg += f'{missing_perm}\n'
                msg += '```'
                await ctx.send(msg)
            else:
                await ctx.send('私人頻道無法使用此功能')
            await ctx.message.add_reaction(settings.REACTION_FAILURE)

        # if isinstance(error, CommandInvokeError):
        #     await ctx.send(f'{settings.BOT_NAME}缺少權限qaq')
        #     await ctx.message.add_reaction(settings.REACTION_FAILURE)

        else:
            print(error, traceback.format_exc())
        


def setup(bot):
    bot.add_cog(Event(bot))





