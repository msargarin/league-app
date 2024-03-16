from decimal import Decimal
from random import randint
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction, OperationalError
from django.db.models import Q, Avg, DecimalField, Case, When, F
from league.models import Team, Coach, Player, Game, PlayedGame


TEAM_NAMES = [  # 16 teams
    'Quirky Penguins', 'Skyline Swiftsters', 'Passionate Hoops', 'The Wry Champions', 'Stargazing Explorers',
    'Chorus Rainbows', 'Magical Wanderers', 'Sonic Flutter', 'Rampage Rares', 'Panther Pride Prowlers',
    'Steel Lightning', 'Mighty Stampede', 'Calm Cobras', 'Spirit Striders', 'Silicon Pinnacles',
    'Daring Magpies'
]
PERSON_NAMES = [  # 176 people = 160 players + 16 coaches
    'Ned Lynn', 'Moses Davis', 'Waldo Davila', 'Bennett Munoz', 'Murray Bonilla', 'Isidro Kelly', 'Brant Massey', 'Arthur Rogers', 'Darin Werner', 'Edwin Liu', 'Joel Callahan', 'Shayne Carson', 'Emanuel Knight', 'Herbert Bauer', 'Sebastian Montes', 'Luke Jensen', 'Minh Hill', 'Teddy Andrews', 'Eugenio Carpenter', 'Donald Weiss', 'Oren Carlson', 'Renaldo Floyd', 'Cristopher Rocha', 'Rudolf Long', 'Jim Carey', 'Brett Turner', 'Oscar Roy', 'Amado Woodward', 'Edmund Moore', 'Kristopher Allen', 'Earnest Buckley', 'Clark Mueller', 'Alfonzo Hancock', 'Ramiro Combs', 'Derick Chapman', 'Oswaldo Hernandez', 'Garth Sharp', 'Sung Bryant', 'Sol Kent', 'Morton Skinner', 'Caleb Trevino', 'Orlando Bryan', 'Zack Dougherty', 'Boyce Trujillo', 'Boyd Thomas', 'Booker Maxwell', 'Brendan Boone', 'Lino Barton', 'Buck Parks', 'Edwardo Meadows', 'Roderick Sanchez', 'Ernesto Bradford', 'Ned Landry', 'Tommy Gutierrez', 'Alfred Gibson', 'Salvatore Matthews', 'Milo Gallegos', 'Marshall Mack', 'Homer Webster', 'Alfonso Underwood', 'Doug Friedman', 'Loyd Wiggins', 'Mel Christensen', 'Kurtis Welch', 'Carl Zamora', 'Cristobal Mercado', 'Randy Greene', 'Giovanni Lowery', 'Reyes Flowers', 'Gale Mendoza', 'Johnathan Shannon', 'Charley Stokes', 'Lavern Warner', 'Clemente Fox', 'Kelley Garza', 'Donovan Hodge', 'Kevin Patel', 'Arden Ingram', 'Kieth Franco', 'Valentin Abbott', 'Darius Prince', 'Terrance Cochran', 'Robert Salas', 'Darron Leonard', 'Rudolf Baker', 'Young Powers', 'Emmitt Ortiz', 'Alfonzo Fernandez', 'Irving Mcclain', 'Nestor Murillo', 'Eugene Brock', 'Bobbie Cabrera', 'Wally Tucker', 'Leigh Rush', 'Bobby Robinson', 'Ellsworth Cameron', 'Lou Carpenter', 'Shelby Silva', 'Cole Phillips', 'Jayson Roth', 'Don Mahoney', 'Thurman Dickson', 'Garth Villanueva', 'Leland Leblanc', 'Josue Terry', 'Jerald Shepard', 'Allan Braun', 'Doyle Conrad', 'Nathanael Patel', 'Rigoberto Frye', 'Odis Parsons', 'Joseph Adams', 'Buster Nguyen', 'Monty Kaiser', 'Lorenzo Stanley', 'Renaldo Ashley', 'Andreas Hoffman', 'Cesar Washington', 'Ross Stanton', 'Vito Whitney', 'Lenard Rice', 'Mark Garner', 'Zachary Jensen', 'Terrence Webb', 'Louis Curtis', 'Nicky Yates', 'Rickie Krause', 'Buck Wiley', 'Merlin Hobbs', 'Charles Schroeder', 'Hung Johnston', 'Otto Duncan', 'Matthew Morton', 'Pasquale Avery', 'Dale Mccullough', 'Adalberto Pugh', 'Gerardo Odonnell', 'Noble Williamson', 'Andrew Ross', 'Tuan Knight', 'Benito Ortiz', 'Van Maddox', 'Robt Gonzales', 'Charlie Weiss', 'Clayton Dixon', 'Adolph Mcintosh', 'Daron Newman', 'Nelson Freeman', 'Jerrell Orr', 'Freddie Atkins', 'Cliff Davies', 'Joey Hays', 'Jason Mcmillan', 'Brice Hubbard', 'Jaime Mcclure', 'Leland Garrison', 'Jackson Pratt', 'Markus Marsh', 'Junior Daniel', 'Pasquale Winters', 'Elisha Hays', 'Rex Hahn', 'Hershel Silva', 'Blaine Bauer', 'Jorge Mcmahon', 'Walker Morris', 'Blake Robinson', 'Mathew Howe', 'Douglass Webb', 'Roger Franklin', 'Warren Guzman', 'Cletus Rose', 'Alphonso Rosales', 'Tyrell Barajas', 'Rufus Oconnor', 'Nestor Jimenez'
]
BASE_SCORE = 80

