from rest_framework import serializers

from league.models import Game, Team, Player


class GameSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Game model
    '''
    team_a = serializers.ReadOnlyField(source='team_a.name')
    team_b = serializers.ReadOnlyField(source='team_b.name')
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
        games = instance.filter(previous_games__isnull=True)

        league_games = []
        # Determine games from every round until finals
        while len(games) != 0:
            # Add current round's games to our list
            league_games.append(GameSerializer(games, many=True).data)

            # Find all games in next round
            next_round = []
            for game in games:
                if game.next_game is not None and game.next_game not in next_round:
                    next_round.append(game.next_game)

            # Treat next round as our current round
            games = next_round

        return league_games
