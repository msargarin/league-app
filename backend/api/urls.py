from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from api.views import GamesPerRoundList, GameList, PlayerList, TeamDetails, PlayerDetails, AccessTokenGenerator


urlpatterns = [
    # Endpoint for access token generation
    path('token/access', AccessTokenGenerator.as_view(), name='access-token-generator'),
    path('token/refresh', TokenRefreshView.as_view(), name='token-refresh'),

    # Endpoint for reverse league games
    path('games/per-round', GamesPerRoundList.as_view(), name='games-per-round-list'),

    # Endpoint for games list
    path('games', GameList.as_view(), name='game-list'),

    # Endpoint for players list
    # TODO: Could be deleted if no longer needed
    path('players', PlayerList.as_view(), name='player-list'),  # Players from all teams
    path('players/team/<int:team_id>', PlayerList.as_view(), name='player-list'),  # Players from a specific team

    # Endpoint for team details
    path('team/<int:team_id>', TeamDetails.as_view(), name='team-details'),  # Players from a specific team

    # Endpoint for player details
    path('player/<int:player_id>', PlayerDetails.as_view(), name='player-details'),  # Players from a specific team
]
