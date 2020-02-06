from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

from trueskill import Rating, rate
from sortedm2m.fields import SortedManyToManyField


class Player(models.Model):
    name = models.CharField(max_length=255, unique=True)
    rating = models.IntegerField(default=25)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['-rating', 'name']

    def __str__(self):
        return self.name

    @property
    def played(self):
        return self.match_set.count

    @property
    def rating_obj(self):
        return Rating(self.rating)

    @rating_obj.setter
    def rating_obj(self, value):
        self.rating = value[0].mu


class Match(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    players = SortedManyToManyField(Player)
    ranked = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return f'Played at {self.created_at}'

    def save(self, *args, **kwargs):
        adding = self._state.adding
        ret = super().save(*args, **kwargs)

        if adding and False:
            self.rank()

        return ret

    def rank(self):
        if self.ranked:
            return

        self.refresh_from_db()
        arg = []
        for player in self.players.all():
            arg.append((player.rating_obj,))

        results = rate(arg)

        for i, player in enumerate(self.players.all()):
            player.rating_obj = results[i]
            player.save()

        self.ranked = True
        self.save()


def on_transaction_commit(func):
    def inner(*args, **kwargs):
        transaction.on_commit(lambda: func(*args, **kwargs))

    return inner


@receiver(post_save, sender=Match)
@on_transaction_commit
def do_rank(sender, instance, created, **kwargs):
    instance.rank()
