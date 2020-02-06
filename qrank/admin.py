from django.contrib import admin

from .models import Match, Player


class PlayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating']


class GameAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'ranked']


admin.site.register(Match, GameAdmin)
admin.site.register(Player, PlayerAdmin)
