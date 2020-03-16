# Generated by Django 3.0.3 on 2020-02-06 08:36

from django.db import migrations
import sortedm2m.fields


class Migration(migrations.Migration):

    dependencies = [
        ('qrank', '0008_remove_game_players'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='players',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, to='qrank.Player'),
        ),
    ]
