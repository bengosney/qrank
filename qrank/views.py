from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import CreateView
from django.urls import reverse
from django.db.models import Count

from .models import Player, Match


class PlayerListView(ListView):
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