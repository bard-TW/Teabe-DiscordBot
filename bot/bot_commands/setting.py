import discord
from discord.ext import commands

from bot.models import Info_guild, Info_guildConfig, JoinGuildCipher, BotReactionRoles, Info_roles, BotPermissionRoles

from bot.core.classes import Cog_Extension
from bot.core.cache import CACHE_REACTION_ROLE, CACHE_REACTION, Reaction
from django.db.models import Count, F, Q, QuerySet, Max
from django.conf import settings

import re

from discord.ext.commands import has_permissions, MemberConverter

import asyncio

import traceback
# log
import logging

logger = logging.getLogger('bot')

async def get_roles(guild_id, roles_id, roles_name):
    roles = Info_roles.objects.filter(guild_id=guild_id, roles_id=roles_id)
    if roles:
        role = roles[0]
        if role.roles_name != roles_name:
            role.roles_name = roles_name
            role.save()
        else:
            return role
    else:
        Info_roles.objects.create(guild_id=guild_id, roles_id=roles_id, roles_name=roles_name)
        role = Info_roles.objects.get(guild_id=guild_id, roles_id=roles_id)
        return role

class Setting(Cog_Extension):
    @commands.group()
    @has_permissions(manage_roles=True)
    async def setting(self, ctx):
        ctx.guild_id = Info_guild.objects.get(guild_id=ctx.guild.id)
        ctx.guildConfig = Info_guildConfig.objects.get(guild_id=ctx.guild_id)

    async def getData_0(self, ctx):
        # 目錄頁
        data_0 = f"<目錄頁> 管理{settings.BOT_NAME}小幫手～\n"
        data_0 += f"```diff\n"
        data_0 += f"- 點擊下方反應會出現相對應說明\n"
        data_0 += f"注意: 指令跟參數和參數跟參數中間，皆需要有空白。\n\n"
        data_0 += f"+ {settings.REACTION_0} >> 回目錄\n"
        data_0 += f"+ {settings.REACTION_1} >> 基本設定\n"
        data_0 += f"+ {settings.REACTION_2} >> 進群密語\n"
        data_0 += f"+ {settings.REACTION_3} >> 反應權限\n"
        data_0 += f"+ {settings.REACTION_3} >> 權限賦予身份組\n"
        data_0 += f"\n- 注意：{settings.BOT_NAME}退出群組後將移除此伺服器的所有設定\n"
        data_0 += f"```"
        return data_0

    async def getData_1(self, ctx):
        # 基本設定
        ctx.guildConfig = Info_guildConfig.objects.get(guild_id=ctx.guild_id)
        data_1 = f"<基本設定> 管理{settings.BOT_NAME}小幫手～\n"
        data_1 += f"```diff\n"
        data_1 += f"下方功能狀態 0:關閉 1:開啟 下指令可控制開關\n"
        data_1 += f"開關推齊範例: {settings.PREFIX}setting previou_is_valid\n"
        data_1 += f"設置進群(離群)通知頻道在要設置的頻道內相同的方式輸入，即可設置\n\n"
        data_1 += f"+ 功能狀態\n"
        data_1 += f"- 以下指令最前面需打 {settings.PREFIX}setting\n"
        data_1 += f"previou_is_valid (推齊功能): {int(ctx.guildConfig.previou_is_valid)}\n"
        data_1 += f"respond_is_valid (回應): {int(ctx.guildConfig.respond_is_valid)}\n"
        data_1 += f"respond_only_guild (只說伺服器內教的): {int(ctx.guildConfig.respond_only_guild)}\n\n"
        join_guild_msg_channel_name = self.bot.get_channel(ctx.guildConfig.join_guild_msg_channel)
        leave_guild_msg_channel_name = self.bot.get_channel(ctx.guildConfig.leave_guild_msg_channel)
        join_guild_msg_channel_name = join_guild_msg_channel_name if join_guild_msg_channel_name else ''
        leave_guild_msg_channel_name = leave_guild_msg_channel_name if leave_guild_msg_channel_name else ''
        data_1 += f"join_msg_is_valid (開啟進群通知): {int(ctx.guildConfig.join_msg_is_valid)}\n"
        data_1 += f"join_guild_msg_channel (進群的訊息頻道): {join_guild_msg_channel_name}\n\n"
        data_1 += f"leave_msg_is_valid (開啟離群通知): {int(ctx.guildConfig.join_msg_is_valid)}\n"
        data_1 += f"leave_guild_msg_channel (離群的訊息頻道): {leave_guild_msg_channel_name}\n\n"
        data_1 += f"join_guild_cipher_is_valid (開啟進群密語): {int(ctx.guildConfig.join_guild_cipher_is_valid)}\n\n"
        data_1 += f"```"
        return data_1

    async def getData_2(self, ctx):
        # 進群密語
        data_2 = f"<進群密語> 管理{settings.BOT_NAME}小幫手～\n"
        data_2 += f"```diff\n"
        data_2 += f"+ 進群密語 (使用者進群後的使用者密語通知訊息)\n"
        data_2 += f"- 以下指令最前面需打 {settings.PREFIX}cipher\n"
        data_2 += f"test (進群密語測試)\n"
        data_2 += f"modify <1~5> <訊息> (進群密語修改 訊息)\n\n"
        data_2 += f"```"
        return data_2

    async def getData_3(self, ctx):
        # 進群密語
        data_3 = f"<反應權限> 管理{settings.BOT_NAME}小幫手～\n"
        data_3 += f"```diff\n"
        data_3 += f"+ 反應權限 (點擊反應後可以獲得身份組)\n"
        data_3 += f"- 以下指令最前面需打 {settings.PREFIX}reaction\n"
        data_3 += f"look (查看目前所設定的反應權限)\n"
        data_3 += f"add <訊息ID> <反應> <身份組名稱> <反應> <身份組名稱> (反應和權限名稱可一次新增多個)\n"
        data_3 += f"remove <訊息ID> (刪除訊息ID裡的全部反應權限))\n\n"
        data_3 += f"```"
        return data_3

    async def getData_4(self, ctx):
        # 權限賦予身份組
        data_4 = f"<權限賦予身份組> 管理{settings.BOT_NAME}小幫手～\n"
        data_4 += f"```diff\n"
        data_4 += f"+ 權限賦予身份組 (設定可以用打指令的方式賦予身份組)\n"
        data_4 += f"- 以下指令最前面需打 {settings.PREFIX}permission\n"
        data_4 += f"look (查看目前所設定的權限賦予身份組)\n"
        data_4 += f"add <擁有身份組名稱> <賦予身份組名稱> <賦予身份組名稱> (新增權限賦予身份組))\n"
        data_4 += f"remove <擁有身份組名稱> (移除擁有身份組名稱裡全部設定))\n"
        data_4 += f"```"
        return data_4

    @setting.command()
    async def look(self, ctx):
        buttonActionDict = {
            settings.REACTION_0: 0, 
            settings.REACTION_1: 1,
            settings.REACTION_2: 2,
            settings.REACTION_3: 3,
            settings.REACTION_4: 4,
            }
        data_dict = {
            0: self.getData_0,
            1: self.getData_1,
            2: self.getData_2,
            3: self.getData_3,
            4: self.getData_4,
        }
        reaction = Reaction()
        reaction.data_dict = data_dict
        reaction.ctx = ctx
        reaction.buttonActionDict = buttonActionDict
        message = await ctx.send(await data_dict[0](ctx))

        reaction.msg = message
        CACHE_REACTION[message.id] = reaction

        for react in reaction.buttonActionDict.keys():
            await message.add_reaction(react)
        await ctx.message.add_reaction(settings.REACTION_SUCCESS)

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
        guild_id = Info_guild.objects.get(guild_id=ctx.guild.id)
        ctx.cipher = JoinGuildCipher.objects.get(guild_id=guild_id)

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

