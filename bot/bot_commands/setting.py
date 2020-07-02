import discord
from discord.ext import commands

from bot.models import Info_guild, Info_guildConfig, JoinGuildCipher, BotReactionRoles

from bot.core.classes import Cog_Extension
from bot.core.cache import CACHE_REACTION_ROLE

from django.conf import settings

import re

from discord.ext.commands import has_permissions

import asyncio

import traceback
# log
import logging

logger = logging.getLogger('bot')


class Setting(Cog_Extension):
    @commands.group()
    @has_permissions(manage_roles=True)
    async def setting(self, ctx):
        if ctx.guild:
            guild_id = Info_guild.objects.get(guild_id=ctx.guild.id)
            ctx.guildConfig = Info_guildConfig.objects.get(guild_id=guild_id)
        else:
            await ctx.send('私人頻道無法使用此功能')

    @setting.command()
    async def look(self, ctx):
        if ctx.guild:
            data = f"{settings.BOT_NAME}伺服器設定查看\n```diff\n"
            data += f"+ 使用介紹\n"
            data += f"下方功能狀態 0:關閉 1:開啟 下指令可控制開關\n"
            data += f"開關推齊範例: {settings.PREFIX}setting previou_is_valid\n"
            data += f"設置進群(離群)通知頻道在要設置的頻道內相同的方式輸入，即可設置\n\n"

            data += f"+ 功能狀態\n"
            data += f"- 以下指令最前面需打 {settings.PREFIX}setting\n"
            data += f"previou_is_valid (推齊功能): {int(ctx.guildConfig.previou_is_valid)}\n"
            data += f"respond_is_valid (回應): {int(ctx.guildConfig.respond_is_valid)}\n"
            data += f"respond_only_guild (只說伺服器內教的): {int(ctx.guildConfig.respond_only_guild)}\n"

            join_guild_msg_channel_name = self.bot.get_channel(ctx.guildConfig.join_guild_msg_channel)
            leave_guild_msg_channel_name = self.bot.get_channel(ctx.guildConfig.leave_guild_msg_channel)
            join_guild_msg_channel_name = join_guild_msg_channel_name if join_guild_msg_channel_name else ''
            leave_guild_msg_channel_name = leave_guild_msg_channel_name if leave_guild_msg_channel_name else ''

            data += f"join_msg_is_valid (開啟進群通知): {int(ctx.guildConfig.join_msg_is_valid)}\n"
            data += f"join_guild_msg_channel (進群的訊息頻道): {join_guild_msg_channel_name}\n"

            data += f"leave_msg_is_valid (開啟離群通知): {int(ctx.guildConfig.join_msg_is_valid)}\n"
            data += f"leave_guild_msg_channel (離群的訊息頻道): {leave_guild_msg_channel_name}\n"

            data += f"join_guild_cipher_is_valid (開啟進群密語): {int(ctx.guildConfig.join_guild_cipher_is_valid)}\n\n"

            data += f"+ 進群密語 (使用者進群後的使用者密語通知訊息)\n"
            data += f"- 以下指令最前面需打 {settings.PREFIX}cipher\n"
            data += f"test (進群密語測試)\n"
            data += f"modify <1~5> <訊息> (進群密語修改 訊息)\n\n"

            data += f"+ 反應權限 (點擊反應後可以獲得權限)\n"
            data += f"- 以下指令最前面需打 {settings.PREFIX}reaction\n"
            data += f"look (查看目前所設定的反應權限)\n"
            data += f"add <訊息ID> <反應> <權限名稱> <反應> <權限名稱> (反應和權限名稱可一次新增多個)\n"
            data += f"remove <訊息ID> (刪除訊息ID裡的全部反應權限))\n"
            data += f"\n```"
            await ctx.send(data)

    @setting.command()
    async def previou_is_valid(self, ctx):
        # 推齊
        if ctx.guild:
            ctx.guildConfig.previou_is_valid = not ctx.guildConfig.previou_is_valid
            ctx.guildConfig.save()
            await ctx.message.add_reaction(settings.REACTION_SUCCESS)

    @setting.command()
    async def respond_is_valid(self, ctx):
        # 回應
        if ctx.guild:
            ctx.guildConfig.respond_is_valid = not ctx.guildConfig.respond_is_valid
            ctx.guildConfig.save()
            await ctx.message.add_reaction(settings.REACTION_SUCCESS)

    @setting.command()
    async def respond_only_guild(self, ctx):
        # 只說伺服器內教的
        if ctx.guild:
            ctx.guildConfig.respond_only_guild = not ctx.guildConfig.respond_only_guild
            ctx.guildConfig.save()
            await ctx.message.add_reaction(settings.REACTION_SUCCESS)

    @setting.command()
    async def join_msg_is_valid(self, ctx):
        # 開啟進群通知
        if ctx.guild:
            ctx.guildConfig.join_msg_is_valid = not ctx.guildConfig.join_msg_is_valid
            ctx.guildConfig.save()
            await ctx.message.add_reaction(settings.REACTION_SUCCESS)

    @setting.command()
    async def leave_msg_is_valid(self, ctx):
        # 開啟離群通知
        if ctx.guild:
            ctx.guildConfig.leave_msg_is_valid = not ctx.guildConfig.leave_msg_is_valid
            ctx.guildConfig.save()
            await ctx.message.add_reaction(settings.REACTION_SUCCESS)

    @setting.command()
    async def join_guild_cipher_is_valid(self, ctx):
        # 開啟進群密語
        if ctx.guild:
            ctx.guildConfig.join_guild_cipher_is_valid = not ctx.guildConfig.join_guild_cipher_is_valid
            ctx.guildConfig.save()
            await ctx.message.add_reaction(settings.REACTION_SUCCESS)

    @setting.command()
    async def join_guild_msg_channel(self, ctx):
        # 進群的訊息頻道
        if ctx.guild:
            ctx.guildConfig.join_guild_msg_channel = ctx.channel.id
            ctx.guildConfig.join_msg_is_valid = True
            ctx.guildConfig.save()
            await ctx.message.add_reaction(settings.REACTION_SUCCESS)
            await ctx.send('此頻道為進群通知頻道')

    @setting.command()
    async def leave_guild_msg_channel(self, ctx):
        # 離群的訊息頻道
        if ctx.guild:
            ctx.guildConfig.leave_guild_msg_channel = ctx.channel.id
            ctx.guildConfig.leave_msg_is_valid = True
            ctx.guildConfig.save()
            await ctx.message.add_reaction(settings.REACTION_SUCCESS)
            await ctx.send('此頻道為離群通知頻道')


