# Generated by Django 3.0.3 on 2020-02-05 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qrank', '0004_player_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='player1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player1', to='qrank.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='player2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player2', to='qrank.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='player3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player3', to='qrank.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='player4',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player4', to='qrank.Player'),
        ),
    ]
