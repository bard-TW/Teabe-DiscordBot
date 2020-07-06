
from bot.core.classes import Cog_Extension
from bot.core.cache import CACHE_REACTION, Reaction
# django
from django.conf import settings
from discord.ext import commands

class Base(Cog_Extension):
    async def getData_0(self, ctx):
        #目錄頁
        data_0 = f"<目錄頁> {settings.BOT_NAME}小幫手～\n"
        data_0 += f"```diff\n"
        data_0 += f"- 點擊下方反應會出現相對應說明\n"
        data_0 += f"注意: 指令跟參數和參數跟參數中間，皆需要有空白。\n\n"
        data_0 += f"+ {settings.REACTION_0} >> 回目錄\n"
        data_0 += f"+ {settings.REACTION_1} >> 說話功能\n"
        data_0 += f"+ {settings.REACTION_1} >> 隨機功能\n"
        data_0 += f"+ {settings.REACTION_9} >> 身份組功能\n"
        data_0 += f"+ {settings.REACTION_10} >> 管理者\\特殊功能\n"
        if ctx.author.id == settings.HOLDER_ID:
            #持有者特殊功能
            data_0 += f"+ {settings.REACTION_ADMIN} >> 持有者功能\n"
        data_0 += f"\n- 注意：{settings.BOT_NAME}退出群組後將移除此伺服器的所有設定\n"
        data_0 += f"```"
        return data_0
    
    async def getData_1(self, ctx):
        data_1 = f"<說話功能> {settings.BOT_NAME}小幫手～\n"
        data_1 += f"```diff\n"
        data_1 += f"+ {settings.BOT_NAME}學習指令\n"
        data_1 += f"API: {settings.PREFIX}學 <關鍵字> <回應1> <回應2> <回應N>\n"
        data_1 += f"範例: {settings.PREFIX}學 無聊怎麼辦 打騎士 耍廢 睡覺 看書\n\n"

        data_1 += f"觸發回 最後 回應:\n"
        data_1 += f"- ME: 無聊怎麼辦    {settings.BOT_NAME}: 睡覺\n"
        data_1 += f"觸發回 隨機 回應:\n"
        data_1 += f"- ME: {settings.BOT_NAME}無聊怎麼辦    {settings.BOT_NAME}: 看書\n\n"

        data_1 += f"+ {settings.BOT_NAME}查看指令\n"
        data_1 += f"API: {settings.PREFIX}查看清單 <空白\\@標記使用者>\n"
        data_1 += f"說明: 查看伺服器\\使用者有教哪些關鍵字\n"
        data_1 += f"API: {settings.PREFIX}查看關鍵字 <關鍵字>\n"
        data_1 += f"說明: 查看關鍵字內使用者教了有哪些回應\n\n"

        data_1 += f"+ {settings.BOT_NAME}忘記指令\n"
        data_1 += f"API: {settings.PREFIX}忘記 <關鍵字>\n"
        data_1 += f"說明: 忘記關鍵字內的最後一個回應\n"
        data_1 += f"API: {settings.PREFIX}忘記關鍵字 <關鍵字>\n"
        data_1 += f"說明: 忘記關鍵字內的全部回應\n"
        data_1 += f"```"
        return data_1

    async def getData_2(self, ctx):
        data_2 = f"<隨機功能> {settings.BOT_NAME}小幫手～\n"
        data_2 += f"```diff\n"
        data_2 += f"+ 瑪英小屋小鬼\n"
        data_2 += f"API:{settings.PREFIX}骰子 <訊息>\n"
        data_2 += f"說明：回應數字1~6\n"
        data_2 += f"範例：{settings.PREFIX}骰子 滾動吧骰子\n\n"

        data_2 += f"API:{settings.PREFIX}數字 <訊息>\n"
        data_2 += f"說明：回應數字1~100\n"
        data_2 += f"範例：{settings.PREFIX}數字 今天的幸運指數是？\n\n"

        data_2 += f"API:{settings.PREFIX}抽獎 <獎品1> <獎品2> <獎品3>\n"
        data_2 += f"說明：回應隨機獎品\n"
        data_2 += f"範例：{settings.PREFIX}抽獎 馬利 凱雅拉 蓋聯\n\n"

        data_2 += f"API:{settings.PREFIX}是否 <訊息>\n"
        data_2 += f"範例：{settings.PREFIX}是否 我穿得帥嗎?\n\n"

        data_2 += f"API:{settings.PREFIX}可以不可以 <訊息>\n"
        data_2 += f"範例：{settings.PREFIX}可以不可以 可以強化武器嗎?\n\n"

        data_2 += f"+ 疊塔\n"
        data_2 += f"API:{settings.PREFIX}塔 <表情符號> <1~5>\n"
        data_2 += f"API:{settings.PREFIX}進化塔 <表情符號> <1~20>\n"
        data_2 += f"```"
        return data_2

    async def getData_9(self, ctx):
        data_9 = f"<身份組功能> {settings.BOT_NAME}小幫手～\n"
        data_9 += f"```diff\n"

        data_9 += f"+ 賦予身份組 (打指令的方式賦予身份組)\n"
        data_9 += f"- 以下指令最前面需打 {settings.PREFIX}roles\n\n"

        data_9 += f"API: look\n"
        data_9 += f"說明: 查看目前您可以變更其他人的身份組\n\n"

        data_9 += f"API: add <@使用者(要標記到)> <新增身份組名稱>\n"
        data_9 += f"說明: 新增使用者身份組，身份組名稱可多個\n\n"
        
        data_9 += f"API: remove <@使用者(要標記到)> <移除身份組名稱>\n"
        data_9 += f"說明: 移除使用者身份組，身份組名稱可多個\n\n"

        data_9 += f"API: change <@使用者(要標記到)> <新增身份組名稱> > <移除身份組名稱> \n"
        data_9 += f"說明: 變更使用者身份組，身份組名稱可多個，新增移除中間需 > 符號\n\n"

        data_9 += f"```"
        return data_9

    async def getData_10(self, ctx):
        data_10 = f"<管理者\\特殊功能> {settings.BOT_NAME}小幫手～\n"
        data_10 += f"```diff\n"
        data_10 += f"+ 特殊功能\n"
        data_10 += f"API: {settings.PREFIX}ping\n"
        data_10 += f"說明: 查看延遲\n"
        data_10 += f"API: {settings.PREFIX}sayd <訊息>\n"
        data_10 += f"說明: 偽裝{settings.BOT_NAME}發送訊息(刪除後發送)\n\n"
        data_10 += f"API: {settings.PREFIX}限時 <1~1800> <訊息>\n"
        data_10 += f"說明: 限時<1~1800>秒刪除訊息\n\n"

        data_10 += f"+ 管理者功能(需管理身份祖權限)\n"
        data_10 += f"API: {settings.PREFIX}clean <1~200>\n"
        data_10 += f"說明: 清除<1~200>條訊息\n"
        data_10 += f"API: {settings.PREFIX}setting look\n"
        data_10 += f"說明: 查看目前{settings.BOT_NAME}設定\n"
        data_10 += f"```"
        return data_10

    async def getData_99(self, ctx):
        #持有者特殊功能
        data_99 = f"<持有者功能> {settings.BOT_NAME}小幫手～\n"
        data_99 += f"```diff\n"
        data_99 += f"+ 模塊讀取\n"
        data_99 += f"API: {settings.PREFIX}load <模塊>\n"
        data_99 += f"API: {settings.PREFIX}unload <模塊>\n"
        data_99 += f"API: {settings.PREFIX}reload <模塊>\n\n"

        data_99 += f"+ {settings.BOT_NAME}change_presence\n"
        data_99 += f"API: {settings.PREFIX}change_presence <0~3> <訊息>\n"
        data_99 += f"說明: 0:預設, 1:下線, 2:閒置, 3:忙碌 正在玩的訊息\n\n"

        data_99 += f"+ {settings.BOT_NAME}學打招呼\n"
        data_99 += f"API: {settings.PREFIX}學打招呼 <訊息>\n"
        data_99 += f"```"
        return data_99

    @commands.command()
    async def help(self, ctx):
        buttonActionDict = {
            settings.REACTION_0: 0, 
            settings.REACTION_1: 1,
            settings.REACTION_2: 2,
            settings.REACTION_9: 9,
            settings.REACTION_10: 10,
            }
        data_dict = {
            0: self.getData_0,
            1: self.getData_1,
            2: self.getData_2,
            9: self.getData_9,
            10: self.getData_10
        }
        if ctx.author.id == settings.HOLDER_ID:
            #持有者特殊功能
            buttonActionDict[settings.REACTION_ADMIN] =  99
            data_dict[99] = self.getData_99

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






















def setup(bot):
    bot.add_cog(Base(bot))