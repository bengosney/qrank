from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import CreateView
from django.views.generic.edit import FormView
from django.http import Http404


from django.urls import reverse
from django.db.models import Count

from .forms import NameForm
from .models import Player, Match, Game


class PlayerListView(ListView):
    model = Player

    def get_game(self):
        if 'game' in self.kwargs:
            try:
                return Game.objects.get(slug=self.kwargs['game'])
            except Game.DoesNotExist:
                pass

        return None

    def get_queryset(self):
        qs = super().get_queryset()

        game = self.get_game()
        if game is not None:
            qs = qs.filter(match__game=game)

        return qs.annotate(num_matches=Count('match')).filter(num_matches__gt=0)

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


class AddMatchView(FormView):
    form_class = NameForm
    template_name = 'qrank/add_match.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['game'] = Game.objects.get(slug=self.kwargs['game'])
        except Game.DoesNotExist:
            raise Http404("Game does not exist")

        return context
