from django.db.models import Q
from rest_framework import serializers

from league.models import Game, Team, Player


class GameSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Game model
    '''
    team_a = serializers.ReadOnlyField(source='team_a.name')
    team_b = serializers.ReadOnlyField(source='team_b.name')
    team_a_pk = serializers.ReadOnlyField(source='team_a.pk')
    team_b_pk = serializers.ReadOnlyField(source='team_b.pk')

    class Meta:
        model = Game
        fields = [
            'pk',
            'team_a',
            'team_a_pk',
            'team_a_score',
            'team_b',
            'team_b_pk',
            'team_b_score']


class PlayerListingField(serializers.RelatedField):
    '''
    Custom class for listing players of a team
    '''
    def to_representation(self, value):
        return {
            'pk': value.pk,
            'name': value.name,
            'average_score': value.average_score,
            'total_games_played': value.total_games_played,
        }


class TeamSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Team model
    '''
    players = PlayerListingField(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ['name', 'average_score', 'players']


class PlayerSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Player model
    '''
    team = serializers.ReadOnlyField(source='team.name')

    class Meta:
        model = Player
        fields = ['team', 'name', 'average_score', 'total_games_played']


class GamesPerRoundSerializer(serializers.ListSerializer):
    '''
    Serializer for the League's game progression
    '''
    def __init__(self, *args, **kwargs):
        self.child = GameSerializer()
        super().__init__(*args, **kwargs)

    def to_representation(self, instance):
        # Games from first round
        games = instance.filter(next_game__isnull=True)

        league_games = []
        # Determine games from every round until finals
        while len(games) != 0:
            # Add current round's games to our list
            league_games.insert(0, GameSerializer(games, many=True).data)

            # Find all games in previous round
            prev_round = []
            for game in games:
                if game.previous_games.exists():
                    # We will specifically add team a's previous game first so that winners in previous games
                    # will follow the same order as the teams in the succeeding games

                    # Append previous game of team a
                    prev_round.append(
                        game.previous_games.filter(Q(team_a=game.team_a) | Q(team_b=game.team_a)).get()
                    )

                    # Append previous game of team b
                    prev_round.append(
                        game.previous_games.filter(Q(team_a=game.team_b) | Q(team_b=game.team_b)).get()
                    )

            # Treat previous round as our current round
            games = prev_round

        return league_games