class Cipher(Cog_Extension):
    @commands.group()
    @has_permissions(manage_roles=True)
    async def cipher(self, ctx):
        if ctx.guild:
            guild_id = Info_guild.objects.get(guild_id=ctx.guild.id)
            ctx.cipher = JoinGuildCipher.objects.get(guild_id=guild_id)
        else:
            await ctx.send('私人頻道無法使用此功能')

    @cipher.command()
    async def test(self, ctx):
        if ctx.guild:
            msgs = [ctx.cipher.msg1, ctx.cipher.msg2, ctx.cipher.msg3, ctx.cipher.msg4, ctx.cipher.msg5]
            for msg in msgs:
                if msg:
                    await ctx.author.send(msg)
                await asyncio.sleep(2)

    @cipher.command()
    async def modify(self, ctx, num, *, msg):
        if ctx.guild:
            try:
                num = int(num)
                if num == 1:
                    ctx.cipher.msg1 = msg
                elif num == 2:
                    ctx.cipher.msg2 = msg
                elif num == 3:
                    ctx.cipher.msg3 = msg
                elif num == 4:
                    ctx.cipher.msg4 = msg
                elif num == 5:
                    ctx.cipher.msg5 = msg
                else:
                    await ctx.send('請輸入1~5數字')
                    await ctx.message.add_reaction(settings.REACTION_FAILURE)
                    return
                ctx.cipher.save()
                await ctx.message.add_reaction(settings.REACTION_SUCCESS)
            except:
                await ctx.send('請輸入1~5數字')
                await ctx.message.add_reaction(settings.REACTION_FAILURE)

