from django.contrib import admin

from .models import Match, Player, Game


class PlayerAdmin(admin.ModelAdmin):
    list_display = ['name', ]


class MatchAdmin(admin.ModelAdmin):
    list_display = ['playerString', 'game', 'created_at', 'ranked']


class GameAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


admin.site.register(Match, MatchAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Game, GameAdmin)
