from datetime import datetime

from django.db import models, connection
from django.urls import reverse
from django.utils import timezone


class Reactor(models.Model):
    STATUS_CHOICES = (
        (1, 'Действует'),
        (2, 'Удалена'),
    )

    name = models.CharField(max_length=100, default="Название реактора",  verbose_name="Название")
    status = models.IntegerField(max_length=100, choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    image = models.ImageField(upload_to="reactors", default="reactors/default.jpg", verbose_name="Фото")
    MaximumHeatOutput = models.IntegerField(default=60, verbose_name="Максимальная тепловая мощность")
    ElectricalPower = models.IntegerField(default=12, verbose_name="Электрическая мощность")
    MaximumNeutronFluxDensity = models.FloatField(default=3.7, verbose_name="Максимальная плотность потока быстрых нейтронов")
    AverageNeutronEnergy = models.IntegerField(default=380, verbose_name="Средняя энергия нейтронов")
    MicrocampaniaDuration = models.IntegerField(default=115, verbose_name="Продолжительность микрокампании")
    TimeBetweenMicroCompanies = models.IntegerField(default=45, verbose_name="Время между микрокомпаниями")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Реактор"
        verbose_name_plural = "Реакторы"

    def get_absolute_url(self):
        return reverse("reactor_details", kwargs={"reactor_id": self.id})

    def get_delete_url(self):
        return reverse("reactor_delete", kwargs={"reactor_id": self.id})

    def delete(self):
        with connection.cursor() as cursor:
            cursor.execute("UPDATE nuclearplants_reactor SET status = 2 WHERE id = %s", [self.pk])


class NuclearPowerStation(models.Model):
    STATUS_CHOICES = (
        (1, 'Введён'),
        (2, 'В работе'),
        (3, 'Завершен'),
        (4, 'Отклонен'),
        (5, 'Удален'),
    )

    name = models.CharField(max_length=100, verbose_name="Название")
    reactors = models.ManyToManyField(Reactor, verbose_name="Реактор", null=True)
    openingYear = models.IntegerField(default=1979, verbose_name="Год открытия")
    powerUnitsNumber = models.IntegerField(default=4, verbose_name="Количество энергоблоков")
    location = models.CharField(max_length=100, verbose_name="вблизи г. Балаково (Саратовская обл.)")

    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    date_created = models.DateTimeField(default=datetime.now(tz=timezone.utc), verbose_name="Дата создания")
    date_of_formation = models.DateTimeField(default=datetime.now(tz=timezone.utc), verbose_name="Дата формирования")
    date_complete = models.DateTimeField(default=datetime.now(tz=timezone.utc), verbose_name="Дата завершения")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "АЭС"
        verbose_name_plural = "АЭС"