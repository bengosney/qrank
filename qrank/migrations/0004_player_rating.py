# Generated by Django 3.0.3 on 2020-02-05 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qrank', '0003_gameplayer_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='rating',
            field=models.IntegerField(default=25),
        ),
    ]
