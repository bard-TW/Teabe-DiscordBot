from django.contrib import admin

from .models import BotResponds, Info_guild, Info_author, Info_guildNickname, Info_guildConfig, BotHelloResponds
from .models import JoinAndLeaveGuild, BotReactionRoles, Info_roles, BotPermissionRoles, BotBlocklist
# Register your models here.


class BotRespondsAdmin(admin.ModelAdmin):
    list_display = ('guild_id', 'author_id', 'update_time', 'keyword', 'respond')
    list_filter = ('guild_id', 'author_id')  # 塞選條件
    fields = ['keyword', ('guild_id', 'author_id'), 'respond', 'update_time']  # django編輯的排版
admin.site.register(BotResponds, BotRespondsAdmin)


class Info_guildAdmin(admin.ModelAdmin):
    list_display = ('guild_id', 'guild', 'remark')
admin.site.register(Info_guild, Info_guildAdmin)


class Info_authorAdmin(admin.ModelAdmin):
    list_display = ('author_id', 'author')
admin.site.register(Info_author, Info_authorAdmin)


class Info_guildNicknameAdmin(admin.ModelAdmin):
    list_display = ('guild_id', 'author_id', 'nickname')
admin.site.register(Info_guildNickname, Info_guildNicknameAdmin)


class Info_rolesAdmin(admin.ModelAdmin):
    list_display = ('guild_id', 'roles_id', 'roles_name')
admin.site.register(Info_roles, Info_rolesAdmin)


class Info_guildConfigAdmin(admin.ModelAdmin):
    list_display = ('guild_id', 'previou_is_valid', 'respond_is_valid', 'respond_only_guild', 'join_msg_is_valid', 
                    'join_guild_msg_channel', 'leave_msg_is_valid', 'leave_guild_msg_channel', 'join_guild_cipher_is_valid',
                    'blackList_is_valid')
    fields = ['guild_id', 
            ('previou_is_valid', 'respond_is_valid', 'respond_only_guild', 'join_guild_cipher_is_valid'), 
            ('join_msg_is_valid', 'join_guild_msg_channel'), 
            ('leave_msg_is_valid', 'leave_guild_msg_channel'),
            ('blackList_is_valid')]  # django編輯的排版
admin.site.register(Info_guildConfig, Info_guildConfigAdmin)


class BoTHelloRespondsAdmin(admin.ModelAdmin):
    list_display = ('respond',)
admin.site.register(BotHelloResponds, BoTHelloRespondsAdmin)


class JoinAndLeaveGuildAdmin(admin.ModelAdmin):
    list_display = ('guild_id', 'joinGuildCipher1', 'joinGuildCipher2', 'joinGuildCipher3', 'joinGuildCipher4', 'joinGuildCipher5',
                    'joinGuildTitle', 'joinGuildDscription', 'leaveGuildTitle', 'leaveGuildDescription')
admin.site.register(JoinAndLeaveGuild, JoinAndLeaveGuildAdmin)


class BotReactionRolesAdmin(admin.ModelAdmin):
    list_display = ('guild_id', 'msg_id', 'emoji_id', 'emoji_name', 'roles_id')
    list_filter = ('guild_id',)  # 塞選條件
admin.site.register(BotReactionRoles, BotReactionRolesAdmin)


class BotPermissionRolesAdmin(admin.ModelAdmin):
    list_display = ('guild_id', 'permission', 'roles')
    list_filter = ('guild_id',)  # 塞選條件
admin.site.register(BotPermissionRoles, BotPermissionRolesAdmin)


class BotBlocklistAdmin(admin.ModelAdmin):
    list_display = ('author', 'guild_id', 'update_time', 'explanation')
    fields = [('guild_id', 'update_time'), 'author', 'explanation']  # django編輯的排版
    list_filter = ('guild_id',)  # 塞選條件
admin.site.register(BotBlocklist, BotBlocklistAdmin)