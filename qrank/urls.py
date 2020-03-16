from django.urls import path

from .views import PlayerListView, PlayerCreateView, GameCreateView, AddMatchView

urlpatterns = [
    path('add-match/<slug:game>/', AddMatchView.as_view(), name='add_match'),
    path('<slug:game>/', PlayerListView.as_view(), name='player_list'),
    path('create/', PlayerCreateView.as_view(), name='player_create'),
    path('add-game/', GameCreateView.as_view(), name='game_create'),
    path('', PlayerListView.as_view(), name='player_list'),
]


