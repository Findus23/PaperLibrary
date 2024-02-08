from django.db import transaction
from django_rq import job

from citenames.citenames import run_tex
from library.models import PDF, Paper
from library.utils.bibtex import papers_to_bibtex_file
from library.utils.pdf import create_preview, pdf_to_text, fetch_arxiv_pdf


@job
def create_previews():
    for pdf in PDF.objects.all():
        print(pdf)
        pdf.preview.delete()
        create_preview(pdf)


@job
def extract_fulltext():
    for pdf in PDF.objects.filter(full_text__exact=""):
        print(pdf)
        pdf_to_text(pdf)


@job
def fetch_pdfs():
    for paper in Paper.objects.filter(pdfs=None):
        print(paper)
        if not paper.arxiv_id:
            continue
        fetch_arxiv_pdf(paper)
    extract_fulltext.delay()


@job
def update_citenames():
    query = Paper.objects.all()

    bibtex = papers_to_bibtex_file(query)
    with_key_query = query.exclude(bibcode__isnull=True)
    keys = []

    for citekey, bibcode in with_key_query.values_list('citation_key', 'bibcode'):
        if citekey is None:
            keys.append(bibcode)
            continue
        keys.append(citekey)
    citenames = run_tex(bibtex, keys)
    with transaction.atomic():
        updated_papers = []
        for paper in with_key_query:
            paper.citename = citenames[paper.citation_key_or_bibcode]
            updated_papers.append(paper)
        Paper.objects.bulk_update(updated_papers, ["citename"])