class Reaction(Cog_Extension):
    @commands.group()
    @has_permissions(manage_roles=True)
    async def reaction(self, ctx):
        if ctx.guild:
            ctx.guild_id = Info_guild.objects.get(guild_id=ctx.guild.id)
            ctx.role_dict = {}
            ctx.role_id_dict = {}
            for i, role in enumerate(ctx.guild.roles, start=1):
                ctx.role_dict[role.name] = role.id
                ctx.role_id_dict[role.id] = role.name
                if len(ctx.role_dict.keys()) < i:
                    await ctx.send('身份組名稱重複')
                    return
        else:
            await ctx.send('私人頻道無法使用此功能')

    @reaction.command()
    async def add(self, ctx, msg_id, *arg):
        reaction = BotReactionRoles.objects.filter(guild_id=ctx.guild_id)
        ctx.reaction_num = len(reaction)
        if ctx.reaction_num > 20:
            await ctx.send('一個伺服器中請勿超過20個權限表情')
            await ctx.message.add_reaction(settings.REACTION_FAILURE)
            return
        elif ctx.role_dict == {}:
            return
        pattern = re.compile(r'<:(.*):(\d{16,22})>')
        try:
            if len(arg)%2 == 0 and (15 < len(msg_id) < 22):
                msg_id = int(msg_id)
                emoji_list = arg[::2]  # 表情符號 list
                role_list = arg[1::2]  # 權限名稱 list
                if (ctx.reaction_num + len(emoji_list)) > 20:
                    await ctx.send('一個伺服器中請勿超過20個權限表情')
                    await ctx.message.add_reaction(settings.REACTION_FAILURE)
                    return
                for i in range(len(emoji_list)):
                    role_id = ctx.role_dict.get(role_list[i])
                    if role_id:
                        emoji_id = None
                        emoji_Name = None
                        if len(emoji_list[i]) >5:
                            emoji_match = pattern.match(emoji_list[i])
                            emoji_id = emoji_match[2]
                            emoji_Name = emoji_match[1]
                            reaction = BotReactionRoles.objects.filter(guild_id=ctx.guild_id, msg_id=msg_id, emoji_id=emoji_id, roles_id=role_id)
                        else:
                            emoji_Name = emoji_list[i]
                            reaction = BotReactionRoles.objects.filter(guild_id=ctx.guild_id, msg_id=msg_id, emoji_name=emoji_Name, roles_id=role_id)
                        if not reaction:
                            try:
                                await ctx.message.add_reaction(emoji_list[i])
                            except discord.errors.HTTPException:
                                return
                            BotReactionRoles.objects.create(
                                guild_id= ctx.guild_id, 
                                msg_id= msg_id,
                                emoji_id= emoji_id,
                                emoji_name= emoji_Name,
                                roles_id= role_id,
                                roles_name= role_list[i]
                                )
                if msg_id not in CACHE_REACTION_ROLE:
                    CACHE_REACTION_ROLE.append(msg_id)

            else:
                await ctx.send('訊息ID錯誤')
                await ctx.message.add_reaction(settings.REACTION_FAILURE)
        except ValueError:
            await ctx.send('訊息ID錯誤')
            await ctx.message.add_reaction(settings.REACTION_FAILURE)

    @reaction.command()
    async def remove(self, ctx, msg_id:int):
        if ctx.role_dict == {}:
            return
        reaction = BotReactionRoles.objects.filter(guild_id=ctx.guild_id, msg_id=msg_id)
        reaction.delete()
        await ctx.message.add_reaction(settings.REACTION_SUCCESS)
        if msg_id in CACHE_REACTION_ROLE:
            CACHE_REACTION_ROLE.remove(msg_id)

    @reaction.command()
    async def look(self, ctx):
        if ctx.role_dict == {}:
            return
        reaction_dict = {}
        reaction = BotReactionRoles.objects.filter(guild_id=ctx.guild_id)

        if not reaction:
            await ctx.send('衛定義權限反應')
            return

        for rea in reaction:
            roles_name = ctx.role_id_dict.get(rea.roles_id)
            if not roles_name: #搜不到權限 刪除
                rea.delete()
                continue
            elif roles_name != rea.roles_name: # 權限名有異動
                rea.roles_name = roles_name
                rea.save()

            if rea.msg_id in reaction_dict.keys():
                reaction_dict[rea.msg_id].append({'emoji_id': rea.emoji_id, 'emoji_name': rea.emoji_name, 'roles_name': roles_name})
            else:
                reaction_dict[rea.msg_id] = [{'emoji_id': rea.emoji_id, 'emoji_name': rea.emoji_name, 'roles_name': roles_name}]
        # 處理顯示文字
        msg = ''
        for reaction in reaction_dict.keys():
            msg += f'> 訊息ID：{reaction}\n'
            for rea in reaction_dict[reaction]:
                if rea.get('emoji_id'):
                    emoji = f'<:{rea.get("emoji_name")}:{rea.get("emoji_id")}>'
                else:
                    emoji = rea.get('emoji_name')
                msg += f'反應: {emoji} >> 權限名稱: {rea.get("roles_name")}\n'
            msg += '\n'
        await ctx.send(msg)







def setup(bot):
    bot.add_cog(Setting(bot))
    bot.add_cog(Cipher(bot))
    bot.add_cog(Reaction(bot))