from django.core.management.base import BaseCommand

from library.tasks import extract_fulltext


class Command(BaseCommand):
    help = 'Fetches text for all PDFs'

    def handle(self, *args, **options):
        extract_fulltext.delay()
