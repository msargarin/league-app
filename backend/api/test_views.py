from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from league.models import Team, Game, Player

class APIEndpointsTest(APITestCase):
    def test_reverse_league_endpoint(self):
        '''
        There must be an endpoint that returns all games in a league in a tree-like format
        '''
        ## Test when database is empty
        # Send request
        url = reverse('league-list')
        response = self.client.get(url)

        # Response should be NOT FOUND
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        ## Test when database is populated
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

        # Send request
        url = reverse('league-list')
        response = self.client.get(url)

        # Response should be OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_game_list_endpoint(self):
        '''
        There must be an endpoint that returns all games as a list
        '''
        # NOTE: No need to test output since serializer has its own tests
        #  and the view has no new custom behaviour

        # Send request
        url = reverse('game-list')
        response = self.client.get(url)

        # Response should be OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_player_list_endpoint(self):
        '''
        There must be an endpoint that returns all players in a team as a list
        '''
        # Create teams
        team_a = Team.objects.create(name='Team A')
        team_b = Team.objects.create(name='Team B')

        # Create players
        Player.objects.bulk_create([
            Player(team=team_a, name='Player A'),
            Player(team=team_a, name='Player B'),
            Player(team=team_b, name='Player C'),
        ])

        # Test for all players in a team
        url = reverse('player-list', args=[team_a.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Response should be OK

        team_players = Player.objects.filter(team=team_a)
        self.assertEqual(
            len(response.data),
            team_players.count())  # Count from response should be the same from db

        # Test for all players regardless of team
        url = reverse('player-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Response should be OK

        all_players = Player.objects.all()
        self.assertEqual(
            len(response.data),
            all_players.count())  # Count from response should be the same from db

    def test_player_details_endpoint(self):
        '''
        There must be an endpoint that returns a player's details
        '''
        # Create team
        team = Team.objects.create(name='Team A')

        # Create player
        player = Player.objects.create(team=team, name='Player A')

        # Test endpoint
        url = reverse('player-details', args=[player.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Response should be OK
