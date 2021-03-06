from django.urls import path

from .views import PlayerListView, PlayerCreateView, GameCreateView, AddMatchView, GameListView

urlpatterns = [
    path('add-match/<slug:game>/', AddMatchView.as_view(), name='add_match'),
    path('create/', PlayerCreateView.as_view(), name='player_create'),
    path('<slug:game>/', PlayerListView.as_view(), name='player_list'),
    path('add-game/', GameCreateView.as_view(), name='game_create'),
    path('', GameListView.as_view(), name='game_list'),
]


