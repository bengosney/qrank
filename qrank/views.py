from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import CreateView
from django.urls import reverse


from .models import Player, Game


class PlayerListView(ListView):
    model = Player


class PlayerCreateView(CreateView):
    model = Player
    fields = ('name',)

    def get_success_url(self):
        return reverse('player_list')


class GameCreateView(CreateView):
    model = Game
    fields = ('players',)