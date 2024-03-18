from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.models import TokenUser

from league.models import Team, Game, Player, Coach


class APIEndpointsTest(APITestCase):
    def setUp(self):
        '''
        Create TokenUsers so they are available across all test in this test class
        '''
        self.player_user = TokenUser({
            'name': 'John Doe',
            'role': 'player',
            'team': 'Team Hello',
        })

    def test_games_per_round_list_endpoint(self):
        '''
        There must be an endpoint that returns all games in a league in a tree-like format
        '''
        # NOTE: No need to test output since serializer has its own tests
        #  and the view has no custom behaviour

        # We chose to authenticate with player but any role will do
        self.client.force_authenticate(user=self.player_user)

        # Create teams
        team_a = Team.objects.create(name='Team A')
        team_b = Team.objects.create(name='Team B')

        # Create game
        game = Game.objects.create(
            team_a=team_a, team_a_score=110,
            team_b=team_b, team_b_score=100)  # Finals game with teams A and B; A won

        # Send request
        url = reverse('games-per-round-list')
        response = self.client.get(url)

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

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # TODO: Could be deleted if no longer needed
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
            status.HTTP_403_FORBIDDEN)

        # Send request using a coach user
        coach_user = TokenUser({
            'name': 'John Doe',
            'role': 'coach',
            'team': 'Team Hello',
        })
        self.client.force_authenticate(user=coach_user)
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK)

        team_players = Player.objects.filter(team=team_a)
        self.assertEqual(
            len(response.data),
            team_players.count())  # Count from response should be the same from db

        # Test for all players regardless of team
        url = reverse('player-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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
        Set up does the following so the functions could run faster:
        - creates a TokenUser with the `player` role
        - creates a TokenUser with the `coach` role
        - creates a Team
        - creates a Coach assigned to the created team
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

    def test_player_has_no_access(self):
        '''
        Endpoint should block access from player users
        '''
        self.client.force_authenticate(user=self.player_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_always_has_access(self):
        '''
        Endpoint should allow access from admin users
        '''
        admin_user = TokenUser({
            'name': 'John Doe',
            'role': 'admin',
            'team': None,
        })

        self.client.force_authenticate(user=admin_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_coach_can_access_own_team(self):
        '''
        A coach should be able to see his team's details
        '''
        self.client.force_authenticate(user=self.coach_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_coach_cannot_access_other_team(self):
        '''
        A coach should not able to see his team's details
        '''
        other_team = Team.objects.create(name='Other team')
        Coach.objects.create(name='Other coach', team=other_team)
        other_url = reverse('team-details', args=[other_team.pk])

        self.client.force_authenticate(user=self.coach_user)
        response = self.client.get(other_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PlayerDetailEndpointTest(APITestCase):
    '''
    Tests for the player details endpoint
    '''
    def setUp(self):
        '''
        Set up does the following so the functions could run faster:
        - creates a TokenUser with the `player` role
        - creates a TokenUser with the `coach` role
        - creates a Team
        - creates a Coach assigned to the created team
        - creates a Player assigned to the created team
        '''
        self.team_name = 'Team Hello'

        # Create a player and coach user so they are available across all test in this test class
        self.player_user = TokenUser({
            'name': 'John Doe',
            'role': 'player',
            'team': self.team_name,
        })
        self.coach_user = TokenUser({
            'name': 'John Doe',
            'role': 'coach',
            'team': self.team_name,
        })

        self.team = Team.objects.create(name=self.team_name)
        self.coach = Coach.objects.create(name=self.coach_user.name, team=self.team)
        self.player = Player.objects.create(name=self.player_user.name, team=self.team)
        self.url = reverse('player-details', args=[self.player.pk])

    def test_admin_always_has_access(self):
        '''
        Endpoint should allow access from admin users
        '''
        admin_user = TokenUser({
            'name': 'John Doe',
            'role': 'admin',
            'team': None,
        })

        self.client.force_authenticate(user=admin_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_coach_can_access_own_teams_players(self):
        '''
        A coach should be able to see his team's players
        '''
        # Coach user should have access to his team's player details
        self.client.force_authenticate(user=self.coach_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_coach_cannot_access_other_teams_players(self):
        '''
        A coach should not be able to see other team's players
        '''
        # Coach user should not have access to other team's player details
        other_team = Team.objects.create(name='Other team')
        Coach.objects.create(name='Other coach', team=other_team)
        other_player = Player.objects.create(name='Other player', team=other_team)
        other_url = reverse('player-details', args=[other_player.pk])

        self.client.force_authenticate(user=self.coach_user)
        response = self.client.get(other_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AccessTokenEndpointTest(APITestCase):
    '''
    Tests for the access token endpoint
    '''
    def test_payload_checks(self):
        url = reverse('access-token-generator')

        # Must reject when there is no payload
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Must reject when role in payload is unreognized
        response = self.client.post(url, { 'role': 'unrecognized_role' })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_returns_access_token(self):
        # Create data
        team = Team.objects.create(name='Team Hello')
        Coach.objects.create(name='Coach', team=team)
        Player.objects.create(name='Player', team=team)

        url = reverse('access-token-generator')

        # Test admin
        response = self.client.post(url, { 'role': 'admin' })
        self.assertIn('name', response.data)
        self.assertIn('team', response.data)
        self.assertIn('role', response.data)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)

        # Test coach
        response = self.client.post(url, { 'role': 'coach' })
        self.assertIn('name', response.data)
        self.assertIn('team', response.data)
        self.assertIn('role', response.data)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)

        # Test player
        response = self.client.post(url, { 'role': 'player' })
        self.assertIn('name', response.data)
        self.assertIn('team', response.data)
        self.assertIn('role', response.data)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)
