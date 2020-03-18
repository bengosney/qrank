from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

from trueskill import Rating, rate
from sortedm2m.fields import SortedManyToManyField

from django_extensions.db.fields import AutoSlugField


class Player(models.Model):
    START_SCORE = 100

    name = models.CharField(max_length=255, unique=True)

    slug = AutoSlugField(populate_from='name')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def played(self):
        return self.match_set.count

    @property
    def rating(self):
        return self.get_rating_for_game(None).rating

    def get_rating_for_game(self, game):
        rank = self.rank_set.filter(game=game).first()

        if rank is None:
            rank = Rank(player=self, game=game)
            rank.save()

        return rank

    def set_rating_for_game(self, game, rating):
        rank = self.get_rating_for_game(game)
        rank.rating = rating
        rank.save()


class Game(models.Model):
    name = models.CharField(max_length=255, unique=True)
    player_count = models.IntegerField()

    slug = AutoSlugField(populate_from='name')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.name


class Match(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    players = SortedManyToManyField(Player)
    ranked = models.BooleanField(default=False, editable=False)

    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.playerString} played {self.game} as {self.created_at}'

    @property
    def playerString(self):
        return ", ".join([str(p) for p in self.players.all()])

    def rank(self, force=False):
        if self.ranked and not force:
            return

        self.refresh_from_db()
        arg = []
        for player in self.players.all():
            arg.append((player.get_rating_for_game(self.game).rating_obj,))

        results = rate(arg)

        for i, player in enumerate(self.players.all()):
            rating = player.get_rating_for_game(self.game)
            rating.rating_obj = results[i]
            rating.match_count += 1
            rating.save()

            if self.game is not None:
                rating = player.get_rating_for_game(None)
                rating.rating_obj = results[i]
                rating.save()

        self.ranked = True
        self.save()


class Rank(models.Model):
    START_SCORE = 100

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=True, null=True)
    match_count = models.IntegerField(default=0)

    rating = models.FloatField(default=START_SCORE)

    @property
    def rating_obj(self):
        return Rating(self.rating)

    @rating_obj.setter
    def rating_obj(self, value):
        self.rating = value[0].mu


def on_transaction_commit(func):
    def inner(*args, **kwargs):
        transaction.on_commit(lambda: func(*args, **kwargs))

    return inner


@receiver(post_save, sender=Match)
@on_transaction_commit
def do_rank(sender, instance, created, **kwargs):
    instance.rank()
