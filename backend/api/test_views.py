from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.tokens import Token


from league.models import Team, Game, Player


class APIEndpointsTest(APITestCase):
    def setUp(self):
        # Create TokenUsers of different user types so they are available across all test in this test class
        self.admin_user = TokenUser({
            'name': 'John Doe',
            'role': 'admin',
            'team': None,
        })  # Admin user
        self.player_user = TokenUser({
            'name': 'John Doe',
            'role': 'player',
            'team': 'Team Hello',
        })  # Player user
        self.coach_user = TokenUser({
            'name': 'John Doe',
            'role': 'coach',
            'team': 'Team Hello',
        })  # Coach user

    def test_reverse_league_endpoint(self):
        '''
        There must be an endpoint that returns all games in a league in a tree-like format
        '''
        # Authenticate using a player user since players have lowest level of access
        self.client.force_authenticate(user=self.player_user)


        ## Test with empty database

        # Send request
        url = reverse('league-list')
        response = self.client.get(url)

        # Response should be NOT FOUND
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


        ## Test with populated database

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
        #  and the view has no custom behaviour

        # Authenticate using a player user since players have lowest access access
        self.client.force_authenticate(user=self.player_user)

        # Send request
        url = reverse('game-list')
        response = self.client.get(url)

        # Response should be OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_player_list_endpoint(self):
        '''
        There must be an endpoint that returns players as a list
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

        # Send request using a player user
        self.client.force_authenticate(user=self.player_user)
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN)  # Response should be FORBIDDEN since players have no access

        # Send request using a coach user
        self.client.force_authenticate(user=self.coach_user)
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK)  # Response should be OK

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

    def test_team_details_endpoint(self):
        '''
        There must be an endpoint that returns a team's details
        '''
        # Authenticate using a coach user since coaches have lowest level of access
        self.client.force_authenticate(user=self.coach_user)

        # Create team
        team = Team.objects.create(name='Team A')

        # Create player
        player = Player.objects.create(team=team, name='Player A')

        # Test endpoint
        url = reverse('team-details', args=[team.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Response should be OK

    def test_player_details_endpoint(self):
        '''
        There must be an endpoint that returns a player's details
        '''
        # Authenticate using a player user since players have least access
        self.client.force_authenticate(user=self.player_user)

        # Create team
        team = Team.objects.create(name='Team A')

        # Create player
        player = Player.objects.create(team=team, name='Player A')

        # Test endpoint
        url = reverse('player-details', args=[player.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Response should be OK
