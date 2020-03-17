from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import CreateView
from django.urls import reverse
from django.db.models import Count

from .models import Player, Match, Game, Rank


class GameListView(ListView):
    model = Game


class PlayerListView(ListView):
    model = Rank

    def get_game(self):
        if 'game' in self.kwargs:
            return Game.objects.get(slug=self.kwargs['game'])

        return None

    def get_queryset(self):
        qs = super().get_queryset()

        game = self.get_game()
        if game is not None:
            qs = qs.filter(game=game)
        else:
            qs = qs.filter(game__isnull=True)

        return qs#.annotate(num_matches=Count('match')).filter(num_matches__gt=0)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['game'] = self.get_game()

        return context


class GameDetailsView(ListView):
    model = Player

    def get_queryset(self):
        return super().get_queryset().annotate(num_matches=Count('match')).filter(num_matches__gt=0)


class PlayerCreateView(CreateView):
    model = Player
    fields = ('name',)

    def get_success_url(self):
        return reverse('player_list')


class GameCreateView(CreateView):
    model = Match
    fields = ('players',)