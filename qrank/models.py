from django.db import models

from trueskill import Rating, rate


class Player(models.Model):
    name = models.CharField(max_length=255)
    rating = models.IntegerField(default=25)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.name

    @property
    def ratingObj(self):
        return Rating(self.rating)

    @ratingObj.setter
    def ratingObj(self, value):
        self.rating = value[0].mu


class Game(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player1', null=True, blank=True)
    player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player2', null=True, blank=True)
    player3 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player3', null=True, blank=True)
    player4 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player4', null=True, blank=True)

    players = models.ManyToManyField(Player, through='Played')

    def __str__(self):
        return f'Played at {self.created_at}'

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.rank()

        super().save(*args, **kwargs)

    def rank(self):
        arg = [
            (self.player1.ratingObj,),
            (self.player2.ratingObj,),
            (self.player3.ratingObj,),
            (self.player4.ratingObj,),
        ]

        r1, r2, r3, r4 = rate(arg)

        self.player1.ratingObj = r1
        self.player2.ratingObj = r2
        self.player3.ratingObj = r3
        self.player4.ratingObj = r4

        self.player1.save()
        self.player2.save()
        self.player3.save()
        self.player4.save()


class Played(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
