# Generated by Django 3.0.3 on 2020-02-06 08:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qrank', '0007_auto_20200205_1408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='players',
        ),
    ]