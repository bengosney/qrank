from django.core.management.base import BaseCommand, CommandError
from qrank.models import Player, Match, Game, Rank


class Command(BaseCommand):
    def handle(self, *args, **options):
        for r in Rank.objects.all():
            r.delete();

        for m in Match.objects.order_by('created_at'):
            m.rank(True)
