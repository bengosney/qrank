from django.core.management.base import BaseCommand, CommandError
from qrank.models import Player, Match


class Command(BaseCommand):
    def handle(self, *args, **options):
        for p in Player.objects.all():
            p.rating = Player.START_SCORE
            p.save()

        for m in Match.objects.order_by('created_at'):
            m.rank(True)
