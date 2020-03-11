from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

from trueskill import Rating, rate
from sortedm2m.fields import SortedManyToManyField


class Player(models.Model):
    START_SCORE = 100

    name = models.CharField(max_length=255, unique=True)
    rating = models.FloatField(default=START_SCORE)

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


class Game(models.Model):
    name = models.CharField(max_length=255, unique=True)
    player_count = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)


    def __str__(self):
        return self.name


class Match(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    players = SortedManyToManyField(Player)
    ranked = models.BooleanField(default=False, editable=False)

    game = models.ForeignKey(Game, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'Played at {self.created_at}'

    def save(self, *args, **kwargs):
        adding = self._state.adding
        ret = super().save(*args, **kwargs)

        if adding and False:
            self.rank()

        return ret

    def rank(self, force=False):
        if self.ranked and not force:
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
    

class PlayerRanks(models.Model):
    START_SCORE = 100
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    rating = models.FloatField(default=START_SCORE)

    
def on_transaction_commit(func):
    def inner(*args, **kwargs):
        transaction.on_commit(lambda: func(*args, **kwargs))

    return inner


@receiver(post_save, sender=Match)
@on_transaction_commit
def do_rank(sender, instance, created, **kwargs):
    instance.rank()
