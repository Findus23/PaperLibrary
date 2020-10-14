from django.core.management.base import BaseCommand

from library.models import PDF
from library.utils.pdf import create_preview


class Command(BaseCommand):
    help = 'create previews for all PDFs'

    def handle(self, *args, **options):
        for pdf in PDF.objects.all():
            print(pdf)
            pdf.preview.delete()
            create_preview(pdf)
