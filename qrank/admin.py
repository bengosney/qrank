from django.contrib import admin

from .models import Match, Player, Game


class PlayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating']


class MatchAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'ranked']

class GameAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Match, MatchAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Game, GameAdmin)
