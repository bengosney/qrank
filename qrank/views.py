from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import CreateView
from django.views.generic.edit import FormView
from django.http import Http404

from django.urls import reverse
from django.db.models import Count

from .forms import MatchAddForm

from .models import Player, Match, Game, Rank
from django.contrib.auth.mixins import LoginRequiredMixin


class GameListView(LoginRequiredMixin, ListView):
    model = Game


class PlayerListView(ListView):
    model = Rank

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
            qs = qs.filter(game=game)
        else:
            qs = qs.filter(game__isnull=True)

        return qs.filter(match_count__gt=0)

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
    form_class = MatchAddForm
    template_name = 'qrank/add_match.html'

    def get_game(self):
        try:
            return Game.objects.get(slug=self.kwargs['game'])
        except Game.DoesNotExist:
            raise Http404("Game does not exist")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['game'] = self.get_game()

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['game'] = self.get_game()

        return kwargs

    def form_valid(self, form):
        match = Match()
        match.game = form.get_game()
        match.save()

        places = form.get_places()

        for player in places:
            match.players.add(player)

        match.save()

        return super().form_valid(form)

    def get_success_url(self):
        return self.get_game().url