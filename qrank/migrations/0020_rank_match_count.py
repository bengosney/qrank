# Generated by Django 3.0.3 on 2020-03-17 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qrank', '0019_auto_20200317_0829'),
    ]

    operations = [
        migrations.AddField(
            model_name='rank',
            name='match_count',
            field=models.IntegerField(default=0),
        ),
    ]
