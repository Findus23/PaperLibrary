from django.apps import AppConfig



class LibraryConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'library'

    def ready(self):
        from . import signals
        return signals
