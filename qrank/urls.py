from django.urls import path

from .views import PlayerListView

urlpatterns = [
    path('', PlayerListView.as_view(), name='player_list'),
]
