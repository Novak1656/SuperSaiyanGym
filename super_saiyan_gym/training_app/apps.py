from django.apps import AppConfig
from django.conf import settings


class TrainingAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'training_app'

    def ready(self):
        if settings.SCHEDULER_DEFAULT:
            from super_saiyan_gym import operator
            operator.start()
