# Generated by Django 5.0.2 on 2024-07-12 16:23

import datetime
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0005_notification_dateandtime_alter_demand_event_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='demand',
            options={'ordering': ['demande_dateandtime']},
        ),
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ['dateandtime']},
        ),
        migrations.AddField(
            model_name='demand',
            name='demande_dateandtime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='demand',
            name='event',
            field=models.ForeignKey(limit_choices_to={'end_at__lt': datetime.datetime(2024, 7, 12, 16, 23, 40, 809685, tzinfo=datetime.timezone.utc), 'registration_end': False}, on_delete=django.db.models.deletion.CASCADE, to='client.event'),
        ),
        migrations.AlterField(
            model_name='eventregistration',
            name='event',
            field=models.ForeignKey(limit_choices_to={'end_at__lt': datetime.datetime(2024, 7, 12, 16, 23, 40, 810648, tzinfo=datetime.timezone.utc), 'registration_end': False}, on_delete=django.db.models.deletion.CASCADE, to='client.event'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='event',
            field=models.ForeignKey(limit_choices_to={'end_at__lt': datetime.datetime(2024, 7, 12, 16, 23, 40, 808645, tzinfo=datetime.timezone.utc)}, on_delete=django.db.models.deletion.CASCADE, to='client.event'),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='related_event',
            field=models.OneToOneField(limit_choices_to={'end_at__lt': datetime.datetime(2024, 7, 12, 16, 23, 40, 808547, tzinfo=datetime.timezone.utc)}, on_delete=django.db.models.deletion.CASCADE, to='client.event'),
        ),
    ]