class ReactionRole(Cog_Extension):
    @commands.group()
    @has_permissions(manage_roles=True)
    async def reaction(self, ctx):
        ctx.guild_id = Info_guild.objects.get(guild_id=ctx.guild.id)
        ctx.role_dict = {}
        ctx.role_id_dict = {}
        for i, role in enumerate(ctx.guild.roles, start=1):
            ctx.role_dict[role.name] = role.id
            ctx.role_id_dict[role.id] = role.name
            if len(ctx.role_dict.keys()) < i:
                await ctx.send('身份組名稱重複')
                return

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

                        role = await get_roles(guild_id=ctx.guild_id, roles_id=role_id, roles_name=role_list[i])

                        if len(emoji_list[i]) >5:
                            emoji_match = pattern.match(emoji_list[i])
                            emoji_id = emoji_match[2]
                            emoji_Name = emoji_match[1]
                            reaction = BotReactionRoles.objects.filter(guild_id=ctx.guild_id, msg_id=msg_id, emoji_id=emoji_id, roles_id=role)
                        else:
                            emoji_Name = emoji_list[i]
                            reaction = BotReactionRoles.objects.filter(guild_id=ctx.guild_id, msg_id=msg_id, emoji_name=emoji_Name, roles_id=role)

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
                                roles_id= role,
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

        roles = Info_roles.objects.filter(guild_id=ctx.guild_id)
        for role in roles:
            roles_name = ctx.role_id_dict.get(role.roles_id)
            if not roles_name:  # 搜不到權限 刪除
                role.delete()
                continue
            elif roles_name != role.roles_name:  # 權限名有異動
                role.roles_name = roles_name
                role.save()

        reaction_dict = {}
        reaction = BotReactionRoles.objects.filter(guild_id=ctx.guild_id)

        if not reaction:
            await ctx.send('無定義權限反應')
            return

        for rea in reaction:
            if rea.msg_id in reaction_dict.keys():
                reaction_dict[rea.msg_id].append({'emoji_id': rea.emoji_id, 'emoji_name': rea.emoji_name, 'roles_name': rea.roles_id.roles_name})
            else:
                reaction_dict[rea.msg_id] = [{'emoji_id': rea.emoji_id, 'emoji_name': rea.emoji_name, 'roles_name': rea.roles_id.roles_name}]
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

