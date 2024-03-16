from django.http import Http404
from rest_framework import generics, permissions

from api.serializers import ReverseLeagueSerializer, GameSerializer, TeamSerializer, PlayerSerializer
from league.models import Game, Team, Player
from league.permissions import IsAtLeastPlayer, IsAtLeastCoach, TeamCoachOrAdmin, PlayersTeamCoachOrAdmin

class ReverseLeagueGameList(generics.RetrieveAPIView):
    '''
    Returns a tree-like object of all games in a league starting with the finals game
    '''
    serializer_class = ReverseLeagueSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsAtLeastPlayer
    ]

    def get_object(self):
        '''
        Set target object to the final game
        '''
        finals_game = Game.objects.filter(next_game__isnull=True)
        if finals_game.exists():
            return finals_game.get()
        else:
            raise Http404


class GameList(generics.ListAPIView):
    '''
    Returns a list of all games in a league
    '''
    serializer_class = GameSerializer
    http_method_names = ['get', 'options']
    permission_classes = [
        permissions.IsAuthenticated,
        IsAtLeastPlayer
    ]

    def get_queryset(self):
        return Game.objects.all()


# TODO: Could be deleted if no longer needed
class PlayerList(generics.ListAPIView):
    '''
    Returns a list of all players in a team
    '''
    serializer_class = PlayerSerializer
    http_method_names = ['get', 'options']
    permission_classes = [
        permissions.IsAuthenticated,
        IsAtLeastCoach
    ]

    def get_queryset(self):
        team_id = self.kwargs.get('team_id', None)
        if team_id is None:
            return Player.objects.all()
        else:
            return Player.objects.filter(team__id=team_id)


class TeamDetails(generics.RetrieveAPIView):
    '''
    Returns a team's details
    '''
    serializer_class = TeamSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        TeamCoachOrAdmin
    ]

    lookup_url_kwarg = 'team_id'
    queryset = Team.objects.all()


class PlayerDetails(generics.RetrieveAPIView):
    '''
    Returns a player's details
    '''
    serializer_class = PlayerSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        PlayersTeamCoachOrAdmin
    ]

    lookup_url_kwarg = 'player_id'
    queryset = Player.objects.all()
