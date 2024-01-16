from django.core.management.base import BaseCommand
from stations.models import *


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Station.objects.all().delete()
        Reactor.objects.all().delete()
        User.objects.all().delete()