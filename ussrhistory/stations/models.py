from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Reactor(models.Model):
    STATUS_CHOICES = (
        (1, 'Действует'),
        (2, 'Удалена'),
    )

    name = models.CharField(max_length=100, default="Название реактора",  verbose_name="Название")
    status = models.IntegerField(max_length=100, choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    image = models.ImageField(upload_to="reactors", default="reactors/default.jpg", verbose_name="Фото")
    maximumHeatOutput = models.IntegerField(default=60, verbose_name="Максимальная тепловая мощность")
    electricalPower = models.IntegerField(default=12, verbose_name="Электрическая мощность")
    maximumNeutronFluxDensity = models.FloatField(default=3.7, verbose_name="Максимальная плотность потока быстрых нейтронов")
    averageNeutronEnergy = models.IntegerField(default=380, verbose_name="Средняя энергия нейтронов")
    microcampaniaDuration = models.IntegerField(default=115, verbose_name="Продолжительность микрокампании")
    timeBetweenMicroCompanies = models.IntegerField(default=45, verbose_name="Время между микрокомпаниями")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Реактор"
        verbose_name_plural = "Реакторы"


class Station(models.Model):
    STATUS_CHOICES = (
        (1, 'Введён'),
        (2, 'В работе'),
        (3, 'Завершен'),
        (4, 'Отклонен'),
        (5, 'Удален'),
    )

    reactors = models.ManyToManyField(Reactor, verbose_name="Реакторы", null=True)

    name = models.CharField(max_length=100, default="Название",  verbose_name="Название")
    openingYear = models.IntegerField(default=1979, verbose_name="Год открытия")
    powerUnitsNumber = models.IntegerField(default=4, verbose_name="Количество энергоблоков")
    location = models.CharField(max_length=100, default="вблизи г. Балаково (Саратовская обл.)", verbose_name="Местоположение")

    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    date_created = models.DateTimeField(default=datetime.now(tz=timezone.utc), verbose_name="Дата создания")
    date_of_formation = models.DateTimeField(verbose_name="Дата формирования", blank=True, null=True)
    date_complete = models.DateTimeField(verbose_name="Дата завершения", blank=True, null=True)

    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="Создатель", related_name='owner', null=True)
    moderator = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="Модератор", related_name='moderator', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "АЭС"
        verbose_name_plural = "АЭС"