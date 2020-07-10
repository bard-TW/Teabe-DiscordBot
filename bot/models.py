from django.db import models
from django.utils import timezone

# Create your models here.
# verbose_name 網頁上名稱
# help_text 網頁上註釋

class Info_guild(models.Model):
    guild = models.CharField(max_length=50, help_text='guild name', verbose_name='公會名')
    guild_id = models.IntegerField(help_text='guild id', verbose_name='公會代碼')
    remark = models.TextField(max_length=100, null=True, blank=True, verbose_name='備註')
    def __str__(self):
        return self.guild
    class Meta:
        verbose_name = "Info 公會"
        verbose_name_plural = "Info 1 公會"

class Info_author(models.Model):
    author = models.CharField(max_length=50, help_text='author name', verbose_name='角色名')
    author_id = models.IntegerField(help_text='author id', verbose_name='角色代碼')
    def __str__(self):
        return self.author
    class Meta:
        verbose_name = "Info 角色"
        verbose_name_plural = "Info 2 角色"

class Info_guildNickname(models.Model):
    guild_id = models.ForeignKey(Info_guild, on_delete=models.CASCADE, blank=True, null=True, verbose_name='公會')
    author_id = models.ForeignKey(Info_author, on_delete=models.CASCADE, blank=True, null=True, verbose_name='角色')
    nickname = models.CharField(max_length=50, verbose_name='公會暱稱', help_text='在伺服器裡的角色暱稱')
    def __str__(self):
        return self.nickname
    class Meta:
        verbose_name = "Info 公會暱稱"
        verbose_name_plural = "Info 4 公會暱稱"

class Info_roles(models.Model):
    guild_id = models.ForeignKey(Info_guild, on_delete=models.CASCADE, blank=True, null=True, verbose_name='公會')
    roles_id = models.IntegerField(verbose_name='身份組代碼')
    roles_name = models.CharField(max_length=100, null=True, verbose_name='身份組名稱')
    def __str__(self):
        return self.roles_name

    class Meta:
        verbose_name = "Info 公會身份組"
        verbose_name_plural = "Info 3 公會身份組"

class BotResponds(models.Model):
    info_id = models.AutoField(primary_key=True)
    keyword = models.CharField(max_length=20, verbose_name='觸發關鍵字')
    guild_id = models.ForeignKey(Info_guild, on_delete=models.CASCADE, blank=True, null=True, verbose_name='公會')
    author_id = models.ForeignKey(Info_author, on_delete=models.CASCADE, blank=True, null=True, verbose_name='角色')
    respond = models.TextField(max_length=500, help_text='respond', verbose_name='回應')
    update_time = models.DateTimeField(default=timezone.now, verbose_name='創建時間')
    def __str__(self):
        return self.keyword
    class Meta:
        verbose_name = "Bot 回應"
        verbose_name_plural = "Bot 4 回應"

class JoinGuildCipher(models.Model):
    guild_id = models.ForeignKey(Info_guild, on_delete=models.CASCADE, blank=True, null=True, verbose_name='公會')
    msg1 = models.TextField(max_length=100, null=True, blank=True, verbose_name='訊息1')
    msg2 = models.TextField(max_length=100, null=True, blank=True, verbose_name='訊息2')
    msg3 = models.TextField(max_length=100, null=True, blank=True, verbose_name='訊息3')
    msg4 = models.TextField(max_length=100, null=True, blank=True, verbose_name='訊息4')
    msg5 = models.TextField(max_length=100, null=True, blank=True, verbose_name='訊息5')
    def __str__(self):
        return self.guild_id.guild
    class Meta:
        verbose_name = "Bot 加入公會密語"
        verbose_name_plural = "Bot 3 加入公會密語"

class BotReactionRoles(models.Model):
    guild_id = models.ForeignKey(Info_guild, on_delete=models.CASCADE, blank=True, null=True, verbose_name='公會')
    msg_id = models.IntegerField(verbose_name='訊息代碼')
    emoji_id = models.IntegerField(null=True, verbose_name='表情符號代碼')
    emoji_name = models.CharField(max_length=5, null=True, verbose_name='表情符號名稱')
    roles_id = models.ForeignKey(Info_roles, on_delete=models.CASCADE, blank=True, null=True, verbose_name='權限名稱')
    def __str__(self):
        return self.guild_id.guild
    class Meta:
        verbose_name = "Bot 反應身份組"
        verbose_name_plural = "Bot 2 反應身份組"

class BotPermissionRoles(models.Model):
    guild_id = models.ForeignKey(Info_guild, on_delete=models.CASCADE, blank=True, null=True, verbose_name='公會')
    permission = models.ForeignKey(Info_roles, on_delete=models.CASCADE, blank=True, null=True, verbose_name='權限', related_name='permission')
    roles = models.ForeignKey(Info_roles, on_delete=models.CASCADE, blank=True, null=True, verbose_name='身份組')
    def __str__(self):
        return self.guild_id.guild

    class Meta:
        verbose_name = "Bot 權限身份組"
        verbose_name_plural = "Bot 1 權限身份組"

class Info_guildConfig(models.Model):
    guild_id = models.ForeignKey(Info_guild, on_delete=models.CASCADE, blank=True, null=True, verbose_name='公會')
    previou_is_valid = models.BooleanField(default=True, verbose_name='推齊', help_text='開啟推齊功能')
    respond_is_valid = models.BooleanField(default=True, verbose_name='回應', help_text='開啟回應功能')
    respond_only_guild = models.BooleanField(default=True, verbose_name='公會回應', help_text='只允許公會內教的')

    join_msg_is_valid = models.BooleanField(default=True, verbose_name='開啟進群通知', help_text='若無設定通知頻道有人進群時將自動關閉')
    join_guild_msg_channel = models.IntegerField(null=True, blank=True, verbose_name='進群的訊息頻道', help_text='設定進群通知頻道')

    leave_msg_is_valid = models.BooleanField(default=True, verbose_name='開啟離群通知', help_text='若無設定通知頻道有人離群時將自動關閉')
    leave_guild_msg_channel = models.IntegerField(null=True, blank=True, verbose_name='離群的訊息頻道', help_text='設定離群通知頻道')

    join_guild_cipher_is_valid = models.BooleanField(default=True, verbose_name='開啟進群密語', help_text='若無設定進群密語時將自動關閉')

    blackList_is_valid = models.BooleanField(default=False, verbose_name='開啟黑名單', help_text='後台控制')
    def __str__(self):
        return self.guild_id.guild
    class Meta:
        verbose_name = "Bot 控制中心"
        verbose_name_plural = "Bot 0 控制中心"

class BotHelloResponds(models.Model):
    respond = models.TextField(max_length=500, help_text='respond', verbose_name='回應')
    def __str__(self):
        return self.respond
    class Meta:
        verbose_name = "Bot 打招呼"
        verbose_name_plural = "Bot 5 打招呼"

class BotBlocklist(models.Model):
    update_time = models.DateTimeField(default=timezone.now, verbose_name='創建時間')
    guild_id = models.ForeignKey(Info_guild, on_delete=models.CASCADE, blank=True, null=True, help_text='舉發公會', verbose_name='公會')
    author = models.CharField(max_length=50, help_text='author name', verbose_name='角色名')
    explanation = models.TextField(max_length=500, help_text='事件說明', verbose_name='說明')
    def __str__(self):
        return self.author
    class Meta:
        verbose_name = "Bot 黑名單"
        verbose_name_plural = "Bot 6 黑名單"