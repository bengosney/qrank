from django.contrib import admin

from .models import Game, Player


class PlayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating']


class GameAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'ranked']


admin.site.register(Game, GameAdmin)
admin.site.register(Player, PlayerAdmin)
