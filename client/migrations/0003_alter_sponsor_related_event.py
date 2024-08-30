# Generated by Django 5.0.2 on 2024-07-12 16:12

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_organizer_rank1_organizer_rank2_organizer_rank3_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsor',
            name='related_event',
            field=models.OneToOneField(limit_choices_to={'end_at__lt': datetime.datetime(2024, 7, 12, 16, 12, 2, 462629, tzinfo=datetime.timezone.utc)}, on_delete=django.db.models.deletion.CASCADE, to='client.event'),
        ),
    ]
