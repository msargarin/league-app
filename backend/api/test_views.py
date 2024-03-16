from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.tokens import Token


from league.models import Team, Game, Player, Coach


class APIEndpointsTest(APITestCase):
    def setUp(self):
        '''
        Create TokenUsers of different user types so they are available across all test in this test class
        '''
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


class TeamDetailEndpointTest(APITestCase):
    '''
    Tests for the team details endpoint
    '''
    def setUp(self):
        '''
        Create team, player user and coach user so we no longer need to create them at the test functions
        '''
        self.team_name = 'Team Hello'

        # Create TokenUsers of different user types so they are available across all test in this test class
        self.player_user = TokenUser({
            'name': 'John Doe',
            'role': 'player',
            'team': self.team_name,
        })  # Player user
        self.coach_user = TokenUser({
            'name': 'John Doe',
            'role': 'coach',
            'team': self.team_name,
        })  # Coach user

        self.team = Team.objects.create(name=self.team_name)
        self.coach = Coach.objects.create(name=self.coach_user.name, team=self.team)
        self.url = reverse('team-details', args=[self.team.pk])

    def test_for_error(self):
        '''
        Endpoint should return OK
        '''
        # Authenticate using the coach user since coaches have lowest level of access to this view
        self.client.force_authenticate(user=self.coach_user)

        # Test endpoint
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Response should be OK

    def test_at_least_coach_can_access(self):
        '''
        Endpoint should only be access to coaches and admins
        '''
        # Player accounts should have no access
        self.client.force_authenticate(user=self.player_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Response should be FORBIDDEN

        # Coach accounts should have access
        self.client.force_authenticate(user=self.coach_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Response should be OK

    def test_coach_can_only_access_own_team(self):
        '''
        A coach should only be able to see his team's details
        '''
        # Coach user should have access to his team's details
        self.client.force_authenticate(user=self.coach_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Response should be OK

        # Coach user should not have access to other team's details
        other_team = Team.objects.create(name='Other team')
        Coach.objects.create(name='Other coach', team=other_team)
        other_url = reverse('team-details', args=[other_team.pk])

        self.client.force_authenticate(user=self.coach_user)
        response = self.client.get(other_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Response should be FORBIDDEN


class PlayerDetailEndpointTest(APITestCase):
    '''
    Tests for the player details endpoint
    '''
    def setUp(self):
        '''
        Create team, player user and coach user so we no longer need to create them at the test functions
        '''
        self.team_name = 'Team Hello'

        # Create TokenUsers of different user types so they are available across all test in this test class
        self.player_user = TokenUser({
            'name': 'John Doe',
            'role': 'player',
            'team': self.team_name,
        })  # Player user
        self.coach_user = TokenUser({
            'name': 'John Doe',
            'role': 'coach',
            'team': self.team_name,
        })  # Coach user

        self.team = Team.objects.create(name=self.team_name)
        self.coach = Coach.objects.create(name=self.coach_user.name, team=self.team)
        self.player = Player.objects.create(name=self.player_user.name, team=self.team)
        self.url = reverse('player-details', args=[self.player.pk])

    def test_for_error(self):
        '''
        Endpoint should return OK
        '''
        # Authenticate using the coach user since coaches have lowest level of access to this view
        self.client.force_authenticate(user=self.coach_user)

        # Test endpoint
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Response should be OK

    def test_coach_can_only_access_his_players(self):
        '''
        A coach should only be able to see his team's players
        '''
        # Coach user should have access to his team's player details
        self.client.force_authenticate(user=self.coach_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Response should be OK

        # Coach user should not have access to other team's player details
        other_team = Team.objects.create(name='Other team')
        Coach.objects.create(name='Other coach', team=other_team)
        other_player = Player.objects.create(name='Other player', team=other_team)
        other_url = reverse('player-details', args=[other_player.pk])

        self.client.force_authenticate(user=self.coach_user)
        response = self.client.get(other_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Response should be FORBIDDEN
