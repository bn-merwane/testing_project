# Generated by Django 5.0.2 on 2024-07-12 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizer',
            name='rank1',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='organizer',
            name='rank2',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='organizer',
            name='rank3',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='organizer',
            name='rank4',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='organizer',
            name='rank5',
            field=models.IntegerField(default=0),
        ),
    ]
