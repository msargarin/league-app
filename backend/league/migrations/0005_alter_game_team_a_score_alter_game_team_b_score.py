# Generated by Django 4.2.11 on 2024-03-15 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0004_alter_coach_name_alter_player_name_alter_team_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='team_a_score',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='game',
            name='team_b_score',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]