import random

from django.http import Http404
from rest_framework import generics, permissions
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView

from api.serializers import ReverseLeagueSerializer, GameSerializer, TeamSerializer, PlayerSerializer
from league.models import Game, Team, Player, Coach
from league.permissions import (
    IsAtLeastPlayer, IsAtLeastCoach, TeamCoachOrAdmin, PlayersTeamCoachOrAdmin, ACCOUNT_LEVEL_ADMIN,
    ACCOUNT_LEVEL_COACH, ACCOUNT_LEVEL_PLAYER)

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


class AccessTokenGenerator(APIView):
    '''
    Returns a dummy access token based on requested role which can be used for authorization
    '''
    authentication_classes = []  # Override default authentication
    permission_classes = []  # Override default permissions
    http_method_names = ['post']

    def post(self, request, format=None):
        '''
        Returns an access token with claims matching the provided role
        '''
        if 'role' not in request.data:
            raise ParseError(detail='Role not provided in payload')
        else:
            role = request.data['role']
            if role == ACCOUNT_LEVEL_ADMIN:
                name = 'Mike A'
                team = None
            elif role == ACCOUNT_LEVEL_COACH:
                coach = random.choice(Coach.objects.select_related().all())
                name = coach.name
                team = coach.team.name
            elif role == ACCOUNT_LEVEL_PLAYER:
                player = random.choice(Player.objects.select_related().all())
                name = player.name
                team = player.team.name
            else:
                raise ParseError(detail='Specified role is unrecognized')

        user = TokenUser({
            'user_id': '{}/{}'.format(name, role),
            'name': name,
            'team': team,
            'role': role,
        })
        token = AccessToken.for_user(user)

        return Response({
            'status': 200,
            'name': name,
            'team': team,
            'role': role,
            'access_token': str(token),
        })
