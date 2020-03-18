# Generated by Django 3.0.3 on 2020-03-17 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qrank', '0020_rank_match_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='game',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='qrank.Game'),
            preserve_default=False,
        ),
    ]
