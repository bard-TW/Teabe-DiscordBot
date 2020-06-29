from django.contrib import admin

from .models import BotResponds, Info_guild, Info_author, Info_guildNickname, Info_guildConfig, BotHelloResponds, JoinGuildMsg
# Register your models here.


class BotRespondsAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'respond', 'guild_id', 'author_id', 'update_time')
    list_filter = ('guild_id', 'author_id')  # 塞選條件
    fields = ['keyword', ('guild_id', 'author_id'), 'respond', 'update_time']  # django編輯的排版
admin.site.register(BotResponds, BotRespondsAdmin)


class Info_guildAdmin(admin.ModelAdmin):
    list_display = ('guild_id', 'guild')
admin.site.register(Info_guild, Info_guildAdmin)


class Info_authorAdmin(admin.ModelAdmin):
    list_display = ('author_id', 'author')
admin.site.register(Info_author, Info_authorAdmin)


class Info_guildNicknameAdmin(admin.ModelAdmin):
    list_display = ('guild_id', 'author_id', 'nickname')
admin.site.register(Info_guildNickname, Info_guildNicknameAdmin)


class Info_guildConfigAdmin(admin.ModelAdmin):
    list_display = ('guild_id', 'previou_is_valid', 'respond_is_valid', 'respond_only_guild')
admin.site.register(Info_guildConfig, Info_guildConfigAdmin)


class BoTHelloRespondsAdmin(admin.ModelAdmin):
    list_display = ('respond',)
admin.site.register(BotHelloResponds, BoTHelloRespondsAdmin)

class JoinGuildMsgAdmin(admin.ModelAdmin):
    list_display = ('guild_id', 'msg1', 'msg2', 'msg3', 'msg4', 'msg5')

admin.site.register(JoinGuildMsg, JoinGuildMsgAdmin)