def get_one(pool):
    '''
    Helper function for popping one random object from a list
    '''
    return pool.pop(randint(0, len(pool)-1))

def allocate_points(points_to_allocate, players, game):
    '''
    Helper function for allocation points across a pool of players
    '''
    games_played_count = 0
    while points_to_allocate > 0:
        # If there is only one player left, allocate all points to that player
        if len(players) == 1:
            player_score = points_to_allocate

        # Otherwise, try to distribute randomly
        else:
            lower_limit = int(points_to_allocate / len(players))

            # upper limit is capped at half of remaining points when more than 7 players are still available
            #  otherwise, we risk losing points for the rest of the players since minimum per game is 5
            if len(players) > 7:
                upper_limit = int(points_to_allocate / 2)
            else:
                upper_limit = points_to_allocate

            player_score = randint(lower_limit, upper_limit)

        PlayedGame.objects.create(
            game=game,
            player=get_one(players),
            score=player_score)
        games_played_count += 1

        points_to_allocate -= player_score

    # If all points have been allocated but more than 5 players remain,
    #  we take more players and give them zero scores
    if len(players) > 5:
        for _ in range(len(players) - 5):
            PlayedGame.objects.create(
                game=game,
                player=get_one(players),
                score=0)
            games_played_count += 1

    return games_played_count


class Command(BaseCommand):
    help = "Populates the database with dummy data"

    def handle(self, *args, **kwargs):
        try:
            if Team.objects.exists():
                raise CommandError('Data appears to have already been populated')
        except OperationalError:
            raise CommandError('Database table appears to be missing. Have you ran python manage.py migrate?')

        available_person_names = PERSON_NAMES

        teams = []
        winners = []

        team_count = 0
        coach_count = 0
        player_count = 0
        games_count = 0
        games_played_count = 0

        with transaction.atomic():
            # Create teams, coaches and players
            for team_name in TEAM_NAMES:
                # Create Team
                this_team = Team.objects.create(name=team_name)

                # Create Coach
                Coach.objects.create(
                    name=get_one(available_person_names),
                    team=this_team)
                coach_count += 1

                # Create 10 players
                for _ in range(10):
                    Player.objects.create(
                        name=get_one(available_person_names),
                        team=this_team)
                    player_count += 1

                teams.append(this_team)
                team_count += 1

            # Create Games
            while len(teams) > 0:
                # Determine scores
                team_a_score = randint(BASE_SCORE+ randint(-10, 10), BASE_SCORE + randint(15, 40))
                team_b_score = randint(BASE_SCORE+ randint(-10, 10), BASE_SCORE + randint(15, 40))
                while team_a_score == team_b_score:
                    team_b_score += randint(-1, 1)

                this_game = Game.objects.create(
                    team_a=get_one(teams),
                    team_b=get_one(teams),
                    team_a_score=team_a_score,
                    team_b_score=team_b_score)
                games_count += 1

                # Link previous game of the two teams
                Game.objects \
                    .filter(
                        # team a in this game is also team a in their previous game
                        Q( Q(team_a=this_game.team_a) & ~Q(team_b=this_game.team_b) )

                        # team a in this game is team b in their previous game
                        | Q( ~Q(team_a=this_game.team_b) & Q(team_b=this_game.team_a) )

                        # team b in this game is also team b in their previous game
                        | Q( ~Q(team_a=this_game.team_a) & Q(team_b=this_game.team_b) )

                        # team b in this game is team a in their previous game
                        | Q( Q(team_a=this_game.team_b) & ~Q(team_b=this_game.team_a) ),

                        # we only look at games that are not yet linked
                        next_game__isnull=True) \
                    .update(next_game=this_game)

                # Allocate scores to players of team a
                games_played_count += allocate_points(team_a_score, list(this_game.team_a.players.all()), this_game)

                # Allocate scores to players of team b
                games_played_count += allocate_points(team_b_score, list(this_game.team_b.players.all()), this_game)

                # Take note of the winner
                winners.append(this_game.get_winning_team())

                # If there are no teams left then start creating games with the winners
                #  ie. move to the next round of games
                if len(teams) == 0 and len(winners) > 1:
                    teams = winners
                    winners = []

            # Compute stats for all players
            for this_player in Player.objects.all():
                played_games = PlayedGame.objects.filter(player=this_player)

                this_player.average_score = played_games.aggregate(
                    Avg('score', output_field=DecimalField(max_digits=4, decimal_places=1), default=Decimal('0.0'))
                )['score__avg']
                this_player.total_games_played = played_games.count()
                this_player.save()

            # Compute stats for teams
            for this_team in Team.objects.all():
                played_games = Game.objects \
                    .filter(Q(team_a=this_team) | Q(team_b=this_team)) \
                    .annotate(this_team_score=Case(
                        When(Q(team_a=this_team), then=F('team_a_score')),
                        When(Q(team_b=this_team), then=F('team_b_score')),
                        default=0
                    ))

                this_team.average_score = played_games.aggregate(
                    Avg('this_team_score', output_field=DecimalField(max_digits=4, decimal_places=1), default=Decimal('0.0'))
                )['this_team_score__avg']
                this_team.save()

            self.stdout.write(
                self.style.SUCCESS('Successfully created the following:')
                + '\n - ' + self.style.SUCCESS('%s teams' % team_count)
                + '\n - ' + self.style.SUCCESS('%s coaches' % coach_count)
                + '\n - ' + self.style.SUCCESS('%s players' % player_count)
                + '\n - ' + self.style.SUCCESS('%s games' % games_count)
                + '\n - ' + self.style.SUCCESS('%s game participations' % games_played_count)
            )
