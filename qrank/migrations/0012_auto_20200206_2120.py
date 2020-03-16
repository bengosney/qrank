# Generated by Django 3.0.3 on 2020-02-06 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qrank', '0011_game_ranked'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={'ordering': ['-rating', 'name']},
        ),
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
