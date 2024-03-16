from rest_framework import serializers

from league.models import Game, Team, Player


class GameSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Game model
    '''
    class Meta:
        model = Game
        fields = ['team_a', 'team_a_score', 'team_b', 'team_b_score']


class PlayerListingField(serializers.RelatedField):
    '''
    Custom class for listing players of a team
    '''
    def to_representation(self, value):
        return value.name


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
        fields = ['team', 'average_score', 'total_games_played']


class ReverseLeagueSerializer(serializers.ModelSerializer):
    '''
    Serializer for the League's game progression
    '''
    team_a = serializers.ReadOnlyField(source='team_a.name')
    team_b = serializers.ReadOnlyField(source='team_b.name')
    previous_games = serializers.SerializerMethodField("get_previous_games")

    def get_previous_games(self, obj):
        if obj.previous_games.exists():
            serializer = self.__class__(obj.previous_games.all(), many=True)
            return serializer.data
        else:
            return []

    class Meta:
        model = Game
        fields = ['team_a', 'team_a_score', 'team_b', 'team_b_score', 'previous_games']
