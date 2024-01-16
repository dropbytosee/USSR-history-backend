# Generated by Django 4.2.5 on 2023-12-13 20:43

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reactor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Название реактора', max_length=100, verbose_name='Название')),
                ('status', models.IntegerField(choices=[(1, 'Действует'), (2, 'Удалена')], default=1, max_length=100, verbose_name='Статус')),
                ('image', models.ImageField(default='reactors/default.jpg', upload_to='reactors', verbose_name='Фото')),
                ('maximumHeatOutput', models.IntegerField(default=60, verbose_name='Максимальная тепловая мощность')),
                ('electricalPower', models.IntegerField(default=12, verbose_name='Электрическая мощность')),
                ('maximumNeutronFluxDensity', models.FloatField(default=3.7, verbose_name='Максимальная плотность потока быстрых нейтронов')),
                ('averageNeutronEnergy', models.IntegerField(default=380, verbose_name='Средняя энергия нейтронов')),
                ('microcampaniaDuration', models.IntegerField(default=115, verbose_name='Продолжительность микрокампании')),
                ('timeBetweenMicroCompanies', models.IntegerField(default=45, verbose_name='Время между микрокомпаниями')),
            ],
            options={
                'verbose_name': 'Реактор',
                'verbose_name_plural': 'Реакторы',
            },
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Название электростанции', max_length=100, verbose_name='Название')),
                ('openingYear', models.IntegerField(default=1979, verbose_name='Год открытия')),
                ('powerUnitsNumber', models.IntegerField(default=4, verbose_name='Количество энергоблоков')),
                ('location', models.CharField(default='вблизи г. Балаково (Саратовская обл.)', max_length=100, verbose_name='Местоположение')),
                ('status', models.IntegerField(choices=[(1, 'Введён'), (2, 'В работе'), (3, 'Завершен'), (4, 'Отклонен'), (5, 'Удален')], default=1, verbose_name='Статус')),
                ('date_created', models.DateTimeField(default=datetime.datetime(2023, 12, 13, 20, 43, 31, 508847, tzinfo=datetime.timezone.utc), verbose_name='Дата создания')),
                ('date_of_formation', models.DateTimeField(blank=True, null=True, verbose_name='Дата формирования')),
                ('date_complete', models.DateTimeField(blank=True, null=True, verbose_name='Дата завершения')),
                ('moderator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='moderator', to=settings.AUTH_USER_MODEL, verbose_name='Модератор')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='owner', to=settings.AUTH_USER_MODEL, verbose_name='Создатель')),
                ('reactors', models.ManyToManyField(null=True, to='stations.reactor', verbose_name='Реактор')),
            ],
            options={
                'verbose_name': 'АЭС',
                'verbose_name_plural': 'АЭС',
            },
        ),
    ]
