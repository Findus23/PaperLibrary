from django.core.management.base import BaseCommand

from library.tasks import update_citenames


class Command(BaseCommand):
    help = 'updates all citenames'

    def handle(self, *args, **options):
        update_citenames.delay()
