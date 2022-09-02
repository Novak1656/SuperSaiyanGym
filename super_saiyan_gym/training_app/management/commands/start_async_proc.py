from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Запуск асинхронных задач'

    def handle(self, *args, **options):
        if settings.SCHEDULER_DEFAULT:
            from super_saiyan_gym import operator
            operator.start()
