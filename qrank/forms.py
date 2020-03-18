import math
from django import forms

from .models import Game, Player


def ordinal(n):
    return "%d%s" % (n, "tsnrhtdd"[(math.floor(n / 10) % 10 != 1) * (n % 10 < 4) * n % 10::4])


class MatchAddForm(forms.Form):
    game = forms.ModelChoiceField(label='Game', queryset=Game.objects.all(), disabled=True)

    def __init__(self, game, *args, **kwargs):
        kwargs['initial']['game'] = game.pk
        super().__init__(*args, **kwargs)

        for i in range(game.player_count):
            label = f"{ordinal(i + 1)} place"
            self.fields[f"place_{i}"] = forms.ModelChoiceField(queryset=Player.objects.all(), label=label)
