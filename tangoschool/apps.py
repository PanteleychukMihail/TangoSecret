from django.apps import AppConfig


class TangoschoolConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tangoschool'
    verbose_name = 'Танго Сикрет'

    def ready(self):
        import tangoschool.signals


