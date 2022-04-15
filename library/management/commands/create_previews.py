from django.core.management.base import BaseCommand

from library.tasks import create_previews


class Command(BaseCommand):
    help = 'create previews for all PDFs'

    def handle(self, *args, **options):
        create_previews.delay()
