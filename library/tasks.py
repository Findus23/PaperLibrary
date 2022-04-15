from celery import shared_task

from library.models import PDF, Paper
from library.utils.pdf import create_preview, pdf_to_text, fetch_arxiv_pdf


@shared_task
def create_previews():
    for pdf in PDF.objects.all():
        print(pdf)
        pdf.preview.delete()
        create_preview(pdf)


@shared_task
def extract_fulltext():
    for pdf in PDF.objects.filter(full_text__exact=""):
        print(pdf)
        pdf_to_text(pdf)


@shared_task
def fetch_pdfs():
    for paper in Paper.objects.filter(pdfs=None):
        print(paper)
        if not paper.arxiv_id:
            continue
        fetch_arxiv_pdf(paper)
    extract_fulltext.delay()
