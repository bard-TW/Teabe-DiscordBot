import discord
from django.conf import settings
from datetime import datetime


CACHE_REACTION = {}
CACHE_REACTION_ROLE = [] # 存放有反應權限的訊息ID

class Reaction(object):
    title = ''  # 標題
    remark = ''  # 備註
    msg = None  # 對話ID
    time = None  # 操作時間
    data_list = list() # 雙列表
    data_list_key = ''
    data_list_value = ''
    data_dict = dict() # 按鈕作用對應字典文字
    page = int()  # 頁數
    buttonActionDict = dict()  # 按鈕作用
    ctx = None # 上下文
    reactionFunction = None
    is_embed = False

    def __init__(self,):
        self.time = datetime.now()

    def makeQueryEmbed(self, button=None):
        if button:
            num = self.buttonActionDict.get(button)
        else:
            num = 0
        if num != None:
            self.page += num
            if 0 <= self.page < len(self.data_list):
                datas = self.data_list[self.page]
                embed=discord.Embed(title=self.title)
                for data in datas:
                    embed.add_field(name=data[self.data_list_key], value=data[self.data_list_value], inline=True)
                if len(self.data_list) > 1:
                    embed.set_footer(text=f"第{self.page+1}頁, 共{len(self.data_list)}頁, 反應慢請慢慢點喔")
                return embed
            else:
                self.page -= num
        return None

    def makeQueryList(self, button=None):
        if button:
            num = self.buttonActionDict.get(button)
        else:
            num = 0
        if num != None:
            self.page += num
            if 0 <= self.page < len(self.data_list):
                datas = self.data_list[self.page]
                msg = f'{self.title}\n\n'
                for data in datas:
                    msg += f'> {data[self.data_list_key]}\n'
                    msg += f'```{data[self.data_list_value]}```\n'
                if len(self.data_list) > 1:
                    msg+=(f"\n第{self.page+1}頁, 共{len(self.data_list)}頁, 反應慢請慢慢點喔")
                return msg
            else:
                self.page -= num
        return None

    def makeQueryDict(self, button=None):
        if button:
            num = self.buttonActionDict.get(button)
        else:
            num = 0
        if num != None and num != self.page:
            self.page = num
            fun = self.data_dict.get(num)
            if fun:
                return fun, self.ctx
        return None, None