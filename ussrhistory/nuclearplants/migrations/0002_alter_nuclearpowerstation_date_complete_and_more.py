# Generated by Django 4.2.4 on 2023-10-18 16:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nuclearplants', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nuclearpowerstation',
            name='date_complete',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 18, 16, 33, 41, 252338, tzinfo=datetime.timezone.utc), verbose_name='Дата завершения'),
        ),
        migrations.AlterField(
            model_name='nuclearpowerstation',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 18, 16, 33, 41, 252338, tzinfo=datetime.timezone.utc), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='nuclearpowerstation',
            name='date_of_formation',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 18, 16, 33, 41, 252338, tzinfo=datetime.timezone.utc), verbose_name='Дата формирования'),
        ),
    ]
