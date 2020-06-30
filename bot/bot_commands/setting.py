import discord
from discord.ext import commands

from bot.core.classes import Cog_Extension
from django.conf import settings

from bot.models import Info_guild, Info_guildConfig, JoinGuildCipher

import asyncio

# log
import logging

logger = logging.getLogger('bot')


class Setting(Cog_Extension):

    @commands.group()
    async def setting(self, ctx):
        if not ctx.guild:
            await ctx.send('私人頻道無法使用此功能')
            return
        ctx.guild_id = Info_guild.objects.get(guild_id=ctx.guild.id)
        ctx.guildConfig = Info_guildConfig.objects.get(guild_id=ctx.guild_id)

    @setting.command()
    async def look(self, ctx):
        if ctx.guild:
            data = f"{settings.BOT_NAME}伺服器設定查看\n```diff\n"
            data += f"+ 使用介紹\n"
            data += f"下方功能狀態 0:關閉 1:開啟 下指令可控制開關\n"
            data += f"開關推齊範例: {settings.PREFIX}setting previou_is_valid\n"
            data += f"設置進群(離群)通知頻道在要設置的頻道內相同的方式輸入，即可設置\n"
            data += f"- 以下指令最前面需打 {settings.PREFIX}setting\n\n"

            data += f"+ 功能狀態\n"
            data += f"previou_is_valid (推齊功能): {int(ctx.guildConfig.previou_is_valid)}\n\n"
            data += f"respond_is_valid (回應): {int(ctx.guildConfig.respond_is_valid)}\n"
            data += f"respond_only_guild (只說伺服器內教的): {int(ctx.guildConfig.respond_only_guild)}\n\n"

            join_guild_msg_channel_name = self.bot.get_channel(ctx.guildConfig.join_guild_msg_channel)
            leave_guild_msg_channel_name = self.bot.get_channel(ctx.guildConfig.leave_guild_msg_channel)
            join_guild_msg_channel_name = join_guild_msg_channel_name if join_guild_msg_channel_name else ''
            leave_guild_msg_channel_name = leave_guild_msg_channel_name if leave_guild_msg_channel_name else ''

            data += f"join_msg_is_valid (開啟進群通知): {int(ctx.guildConfig.join_msg_is_valid)}\n"
            data += f"join_guild_msg_channel (進群的訊息頻道): {join_guild_msg_channel_name}\n\n"

            data += f"leave_msg_is_valid (開啟離群通知): {int(ctx.guildConfig.join_msg_is_valid)}\n"
            data += f"leave_guild_msg_channel (離群的訊息頻道): {leave_guild_msg_channel_name}\n\n"

            data += f"join_guild_cipher_is_valid (開啟進群密語): {int(ctx.guildConfig.join_guild_cipher_is_valid)}\n\n"

            data += f"+ 進群密語\n"
            data += f"cipher test (進群密語測試)\n"
            data += f"cipher modify <1~5> <訊息> (進群密語修改 訊息)\n"

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

    @setting.group()
    async def cipher(self, ctx):
        if ctx.guild:
            ctx.cipher = JoinGuildCipher.objects.get(guild_id=ctx.guild_id)
        

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

def setup(bot):
    bot.add_cog(Setting(bot))