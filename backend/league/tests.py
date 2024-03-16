from django.core.management import call_command
from django.core.management.base import CommandError
from django.db.models import Q
from django.test import TestCase

from league.models import Team, Game, Coach, Player


class ModelTests(TestCase):
    def test_game_different_teams(self):
        '''
        A game must always involve different teams
        '''
        # Create a team
        team_a = Team.objects.create(name='Team A')

        # Creating a game with only 1 team should raise an error
        with self.assertRaises(ValueError):
            Game.objects.create(
                team_a=team_a,
                team_b=team_a)

    def test_game_no_tie(self):
        '''
        A game must always have a winner (ie. there are no tied games in basketball)
        '''
        # Create teams
        team_a = Team.objects.create(name='Team A')
        team_b = Team.objects.create(name='Team B')

        # Creating a game with teams A and B ending in a tie should raise an error
        with self.assertRaises(ValueError):
            same_score = 100
            Game.objects.create(
                team_a=team_a,
                team_a_score=same_score,
                team_b=team_b,
                team_b_score=same_score)

    def test_game_winner(self):
        '''
        Winner in a game is the team with most points
        '''
        # Create teams
        team_a = Team.objects.create(name='Team A')
        team_b = Team.objects.create(name='Team B')

        # Creating a game with teams A and B and with A having more points
        game = Game.objects.create(
            team_a=team_a,
            team_a_score=110,
            team_b=team_b,
            team_b_score=100)
        self.assertEqual(game.get_winning_team(), team_a)  # Team A wins

    def test_team_list_games(self):
        '''
        A team's games must be enumerable
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

        # Team has a games parameter that returns all of their games
        self.assertTrue(hasattr(team_a, 'get_games'))
        self.assertQuerySetEqual(
            Game.objects.filter(Q(team_a=team_a) | Q(team_b=team_a)),
            team_a.get_games(),
            ordered=False)


class CommandTest(TestCase):
    '''
    Tests for Django Commands
    '''
    def test_populate_database_command(self):
        call_command('populate_database', *[], **{})

        # Should have created 16 teams
        self.assertEqual(Team.objects.count(), 16)

        # Should have created 16 coaches
        self.assertEqual(Coach.objects.count(), 16)

        # Should have created 160 players (16 * 10)
        self.assertEqual(Player.objects.count(), 160)

        # Should have created 15 games (8 + 4 + 2 + 1)
        self.assertEqual(Game.objects.count(), 15)

        # Should show an error if there is data available
        with self.assertRaises(CommandError):
             call_command('populate_database', *[], **{})
