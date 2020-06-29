
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
        data_0 += f"注意: 使用指令時\n"
        data_0 += f"+ {settings.REACTION_0} >> 回目錄\n"
        data_0 += f"+ {settings.REACTION_1} >> 說話功能\n"
        data_0 += f"+ {settings.REACTION_10} >> 管理者\\特殊功能\n"
        if ctx.author.id == settings.HOLDER_ID:
            #持有者特殊功能
            data_0 += f"+ {settings.REACTION_ADMIN} >> 持有者功能\n"
        data_0 += f"```"
        return data_0
    
    async def getData_1(self, ctx):
        data_1 = f"<說話功能> {settings.BOT_NAME}小幫手～\n"
        data_1 += f"```diff\n"
        data_1 += f"+ {settings.BOT_NAME}學習指令\n"
        data_1 += f"API: {settings.PREFIX}學 <關鍵字> <回應1> <回應2> <回應N>\n"
        data_1 += f"範例: {settings.PREFIX}學 無聊怎麼辦 打後7 打中4 打前6 打騎士 耍費 睡覺\n\n"
        data_1 += f"觸發回 最後 回應:\n"
        data_1 += f"- ME: 無聊怎麼辦    提比: 睡覺\n"
        data_1 += f"觸發回 隨機 回應:\n"
        data_1 += f"- ME: 提比無聊怎麼辦    提比: 打後7\n\n"
        data_1 += f"+ {settings.BOT_NAME}查看指令\n"
        data_1 += f"API: {settings.PREFIX}查看清單 <空白\\@標記使用者>\n"
        data_1 += f"說明: 查看伺服器\\使用者有教哪些關鍵字\n"
        data_1 += f"API: {settings.PREFIX}查看關鍵字 <關鍵字>\n\n"
        data_1 += f"說明: 查看關鍵字內使用者教了有哪些回應\n"
        data_1 += f"+ {settings.BOT_NAME}忘記指令\n"
        data_1 += f"API: {settings.PREFIX}忘記 <關鍵字>\n"
        data_1 += f"說明: 忘記關鍵字內的最後一個回應\n"
        data_1 += f"API: {settings.PREFIX}忘記關鍵字 <關鍵字>\n"
        data_1 += f"說明: 忘記關鍵字內的全部回應\n"
        data_1 += f"```"
        return data_1

    async def getData_10(self, ctx):
        data_10 = f"<管理者\\特殊功能> {settings.BOT_NAME}小幫手～\n"
        data_10 += f"```diff\n"
        data_10 += f"+ 特殊功能\n"
        data_10 += f"API: {settings.PREFIX}ping\n"
        data_10 += f"說明: 查看延遲\n"
        data_10 += f"API: {settings.PREFIX}sayd <訊息>\n"
        data_10 += f"說明: 偽裝{settings.BOT_NAME}發送訊息(刪除後發送)\n\n"
        data_10 += f"+ 管理者功能(需權限)\n"
        data_10 += f"API: {settings.PREFIX}clean <數量>\n"
        data_10 += f"說明: 清除<數量>條訊息\n"
        data_10 += f"```"
        return data_10

    async def getData_99(self, ctx):
        #持有者特殊功能
        data_99 = f"<持有者功能> {settings.BOT_NAME}小幫手～\n"
        data_99 += f"```diff\n"
        data_99 += f"+ 模塊讀取\n"
        data_99 += f"API: {settings.PREFIX}load <模塊>\n"
        data_99 += f"API: {settings.PREFIX}unload <模塊>\n"
        data_99 += f"API: {settings.PREFIX}reload <模塊>\n"

        data_99 += f"+ {settings.BOT_NAME}狀態\n"
        data_99 += f"API: {settings.PREFIX}change_presence <0~3> <訊息>\n"
        data_99 += f"說明: 0:預設, 1:下線, 2:閒置, 3:忙碌 正在玩的訊息"
        
        data_99 += f"```"
        return data_99

    @commands.command()
    async def help(self, ctx):
        buttonActionDict = {
            settings.REACTION_0: 0, 
            settings.REACTION_1: 1,
            settings.REACTION_10: 10,
            }
        data_dict = {
            0: await self.getData_0(ctx),
            1: await self.getData_1(ctx),
            10: await self.getData_10(ctx)
        }
        if ctx.author.id == settings.HOLDER_ID:
            #持有者特殊功能
            buttonActionDict[settings.REACTION_ADMIN] =  99
            data_dict[99] = await self.getData_99(ctx)

        reaction = Reaction()
        reaction.data_dict = data_dict
        reaction.buttonActionDict = buttonActionDict

        message = await ctx.send(data_dict[0])
        reaction.msg = message
        CACHE_REACTION[message.id] = reaction

        for react in reaction.buttonActionDict.keys():
            await message.add_reaction(react)
        await ctx.message.add_reaction(settings.REACTION_SUCCESS)






















def setup(bot):
    bot.add_cog(Base(bot))