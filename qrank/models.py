from django.db import models

from trueskill import Rating, rate
from sortedm2m.fields import SortedManyToManyField


class Player(models.Model):
    name = models.CharField(max_length=255)
    rating = models.IntegerField(default=25)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.name

    @property
    def rating_obj(self):
        return Rating(self.rating)

    @rating_obj.setter
    def rating_obj(self, value):
        self.rating = value[0].mu


class Game(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    players = SortedManyToManyField(Player)

    def __str__(self):
        return f'Played at {self.created_at}'

    def save(self, *args, **kwargs):
        adding = self._state.adding
        ret = super().save(*args, **kwargs)

        if adding:
            self.rank()

        return ret

    def rank(self):
        self.refresh_from_db()
        arg = []
        for player in self.players.all():
            arg.append((player.rating_obj,))

        results = rate(arg)

        for i, player in enumerate(self.players.all()):
            player.rating_obj = results[i]
            player.save()
