from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from django.utils import timezone


class Reactor(models.Model):
    STATUS_CHOICES = (
        (1, 'Действует'),
        (2, 'Удалена'),
    )

    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(max_length=500, verbose_name="Описание")
    maximumHeatOutput = models.IntegerField(default=60, verbose_name="Максимальная тепловая мощность")
    electricalPower = models.IntegerField(default=12, verbose_name="Электрическая мощность")

    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    image = models.ImageField(default="reactors/default.png", verbose_name="Фото")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Реактор"
        verbose_name_plural = "Реакторы"


class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, password="1234", **extra_fields):
        extra_fields.setdefault('name', name)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, name, email, password="1234", **extra_fields):
        extra_fields.setdefault('is_moderator', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(name, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30)
    is_moderator = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Station(models.Model):
    STATUS_CHOICES = (
        (1, 'Введён'),
        (2, 'В работе'),
        (3, 'Завершён'),
        (4, 'Отменён'),
        (5, 'Удалён'),
    )

    reactors = models.ManyToManyField(Reactor, verbose_name="Реакторы", null=True)

    name = models.CharField(max_length=100, default="Название", verbose_name="Название")
    openingYear = models.IntegerField(default=1979, verbose_name="Год открытия")
    powerUnits = models.IntegerField(default=4, verbose_name="Количество энергоблоков")
    location = models.CharField(max_length=100, default="вблизи г. Балаково (Саратовская обл.)", verbose_name="Местоположение")

    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    date_created = models.DateTimeField(default=timezone.now(), verbose_name="Дата создания")
    date_formation = models.DateTimeField(verbose_name="Дата формирования", blank=True, null=True)
    date_complete = models.DateTimeField(verbose_name="Дата завершения", blank=True, null=True)

    owner = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, verbose_name="Создатель", related_name='owner', null=True)
    moderator = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, verbose_name="Модератор", related_name='moderator', null=True)

    def __str__(self):
        return "АЭС №" + str(self.pk)

    class Meta:
        verbose_name = "АЭС"
        verbose_name_plural = "АЭС"