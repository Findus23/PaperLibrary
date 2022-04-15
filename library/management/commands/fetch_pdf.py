from django.core.management.base import BaseCommand

from library.tasks import fetch_pdfs


class Command(BaseCommand):
    help = 'Fetches PDFs for all papers'

    def handle(self, *args, **options):
        fetch_pdfs.delay()
