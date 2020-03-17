# Generated by Django 3.0.3 on 2020-03-16 08:47

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('qrank', '0017_auto_20200312_0849'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={'ordering': ['name']},
        ),
        migrations.RemoveField(
            model_name='player',
            name='rating',
        ),
        migrations.AddField(
            model_name='game',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='name'),
        ),
        migrations.AddField(
            model_name='player',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='name'),
        ),
    ]
