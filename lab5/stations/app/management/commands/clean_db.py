from django.core.management.base import BaseCommand
from app.models import *


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Station.objects.all().delete()
        Reactor.objects.all().delete()
        CustomUser.objects.all().delete()