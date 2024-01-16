# Generated by Django 4.2.4 on 2023-10-08 11:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reactor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Название реактора', max_length=100, verbose_name='Название')),
                ('status', models.IntegerField(choices=[(1, 'Действует'), (2, 'Удалена')], default=1, max_length=100, verbose_name='Статус')),
                ('image', models.ImageField(default='reactors/default.jpg', upload_to='reactors', verbose_name='Фото')),
                ('MaximumHeatOutput', models.IntegerField(default=60, verbose_name='Максимальная тепловая мощность')),
                ('ElectricalPower', models.IntegerField(default=12, verbose_name='Электрическая мощность')),
                ('MaximumNeutronFluxDensity', models.FloatField(default=3.7, verbose_name='Максимальная плотность потока быстрых нейтронов')),
                ('AverageNeutronEnergy', models.IntegerField(default=380, verbose_name='Средняя энергия нейтронов')),
                ('MicrocampaniaDuration', models.IntegerField(default=115, verbose_name='Продолжительность микрокампании')),
                ('TimeBetweenMicroCompanies', models.IntegerField(default=45, verbose_name='Время между микрокомпаниями')),
            ],
            options={
                'verbose_name': 'Реактор',
                'verbose_name_plural': 'Реакторы',
            },
        ),
        migrations.CreateModel(
            name='NuclearPowerStation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('openingYear', models.IntegerField(default=1979, verbose_name='Год открытия')),
                ('powerUnitsNumber', models.IntegerField(default=4, verbose_name='Количество энергоблоков')),
                ('location', models.CharField(max_length=100, verbose_name='вблизи г. Балаково (Саратовская обл.)')),
                ('status', models.IntegerField(choices=[(1, 'Введён'), (2, 'В работе'), (3, 'Завершен'), (4, 'Отклонен'), (5, 'Удален')], default=1, verbose_name='Статус')),
                ('date_created', models.DateTimeField(default=datetime.datetime(2023, 10, 8, 11, 26, 23, 33728, tzinfo=datetime.timezone.utc), verbose_name='Дата создания')),
                ('date_of_formation', models.DateTimeField(default=datetime.datetime(2023, 10, 8, 11, 26, 23, 33728, tzinfo=datetime.timezone.utc), verbose_name='Дата формирования')),
                ('date_complete', models.DateTimeField(default=datetime.datetime(2023, 10, 8, 11, 26, 23, 33728, tzinfo=datetime.timezone.utc), verbose_name='Дата завершения')),
                ('reactors', models.ManyToManyField(null=True, to='nuclearplants.reactor', verbose_name='Реактор')),
            ],
            options={
                'verbose_name': 'АЭС',
                'verbose_name_plural': 'АЭС',
            },
        ),
    ]
