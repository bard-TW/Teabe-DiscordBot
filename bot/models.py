from django.db import models
from django.utils import timezone

# Create your models here.
# verbose_name 網頁上名稱
# help_text 網頁上註釋

class Info_guild(models.Model):
    guild = models.CharField(max_length=50, help_text='guild name', verbose_name='伺服器名')
    guild_id = models.IntegerField(help_text='guild id', verbose_name='伺服器代碼')
    def __str__(self):
        return self.guild

class Info_author(models.Model):
    author = models.CharField(max_length=50, help_text='author name', verbose_name='角色名')
    author_id = models.IntegerField(help_text='author id', verbose_name='角色代碼')
    def __str__(self):
        return self.author

class Info_guildNickname(models.Model):
    guild_id = models.ForeignKey(Info_guild, on_delete=models.CASCADE, blank=True, null=True, verbose_name='伺服器')
    author_id = models.ForeignKey(Info_author, on_delete=models.CASCADE, blank=True, null=True, verbose_name='角色')
    nickname = models.CharField(max_length=50, verbose_name='伺服器角色名', help_text='在伺服器裡的角色暱稱')
    def __str__(self):
        return self.nickname

class BotResponds(models.Model):
    info_id = models.AutoField(primary_key=True)
    keyword = models.CharField(max_length=20, verbose_name='觸發關鍵字')
    guild_id = models.ForeignKey(Info_guild, on_delete=models.CASCADE, blank=True, null=True, verbose_name='伺服器')
    author_id = models.ForeignKey(Info_author, on_delete=models.CASCADE, blank=True, null=True, verbose_name='角色')
    respond = models.TextField(max_length=500, help_text='respond', verbose_name='回應')
    update_time = models.DateTimeField(default=timezone.now, verbose_name='創建時間')
    def __str__(self):
        return self.keyword

class Info_guildConfig(models.Model):
    guild_id = models.ForeignKey(Info_guild, on_delete=models.CASCADE, blank=True, null=True, verbose_name='伺服器')
    previou_is_valid = models.BooleanField(default=True, verbose_name='推齊', help_text='是否開啟推齊功能')
    respond_is_valid = models.BooleanField(default=True, verbose_name='回應', help_text='是否開啟回應功能')
    respond_only_guild = models.BooleanField(default=True, verbose_name='公會回應', help_text='是否只說公會內教的')

    # join_guild_msg_channel = models.IntegerField(help_text='channel id', verbose_name='加入伺服器訊息頻道')
    # leave_guild_msg_channel = models.IntegerField(help_text='channel id', verbose_name='離開伺服器訊息頻道')

    def __str__(self):
        return self.guild_id.guild

class BotHelloResponds(models.Model):
    respond = models.TextField(max_length=500, help_text='respond', verbose_name='回應')
    def __str__(self):
        return self.respond

class JoinGuildMsg(models.Model):
    guild_id = models.ForeignKey(Info_guild, on_delete=models.CASCADE, blank=True, null=True, verbose_name='伺服器')
    msg1 = models.TextField(max_length=100, null=True, verbose_name='訊息1')
    msg2 = models.TextField(max_length=100, null=True, verbose_name='訊息2')
    msg3 = models.TextField(max_length=100, null=True, verbose_name='訊息3')
    msg4 = models.TextField(max_length=100, null=True, verbose_name='訊息4')
    msg5 = models.TextField(max_length=100, null=True, verbose_name='訊息5')

    def __str__(self):
        return self.guild_id.guild