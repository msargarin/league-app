from decimal import Decimal

from django.db import models
from django.db.models import Q


class Person(models.Model):
    '''
    A person has a name
    '''
    name = models.CharField(max_length=160, unique=True)

    class Meta:
        abstract = True


class Team(models.Model):
    '''
    A team has a name and a coach
    '''
    name = models.CharField(max_length=160, unique=True)
    average_score = models.DecimalField(max_digits=4, decimal_places=1, default=Decimal('0.0'))

    def get_games(self):
        return Game.objects.filter(Q(team_a=self) | Q(team_b=self))


class Coach(Person):
    '''
    A coach is a person with a team
    '''
    team = models.OneToOneField(
        Team,
        on_delete=models.CASCADE,
        related_name='coach')


class Player(Person):
    '''
    A player is a person with a team
    '''
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='players')
    average_score = models.DecimalField(max_digits=4, decimal_places=1, default=Decimal('0.0'))
    total_games_played = models.PositiveIntegerField(default=0)


class Game(models.Model):
    '''
    A game has two opposing teams and their scores
    '''
    team_a = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name='+')
    team_a_score = models.PositiveIntegerField()

    team_b = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name='+')
    team_b_score = models.PositiveIntegerField()

    next_game = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        verbose_name='Next game in league',
        related_name='previous_games',
        null=True)

    def get_winning_team(self):
        # Determine winner based on their scores
        if self.team_a_score > self.team_b_score:
            return self.team_a
        else:  # There are no ties in a basketball game!
            return self.team_b

    def save(self, *args, **kwargs):
        # Raise value error if only 1 team is specified
        if self.team_a == self.team_b:
            raise ValueError('Scores cannot be the same.')

        # Raise value error if both teams have same score
        if self.team_a_score == self.team_b_score:
            raise ValueError('Scores cannot be the same.')

        super().save(*args, **kwargs)


class PlayedGame(models.Model):
    '''
    A player's score in a game he played
    '''
    game = models.ForeignKey(
        Game,
        on_delete=models.PROTECT,
        related_name='participants')
    player = models.ForeignKey(
        Player,
        on_delete=models.PROTECT,
        related_name='games_played')
    score = models.PositiveIntegerField()
