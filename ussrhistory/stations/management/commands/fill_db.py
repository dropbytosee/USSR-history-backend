import random

from django.contrib.auth.models import User
from django.core import management
from django.core.management.base import BaseCommand
from stations.models import *
from .add_users import add_users
from .utils import random_date, random_timedelta


def add_reactors():
    Reactor.objects.create(
        name="Нововоро́нежский реактор",
        maximumHeatOutput=random.randint(30, 100),
        electricalPower=random.randint(10, 30),
        maximumNeutronFluxDensity=round(random.uniform(1.0, 5.0), 2),
        averageNeutronEnergy=random.randint(100, 500),
        microcampaniaDuration=random.randint(50, 300),
        timeBetweenMicroCompanies=random.randint(10, 60)
    )
    Reactor.objects.create(
        name="Курский реактор",
        maximumHeatOutput=random.randint(30, 100),
        electricalPower=random.randint(10, 30),
        maximumNeutronFluxDensity=round(random.uniform(1.0, 5.0), 2),
        averageNeutronEnergy=random.randint(100, 500),
        microcampaniaDuration=random.randint(50, 300),
        timeBetweenMicroCompanies=random.randint(10, 60)
    )
    Reactor.objects.create(
        name="Черно́быльский реактор",
        maximumHeatOutput=random.randint(30, 100),
        electricalPower=random.randint(10, 30),
        maximumNeutronFluxDensity=round(random.uniform(1.0, 5.0), 2),
        averageNeutronEnergy=random.randint(100, 500),
        microcampaniaDuration=random.randint(50, 300),
        timeBetweenMicroCompanies=random.randint(10, 60)
    )

    print("Услуги добавлены")


def add_stations():
    owners = User.objects.filter(is_superuser=False)
    moderators = User.objects.filter(is_superuser=True)

    if len(owners) == 0 or len(moderators) == 0:
        print("Заявки не могут быть добавлены. Сначала добавьте пользователей с помощью команды add_users")
        return

    reactors = Reactor.objects.all()

    for _ in range(30):
        station = Station.objects.create()
        station.name = "Станция №" + str(station.pk)
        station.status = random.randint(2, 5)

        if station.status in [3, 4]:
            station.closed_date = random_date()
            station.formated_date = station.closed_date - random_timedelta()
            station.created_date = station.formated_date - random_timedelta()
        else:
            station.formated_date = random_date()
            station.created_date = station.formated_date - random_timedelta()

        station.owner = random.choice(owners)
        station.moderator = random.choice(moderators)

        for i in range(random.randint(1, 3)):
            station.reactors.add(random.choice(reactors))

        station.save()

    print("Заявки добавлены")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        management.call_command("clean_db")

        add_users()
        add_reactors()
        add_stations()









