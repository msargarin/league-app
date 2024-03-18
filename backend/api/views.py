import random

from rest_framework import generics, permissions
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

from api.serializers import GamesPerRoundSerializer, TeamSerializer, PlayerSerializer
from league.models import Game, Team, Player, Coach
from league.permissions import (
    IsAtLeastPlayer, IsAtLeastCoach, TeamCoachOrAdmin, PlayersTeamCoachOrAdmin, ACCOUNT_LEVEL_ADMIN,
    ACCOUNT_LEVEL_COACH, ACCOUNT_LEVEL_PLAYER)

class GamesPerRoundList(APIView):
    '''
    Returns lists of games grouped per round
    '''
    permission_classes = [
        permissions.IsAuthenticated,
        IsAtLeastPlayer
    ]
    def get(self, request, format=None):
        return Response(GamesPerRoundSerializer(Game.objects.all()).data)


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
            # Set correct token payload based on requested role
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

        # Create dummy user and tokens based on token payload
        user = TokenUser({
            'user_id': '{}/{}'.format(name.replace(' ', ''), role),
        })
        refresh_token = RefreshToken.for_user(user)
        refresh_token['name'] = name
        refresh_token['team'] = team
        refresh_token['role'] = role

        return Response({
            'status': 200,
            'name': name,
            'team': team,
            'role': role,
            'access_token': str(refresh_token.access_token),
            'refresh_token': str(refresh_token),
        })