class Permission(Cog_Extension):
    @commands.group()
    @has_permissions(manage_roles=True)
    async def permission(self, ctx):
        ctx.guild_id = Info_guild.objects.get(guild_id=ctx.guild.id)
        ctx.role_dict = {}
        ctx.role_id_dict = {}
        for i, role in enumerate(ctx.guild.roles, start=1):
            ctx.role_dict[role.name] = role.id
            ctx.role_id_dict[role.id] = role.name
            if len(ctx.role_dict.keys()) < i:
                await ctx.send('身份組名稱重複')
                return


    @permission.command()
    async def look(self, ctx):
        if ctx.role_dict == {}:
            return

        roles = Info_roles.objects.filter(guild_id=ctx.guild_id)
        for role in roles:
            roles_name = ctx.role_id_dict.get(role.roles_id)
            if not roles_name:  # 搜不到權限 刪除
                role.delete()
                continue
            elif roles_name != role.roles_name:  # 權限名有異動
                role.roles_name = roles_name
                role.save()

        rermissionRole_dict = {}
        rermissionRoles = BotPermissionRoles.objects.filter(guild_id=ctx.guild_id)
        if not rermissionRoles:
            await ctx.send('無定義權限賦予身份組')
            return
        for rermissionRole in rermissionRoles:
            if rermissionRole.permission in rermissionRole_dict.keys():
                rermissionRole_dict[rermissionRole.permission].append(rermissionRole)
            else:
                rermissionRole_dict[rermissionRole.permission] = [rermissionRole]

        # 處理顯示文字
        msg = '權限賦予身份組```diff\n'
        for rermissionRole in rermissionRole_dict.keys():
            msg += f'{rermissionRole.roles_name} > '
            
            for role in rermissionRole_dict[rermissionRole]:
                msg += f'{role.roles.roles_name} '
            msg += '\n'
        msg += '\n'
        msg += f"- 以下指令最前面需打 {settings.PREFIX}permission\n"
        msg += f"add <擁有身份組名稱> <賦予身份組名稱> <賦予身份組名稱> (新增權限賦予身份組))\n"
        msg += f"remove <擁有身份組名稱> (移除擁有身份組名稱裡全部設定))\n"
        msg += '```'
        await ctx.send(msg)

    @permission.command()
    async def add(self, ctx, per, *args):
        permission_id = ctx.role_dict.get(per)
        if permission_id:
            msg = '建立狀態\n```diff\n'
            permission = await get_roles(guild_id=ctx.guild_id, roles_id=permission_id, roles_name=per)
            for arg in args:
                role_id = ctx.role_dict.get(arg)
                if role_id:
                    roles = await get_roles(guild_id=ctx.guild_id, roles_id=role_id, roles_name=arg)

                    permissionRoles = BotPermissionRoles.objects.filter(guild_id=ctx.guild_id, permission=permission, roles=roles)
                    if not permissionRoles:
                        BotPermissionRoles.objects.create(guild_id=ctx.guild_id, permission=permission, roles=roles)
                        msg += f'+ {per} > {arg} 建立成功\n'
                    else:
                        msg += f'- {per} > {arg} 已建立\n'
                else:
                    msg += f'- {per} > {arg} 查無此身份組\n'
            msg += '```'
            await ctx.send(msg)
        else:
            await ctx.send(f'查無此身份組: {per}')

    @permission.command()
    async def remove(self, ctx, per):
        permission_id = ctx.role_dict.get(per)
        if permission_id:
            permission = await get_roles(guild_id=ctx.guild_id, roles_id=permission_id, roles_name=per)
            permissionRoles = BotPermissionRoles.objects.filter(guild_id=ctx.guild_id, permission=permission)
            if permissionRoles:
                permissionRoles.delete()
                await ctx.send(f'移除成功')
            else:
                await ctx.send(f'此權限無資料: {per}')
        else:
            await ctx.send(f'查無此身份組: {per}')

