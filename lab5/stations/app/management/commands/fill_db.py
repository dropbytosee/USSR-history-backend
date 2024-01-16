import random

from django.core import management
from django.core.management.base import BaseCommand
from app.models import *
from .utils import random_date, random_timedelta


def add_reactors():

    for i in range(1, 5):
        Reactor.objects.create(
            name=f"Реактор №{i}",
            description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam mollis sagittis metus, non laoreet ipsum consectetur at.",
            image=f"reactors/{i}.jpg",
            maximumHeatOutput=random.randint(20, 100),
            electricalPower=random.randint(10, 20)
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

        if station.status in [3, 4]:
            station.closed_date = random_date()
            station.formated_date = station.closed_date - random_timedelta()
            station.created_date = station.formated_date - random_timedelta()
            station.moderator = random.choice(moderators)
        else:
            station.formated_date = random_date()
            station.created_date = station.formated_date - random_timedelta()

        station.owner = random.choice(owners)

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









