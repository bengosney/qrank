from django.urls import path

from .views import PlayerListView, PlayerCreateView, GameCreateView

urlpatterns = [
    path('', PlayerListView.as_view(), name='player_list'),
    path('create/', PlayerCreateView.as_view(), name='player_create'),
    path('add-game/', GameCreateView.as_view(), name='game_create'),
]
