from django.test import TestCase

from api.serializers import GameSerializer, TeamSerializer, PlayerSerializer, GamesPerRoundSerializer
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
        test_game = Game.objects.create(
            team_a=team_a, team_a_score=100, team_b=team_b, team_b_score=110)  # Game with teams A and B
        Game.objects.bulk_create([
            Game(team_a=team_c, team_a_score=100, team_b=team_a, team_b_score=110),  # Game with teams C and A
            Game(team_a=team_b, team_a_score=100, team_b=team_c, team_b_score=110),  # Game with teams B and C
        ])

        # Query games from db then serialize
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)

        # Count should be the same
        self.assertEqual(games.count(), len(serializer.data))

        # Serialized data should have correct data fields:
        #  pk, team_a, team_a_pk, team_a_score, team_b, team_b_pk and team_b_score
        serializer = GameSerializer(test_game)
        self.assertEqual(test_game.pk, serializer.data.get('pk', None))
        self.assertEqual(test_game.team_a.name, serializer.data.get('team_a', None))
        self.assertEqual(test_game.team_a.pk, serializer.data.get('team_a_pk', None))
        self.assertEqual(test_game.team_a_score, serializer.data.get('team_a_score', None))
        self.assertEqual(test_game.team_b.name, serializer.data.get('team_b', None))
        self.assertEqual(test_game.team_b.pk, serializer.data.get('team_b_pk', None))
        self.assertEqual(test_game.team_b_score, serializer.data.get('team_b_score', None))

    def test_team_serializer(self):
        '''
        Player serializer should return correct count, names, average scores and total games played
        '''
        # Create teams
        team_a = Team.objects.create(name='Team A')
        Team.objects.create(name='Team B')
        Team.objects.create(name='Team C')

        # Create players
        player_a = Player.objects.create(team=team_a, name='Player A')
        player_b = Player.objects.create(team=team_a, name='Player B')

        # Query teams
        teams = Team.objects.all()

        # Serialize
        serializer = TeamSerializer(teams, many=True)

        # Team count should be the same
        self.assertEqual(teams.count(), len(serializer.data))

        # Team player count should be the same
        serialized_team = serializer = TeamSerializer(team_a)
        self.assertEqual(team_a.players.count(), len(serialized_team.data['players']))

        # Serialized data should have correct data fields:
        #  - name, average_score and players list
        #  - each item in players list should have pk, name average_score and total_games_played
        self.assertEqual(team_a.name, serialized_team.data.get('name', None))
        self.assertEqual(str(team_a.average_score), serialized_team.data.get('average_score', None))

        players = [
            {
                'pk': player_a.pk,
                'name': player_a.name,
                'average_score': player_a.average_score,
                'total_games_played': player_a.total_games_played,
            },
            {
                'pk': player_b.pk,
                'name': player_b.name,
                'average_score': player_b.average_score,
                'total_games_played': player_b.total_games_played,
            }
        ]
        self.assertListEqual(players, serialized_team.data.get('players', None))

    def test_player_serializer(self):
        '''
        Player serializer should return correct count, names, average scores and total games played
        '''
        # Create a team
        team = Team.objects.create(name='Team A')

        # Create players
        player_a = Player.objects.create(team=team, name='Player A')
        Player.objects.bulk_create([
            Player(team=team, name='Player B'),
            Player(team=team, name='Player C'),
        ])

        # Query players
        players = Player.objects.all()

        # Serialize
        serializer = PlayerSerializer(players, many=True)

        # Count should be the same
        self.assertEqual(players.count(), len(serializer.data))

        # Serialized data should have correct data fields:
        #  - team, team_pk, name, average_score, total_games_played
        serializer = PlayerSerializer(player_a)
        self.assertEqual(player_a.team.pk, serializer.data.get('team_pk', None))
        self.assertEqual(player_a.name, serializer.data.get('name', None))
        self.assertEqual(str(player_a.average_score), serializer.data.get('average_score', None))
        self.assertEqual(player_a.total_games_played, serializer.data.get('total_games_played', None))

    def test_games_per_round_serializer(self):
        '''
        Game serializer that maps all the games from all rounds.
         Returns lists of games from each round; one list per round starting from the first.
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
        serializer = GamesPerRoundSerializer(Game.objects.all())

        # Serialized data should be tree-like
        expected_data = [
            # First round
            [
                {
                    'pk': game_semi1.pk,
                    'team_a': game_semi1.team_a.name,
                    'team_a_pk': game_semi1.team_a.pk,
                    'team_a_score': game_semi1.team_a_score,
                    'team_b': game_semi1.team_b.name,
                    'team_b_pk': game_semi1.team_b.pk,
                    'team_b_score': game_semi1.team_b_score,
                },
                {
                    'pk': game_semi2.pk,
                    'team_a': game_semi2.team_a.name,
                    'team_a_pk': game_semi2.team_a.pk,
                    'team_a_score': game_semi2.team_a_score,
                    'team_b': game_semi2.team_b.name,
                    'team_b_pk': game_semi2.team_b.pk,
                    'team_b_score': game_semi2.team_b_score,
                }
            ],

            # Final round
            [
                {
                    'pk': game_final.pk,
                    'team_a': game_final.team_a.name,
                    'team_a_pk': game_final.team_a.pk,
                    'team_a_score': game_final.team_a_score,
                    'team_b': game_final.team_b.name,
                    'team_b_pk': game_final.team_b.pk,
                    'team_b_score': game_final.team_b_score
                }
            ]
        ]

        self.assertListEqual(serializer.data, expected_data)
