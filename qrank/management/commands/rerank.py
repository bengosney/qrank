from django.core.management.base import BaseCommand, CommandError
from qrank.models import Player, Match, Game, Rank


class Command(BaseCommand):
    def handle(self, *args, **options):
        for p in Player.objects.all():
            r = p.get_rating_for_game(None)
            r.rating = Rank.START_SCORE
            r.save()

        for m in Match.objects.order_by('created_at'):
            m.rank(True)
