# discord
import discord
from discord.ext import commands
from discord.ext.commands import UserConverter

# django
from django.conf import settings
from bot.models import Info_guild, Info_author, Info_guildNickname, BotResponds, Info_guildConfig, BotHelloResponds
from django.db.models import Count, F, Q, QuerySet, Max
from django.core.exceptions import ObjectDoesNotExist

import asyncio
import random
import re
from datetime import datetime


from bot.core.classes import Cog_Extension
from bot.core.cache import CACHE_REACTION, Reaction

import logging
logger = logging.getLogger('bot')

class MsgHandler(Cog_Extension):
    previou_msg_dict = {}  # 紀錄各頻道最後訊息
    previou_reply_dict = {}  # 紀錄各頻道最後推齊訊息

    @commands.Cog.listener()
    async def on_message(self, msg):
        # 對機器人密語
        if type(msg.channel) == discord.channel.DMChannel and msg.author != self.bot.user:
            channel = self.bot.get_channel(settings.BOT_CIPHER_CHANNEL)
            send_msg = "{} {} 說：\n{}".format(msg.author.id, msg.author, msg.content)
            for attachment in msg.attachments:
                send_msg += '\n{}'.format(attachment.url)
            logger.info(send_msg)
            if channel:
                await channel.send(send_msg)

        # 回話功能
        if not msg.guild:
            return
        guild_id = Info_guild.objects.get(guild_id=msg.guild.id)
        guildConfig = Info_guildConfig.objects.get(guild_id=guild_id)
        if (not msg.author.bot) and (guildConfig.respond_is_valid):
            respond = ''
            if settings.BOT_NAME == msg.content:
                # 打招呼
                responds = BotHelloResponds.objects.all()
                if responds:
                    respond = random.choice(responds)

            elif settings.BOT_NAME == msg.content[:len(settings.BOT_NAME)]:
                # 隨機回話
                keyword = msg.content[len(settings.BOT_NAME):]
                if guildConfig.respond_only_guild:
                    responds = BotResponds.objects.filter(keyword=keyword, guild_id=guild_id)
                else:
                    responds = BotResponds.objects.filter(keyword=keyword)
                if responds:
                    respond = random.choice(responds.values('respond'))['respond']
            else:
                # 回最後一句
                keyword = msg.content
                if guildConfig.respond_only_guild:
                    responds = BotResponds.objects.filter(keyword=keyword, guild_id=guild_id).last()
                else:
                    responds = BotResponds.objects.filter(keyword=keyword).last()
                if responds:
                    respond = responds.respond

            if respond:
                await asyncio.sleep(0.5)
                await msg.channel.send(respond)
                return

        # 推齊
        if (not msg.author.bot) and (guildConfig.previou_is_valid):
            respond = await self.replay(msg)

            if respond:
                await asyncio.sleep(0.5)
                await msg.channel.send(respond)
                return

    async def replay(self, msg):
        # 推齊功能
        previou_msg = self.previou_msg_dict.get(msg.channel)
        if previou_msg == msg.content:
            previou_reply = self.previou_reply_dict.get(msg.channel)
            if previou_reply != msg.content:
                self.previou_reply_dict[msg.channel] = msg.content
                return msg.content

        else:
            self.previou_msg_dict[msg.channel] = msg.content
        return None

    @commands.command()
    async def 學(self, ctx, keyword, *arg):
        if not ctx.guild:
            await ctx.send('私人頻道無法使用此功能')
            return

        if keyword[:2] != settings.BOT_NAME:
            if len(arg):
                # 公會名稱更新
                guild_data = Info_guild.objects.get(guild_id=ctx.guild.id)

                # author名稱更新
                author_data = Info_author.objects.filter(author_id=ctx.author.id)
                if author_data:
                    author = author_data.values()[0]['author']
                    if author != str(ctx.author):
                        logger.info(f'update author name: {author} > {str(ctx.author)}')
                        author_data.update(author=str(ctx.author))
                else:
                    Info_author.objects.create(author=str(ctx.author), author_id=ctx.author.id)
                    author_data = Info_author.objects.filter(author_id=ctx.author.id)

                # 公會暱稱更新
                nickname_data = Info_guildNickname.objects.filter(guild_id=guild_data[0], author_id=author_data[0])
                if nickname_data:
                    nickname = nickname_data.values()[0]['nickname']
                    if nickname != str(ctx.author.display_name):
                        logger.info(f'update nickname: {nickname} > {str(ctx.author.display_name)}')
                        nickname_data.update(nickname=ctx.author.display_name)
                else:
                    Info_guildNickname.objects.create(guild_id=guild_data[0], author_id=author_data[0], nickname=ctx.author.display_name)
                    nickname_data = Info_guildNickname.objects.filter(guild_id=guild_data[0], author_id=author_data[0])

                # 回應更新
                for respond in arg:
                    botResponds_data = BotResponds.objects.filter(keyword=keyword, guild_id=guild_data[0], author_id=author_data[0], respond=respond)
                    if not botResponds_data:
                        BotResponds.objects.create(keyword=keyword, guild_id=guild_data[0], author_id=author_data[0], respond=respond)
                        await ctx.message.add_reaction(settings.REACTION_SUCCESS)
            else:
                await ctx.message.add_reaction(settings.REACTION_FAILURE)
                await ctx.send('無關鍵字回應 > <')
        else:
            await ctx.message.add_reaction(settings.REACTION_FAILURE)
            await ctx.send(f'請勿使用 *{settings.BOT_NAME}* 開頭的關鍵字 > <')

    @commands.command()
    async def 忘記(self, ctx, keyword=None, *arg):
        if not ctx.guild:
            await ctx.send('私人頻道無法使用此功能')
            return
        if keyword:
            guild_id = Info_guild.objects.get(guild_id=ctx.guild.id)
            responds = BotResponds.objects.filter(keyword=keyword, guild_id=guild_id).last()
            if responds:
                await ctx.send(f'我把 __{responds.respond}__ 忘記惹！')
                responds.delete()
                await ctx.message.add_reaction(settings.REACTION_SUCCESS)
            else:
                await ctx.send(f'本{settings.BOT_NAME}沒學過喔！')
                await ctx.message.add_reaction(settings.REACTION_FAILURE)
        else:
            await ctx.send('請輸入你要查詢的關鍵字喔!')
            await ctx.message.add_reaction(settings.REACTION_FAILURE)

    @commands.command()
    async def 忘記關鍵字(self, ctx, keyword=None, *arg):
        if not ctx.guild:
            await ctx.send('私人頻道無法使用此功能')
            return
        if keyword:
            guild_id = Info_guild.objects.get(guild_id=ctx.guild.id)
            responds = BotResponds.objects.filter(keyword=keyword, guild_id=guild_id)
            if responds:
                await ctx.send(f'我把 __{keyword}__ 忘記惹！')
                responds.delete()
                await ctx.message.add_reaction(settings.REACTION_SUCCESS)
            else:
                await ctx.send(f'本{settings.BOT_NAME}沒學過喔！')
                await ctx.message.add_reaction(settings.REACTION_FAILURE)
        else:
            await ctx.message.add_reaction(settings.REACTION_FAILURE)
            await ctx.send('請輸入你要查詢的關鍵字喔!')

    @commands.command()
    async def 學打招呼(self, ctx, *arg):
        if ctx.author.id == settings.HOLDER_ID:
            respond = " ".join(arg)
            data = BotHelloResponds.objects.filter(respond=respond)
            if not data:
                BotHelloResponds.objects.create(respond=respond)
                await ctx.message.add_reaction(settings.REACTION_SUCCESS)
            else:
                await ctx.send(f'{settings.BOT_NAME}已經會了！')
                await ctx.message.add_reaction(settings.REACTION_FAILURE)

    @commands.command()
    async def 回(self, ctx, toUser, *msg):
        # 機器人回話
        member = await UserConverter().convert(ctx, toUser)
        send_msg = ''.join(msg)
        for attachment in ctx.message.attachments:
            send_msg += '\n{}'.format(attachment.url)
        await member.send(send_msg)
        await ctx.message.add_reaction(settings.REACTION_SUCCESS)

    @commands.command()
    async def 查看清單(self, ctx, *arg):
        if not ctx.guild:
            await ctx.send('私人頻道無法使用此功能')
            return
        data = {}
        if arg:
            author = await self.msg2author(arg)
            if author:
                author_id = (
                    Info_author.objects
                    .get(author_id=author)
                )
                data['author_id'] = author_id
            else:
                await ctx.send('標記錯誤！')
                await ctx.message.add_reaction(settings.REACTION_FAILURE)
                return
        else:
            guild_id = (
                Info_guild.objects
                .get(guild_id=ctx.guild.id)
            )
            data['guild_id'] = guild_id

        qs = (
            BotResponds.objects
            .values('keyword')
            .filter(**data)
            .annotate(max_id=Max('info_id'))
        )
        if qs:
            id_list = qs.values_list('max_id', flat=True)
            q_info_id = Q(info_id__in=list(id_list))
            responds = BotResponds.objects.filter(q_info_id).values('keyword', 'respond')
            reaction = Reaction()
            reaction.data_list_key = 'keyword'
            reaction.data_list_value = 'respond'
            await self.queryList(ctx, responds, reaction)
            return
        else:
            await ctx.send('查無資料')
            await ctx.message.add_reaction(settings.REACTION_FAILURE)
            return
        await ctx.send(f'疑是出現錯誤，可向{settings.BOT_NAME}密語反應喔！')

    @commands.command()
    async def 查看關鍵字(self, ctx, keyword=None, *arg):
        if keyword:
            responds = (
                BotResponds.objects
                .select_related('author_id').all()
                .values('respond', 'author_id__author')
                .filter(keyword=keyword)
            )

            if responds:
                reaction = Reaction()
                reaction.data_list_key = 'respond'
                reaction.data_list_value = 'author_id__author'
                await self.queryList(ctx, responds, reaction)
                return
            else:
                await ctx.send('查無資料')
                await ctx.message.add_reaction(settings.REACTION_FAILURE)
                return
        else:
            await ctx.send('請輸入你要查詢的關鍵字!')
            await ctx.message.add_reaction(settings.REACTION_FAILURE)
            return
        await ctx.send(f'疑是出現錯誤，可向{settings.BOT_NAME}密語反應喔！')


    async def queryList(self, ctx, responds, reaction):
        result = [responds[i:i+12] for i in range(0, len(responds), 12)]
        reaction.data_list = result

        if len(result)>=2:
            reaction.buttonActionDict = {settings.REACTION_BACKWARD: -1, settings.REACTION_FORWARD: 1}
        embed = reaction.makeQueryList()
        if embed:
            message = await ctx.send(embed=embed)
            reaction.msg = message
            CACHE_REACTION[message.id] = reaction

            for react in reaction.buttonActionDict.keys():
                await message.add_reaction(react)
            await ctx.message.add_reaction(settings.REACTION_SUCCESS)

    async def msg2author(self, msgs):
        pattern = re.compile(r'<@!?(\d*)>')
        for msg in msgs:
            match = pattern.match(msg)
            if match:
                return match.group(1)
        return None


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # 加入表情反應
        await self.changeMsgReaction(reaction, user)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        # 解除表情反應
        await self.changeMsgReaction(reaction, user)

    async def changeMsgReaction(self, reaction, user):
        if (not user.bot):
            rea = CACHE_REACTION.get(reaction.message.id)
            if rea and rea.data_list:
                embed = rea.makeQueryList(str(reaction))
                if embed:
                    await reaction.message.edit(embed=embed)
                    rea.time=datetime.now()
            elif rea and rea.data_dict:
                fun, ctx = rea.makeQueryDict(str(reaction))
                data = None
                if fun and ctx:
                    data = await fun(ctx)
                if data:
                    await reaction.message.edit(content=data)
                    rea.time=datetime.now()

            now = datetime.now()
            for msg_id in list(CACHE_REACTION):
                if (now - CACHE_REACTION[msg_id].time).seconds > 600:
                    for react in CACHE_REACTION[msg_id].buttonActionDict.keys():
                        await CACHE_REACTION[msg_id].msg.remove_reaction(react, self.bot.user)
                    del(CACHE_REACTION[msg_id])


def setup(bot):
    bot.add_cog(MsgHandler(bot))