class Roles(Cog_Extension):
    @commands.group()
    async def roles(self, ctx):
        ctx.guild_id = Info_guild.objects.get(guild_id=ctx.guild.id)
        roles = []
        for author_roles in ctx.message.author.roles:
            roles.append(await get_roles(guild_id=ctx.guild_id, roles_id=author_roles.id, roles_name=author_roles.name))
        q_permission = Q(permission__in=roles)
        permissionRoles = BotPermissionRoles.objects.filter(q_permission)

        ctx.roles_dict = {}
        for permissionRole in permissionRoles:
            ctx.roles_dict[permissionRole.roles.roles_name] = permissionRole.roles.roles_id

    @roles.command()
    async def look(self, ctx):
        msg = '您可以變更其他人的身份組: \n'
        for role in ctx.roles_dict.keys():
            msg += f'{role} '
        await ctx.send(msg)

    @roles.command()
    async def add(self, ctx, user, *role_names):
        roles_name_list = ctx.roles_dict.keys()
        member = await MemberConverter().convert(ctx, user)
        owner_role_id_list = await self.update_member_roles(member=member)
        msg = '新增身份組狀態\n```diff\n'
        for role_name in role_names:
            if role_name in roles_name_list:
                msg += await self.addRole(ctx=ctx, member=member, role_name=role_name, owner_role_id_list=owner_role_id_list)
            else:
                msg += f'- {role_name} 查無此分身組或無權限\n'
        msg += '```'
        await ctx.send(msg)

    @roles.command()
    async def remove(self, ctx, user, *role_names):
        roles_name_list = ctx.roles_dict.keys()
        member = await MemberConverter().convert(ctx, user)
        owner_role_id_list = await self.update_member_roles(member=member)
        msg = '移除身份組狀態\n```diff\n'
        for role_name in role_names:
            if role_name in roles_name_list:
                msg += await self.removeRole(ctx=ctx, member=member, role_name=role_name, owner_role_id_list=owner_role_id_list)
            else:
                msg += f'- {role_name} 查無此分身組或無權限\n'
        msg += '```'
        await ctx.send(msg)

    @roles.command()
    async def change(self, ctx, user, *role_names):
        if '>' in role_names:
            roles_name_list = ctx.roles_dict.keys()
            member = await MemberConverter().convert(ctx, user)
            owner_role_id_list = await self.update_member_roles(member=member)
            is_remove = False
            msg = '轉換身份組狀態\n```diff\n'
            for role_name in role_names:
                if role_name == '>':
                    is_remove = True
                    owner_role_id_list = await self.update_member_roles(member=member)
                    continue
                if role_name in roles_name_list:
                    if is_remove:
                        msg += await self.removeRole(ctx=ctx, member=member, role_name=role_name, owner_role_id_list=owner_role_id_list)
                    else:
                        msg += await self.addRole(ctx=ctx, member=member, role_name=role_name, owner_role_id_list=owner_role_id_list)
                else:
                    msg += f'- {role_name} 查無此分身組或無權限\n'
            msg += '```'
            await ctx.send(msg)
        else:
            await ctx.send(f'格式錯誤')

    async def addRole(self, ctx, member, role_name, owner_role_id_list):
        msg = ''
        if ctx.roles_dict[role_name] not in owner_role_id_list:
            try:
                role = discord.utils.get(ctx.guild.roles, id=ctx.roles_dict[role_name])
                await member.add_roles(role)
                msg += f'+ {role_name} 新增成功\n'
            except:
                msg += f'- {role_name} 未知錯誤\n'
        else:
            msg += f'- {role_name} 已擁有分身組\n'
        return msg

    async def removeRole(self, ctx, member, role_name, owner_role_id_list):
        msg = ''
        if ctx.roles_dict[role_name] in owner_role_id_list:
            try:
                role = discord.utils.get(ctx.guild.roles, id=ctx.roles_dict[role_name])
                await member.remove_roles(role)
                msg += f'+ {role_name} 移除成功\n'
            except:
                msg += f'- {role_name} 未知錯誤\n'
        else:
            msg += f'- {role_name} 未擁有分身組\n'
        return msg

    async def update_member_roles(self, member):
        owner_role_id_list = []
        for role in member.roles:
            owner_role_id_list.append(role.id)
        return owner_role_id_list

def setup(bot):
    bot.add_cog(Setting(bot))
    bot.add_cog(Cipher(bot))
    bot.add_cog(ReactionRole(bot))
    bot.add_cog(Permission(bot))
    bot.add_cog(Roles(bot))