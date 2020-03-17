from django.urls import path

from .views import PlayerListView, PlayerCreateView, GameCreateView, GameListView

urlpatterns = [
    path('', GameListView.as_view(), name='game_list'),
    path('<slug:game>/', PlayerListView.as_view(), name='player_list'),
    path('create/', PlayerCreateView.as_view(), name='player_create'),
    path('add-game/', GameCreateView.as_view(), name='game_create'),
]
