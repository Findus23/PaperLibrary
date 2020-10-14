from django.core.management.base import BaseCommand

from library.models import Paper
from library.utils.pdf import fetch_arxiv_pdf


class Command(BaseCommand):
    help = 'Fetches PDFs for all papers'

    def handle(self, *args, **options):
        for paper in Paper.objects.filter(pdfs=None):
            print(paper)
            fetch_arxiv_pdf(paper)
