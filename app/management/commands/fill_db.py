import random

from django.core import management
from django.core.management.base import BaseCommand
from app.models import *
from .utils import random_date, random_timedelta
from ...utils import random_text


def add_reactors():
    Reactor.objects.create(
        name=f"ЭГП-6",
        image="reactors/1.jpg",
        coolant="вода",
        fuel="Топливо",
        thermal_power="80",
        electrical_power="20"
    )

    Reactor.objects.create(
        name=f"АМБ-200",
        image="reactors/2.jpg",
        coolant="вода",
        fuel="двуокись урана",
        thermal_power="65",
        electrical_power="12"
    )

    Reactor.objects.create(
        name=f"РБМК-1000",
        image="reactors/3.jpg",
        coolant="вода",
        fuel="диоксид урана",
        thermal_power="50",
        electrical_power="11"
    )

    Reactor.objects.create(
        name=f"ВВЭР-1000",
        image="reactors/4.jpg",
        coolant="вода",
        fuel="диоксид урана",
        thermal_power="30",
        electrical_power="10"
    )

    print("Услуги добавлены")


def add_stations():
    owners = CustomUser.objects.filter(is_superuser=False)
    moderators = CustomUser.objects.filter(is_superuser=True)

    if len(owners) == 0 or len(moderators) == 0:
        print("Заявки не могут быть добавлены. Сначала добавьте пользователей с помощью команды add_users")
        return

    reactors = Reactor.objects.all()

    for _ in range(30):
        station = Station.objects.create()
        station.name = "АЭС №" + str(station.pk)
        station.status = random.randint(2, 5)
        station.owner = random.choice(owners)
        station.location = random_text()

        if station.status in [2, 3, 4]:
            station.year = random.randint(1954, 2023)

        if station.status in [3, 4]:
            station.date_complete = random_date()
            station.date_formation = station.date_complete - random_timedelta()
            station.date_created = station.date_formation - random_timedelta()
            station.moderator = random.choice(moderators)
        else:
            station.date_formation = random_date()
            station.date_created = station.date_formation - random_timedelta()

        for i in range(random.randint(1, 3)):
            station.reactors.add(random.choice(reactors))

        station.save()

    print("Заявки добавлены")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        management.call_command("clean_db")
        management.call_command("add_users")

        add_reactors()
        add_stations()









