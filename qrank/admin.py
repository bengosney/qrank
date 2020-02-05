from django.contrib import admin

from .models import Game, Player, Played


class PlayerAdmin(admin.ModelAdmin):
    pass


class PlayedAdmin(admin.TabularInline):
    model = Played


class GameAdmin(admin.ModelAdmin):
    inlines = [PlayedAdmin, ]
    list_display = ['created_at', 'player1', 'player2', 'player3', 'player4']


admin.site.register(Game, GameAdmin)
admin.site.register(Player, PlayerAdmin)
