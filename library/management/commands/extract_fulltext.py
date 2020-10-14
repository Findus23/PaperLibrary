from django.core.management.base import BaseCommand

from library.models import PDF
from library.utils.pdf import pdf_to_text


class Command(BaseCommand):
    help = 'Fetches text for all PDFs'

    def handle(self, *args, **options):
        for pdf in PDF.objects.filter(full_text__exact=""):
            print(pdf)
            pdf_to_text(pdf)
