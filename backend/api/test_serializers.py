from django.test import TestCase

from api.serializers import GameSerialier, TeamSerializer, PlayerSerializer, ReverseLeagueSerializer
from league.models import Team, Game, Player


class APISerializerTests(TestCase):
    def test_game_serializer(self):
        '''
        Game serializer should return correct count, team names and scores
        '''
        # Create teams
        team_a = Team.objects.create(name='Team A')
        team_b = Team.objects.create(name='Team B')
        team_c = Team.objects.create(name='Team C')

        # Create games
        Game.objects.bulk_create([
            Game(team_a=team_a, team_a_score=100, team_b=team_b, team_b_score=110),  # Game with teams A and B
            Game(team_a=team_c, team_a_score=100, team_b=team_a, team_b_score=110),  # Game with teams C and A
            Game(team_a=team_b, team_a_score=100, team_b=team_c, team_b_score=110),  # Game with teams B and C
        ])

        # Query games
        games = Game.objects.all()

        # Serialize
        serializer = GameSerialier(games, many=True)

        # Count should be the same
        self.assertEqual(games.count(), len(serializer.data))

        # Serialized data should have team_a, team_a_score, team_b and team_b_score keys
        self.assertIn('team_a', serializer.data[0])
        self.assertIn('team_a_score', serializer.data[0])
        self.assertIn('team_b', serializer.data[0])
        self.assertIn('team_b_score', serializer.data[0])

    def test_team_serializer(self):
        '''
        Player serializer should return correct count, names, average scores and total games played
        '''
        # Create teams
        team_a = Team.objects.create(name='Team A')
        Team.objects.create(name='Team B')
        Team.objects.create(name='Team C')

        # Create players
        Player.objects.bulk_create([
            Player(team=team_a, name='Player A'),
            Player(team=team_a, name='Player B'),
        ])

        # Query teams
        teams = Team.objects.all()

        # Serialize
        serializer = TeamSerializer(teams, many=True)

        # Team count should be the same
        self.assertEqual(teams.count(), len(serializer.data))

        # Team player count should be the same
        serialized_team = serializer = TeamSerializer(team_a)
        self.assertEqual(team_a.players.count(), len(serialized_team.data['players']))

        # Serialized data should have name, average_score and players keys
        self.assertIn('name', serialized_team.data)
        self.assertIn('average_score', serialized_team.data)
        self.assertIn('players', serialized_team.data)

    def test_player_serializer(self):
        '''
        Player serializer should return correct count, names, average scores and total games played
        '''
        # Create a team
        team = Team.objects.create(name='Team A')

        # Create players
        Player.objects.bulk_create([
            Player(team=team, name='Player A'),
            Player(team=team, name='Player B'),
            Player(team=team, name='Player C'),
        ])

        # Query players
        players = Player.objects.all()

        # Serialize
        serializer = PlayerSerializer(players, many=True)

        # Count should be the same
        self.assertEqual(players.count(), len(serializer.data))

        # Serialized data should have team, average_score and total_games_played keys
        self.assertIn('team', serializer.data[0])
        self.assertIn('average_score', serializer.data[0])
        self.assertIn('total_games_played', serializer.data[0])

    def test_reverse_league_serializer(self):
        '''
        Game serializer that maps all the games from the finals to the first qualifying round.
         Returns a tree-like structure with the finals game at the top and the first qualifying
         round games at the bottom.
        '''
        # Create teams
        team_a = Team.objects.create(name='Team A')
        team_b = Team.objects.create(name='Team B')
        team_c = Team.objects.create(name='Team C')
        team_d = Team.objects.create(name='Team D')

        # Create games
        game_semi1 = Game.objects.create(
            team_a=team_a, team_a_score=110,
            team_b=team_b, team_b_score=100)  # Semi-finals game with teams A and B; A won
        game_semi2 = Game.objects.create(
            team_a=team_c, team_a_score=110,
            team_b=team_d, team_b_score=100)  # Semi-finals game with teams C and D; C won
        game_final = Game.objects.create(
            team_a=team_a, team_a_score=110,
            team_b=team_c, team_b_score=100)  # Finals game with teams A and C; A won

        # Link final game to semi-final games
        game_final.previous_games.add(game_semi1)
        game_final.previous_games.add(game_semi2)

        # Serialize starting with the finals game
        serializer = ReverseLeagueSerializer(game_final)

        # Serialized data should be tree-like
        expected_data = {
            'team_a': game_final.team_a.name,
            'team_a_score': game_final.team_a_score,
            'team_b': game_final.team_b.name,
            'team_b_score': game_final.team_b_score,
            'previous_games': [
                {
                    'team_a': game_semi1.team_a.name,
                    'team_a_score': game_semi1.team_a_score,
                    'team_b': game_semi1.team_b.name,
                    'team_b_score': game_semi1.team_b_score,
                    'previous_games': [],
                },
                {
                    'team_a': game_semi2.team_a.name,
                    'team_a_score': game_semi2.team_a_score,
                    'team_b': game_semi2.team_b.name,
                    'team_b_score': game_semi2.team_b_score,
                    'previous_games': [],
                }
            ]
        }

        self.assertDictEqual(serializer.data, expected_data)
