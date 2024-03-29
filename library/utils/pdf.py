import hashlib
from subprocess import run
from tempfile import TemporaryFile

from alive_progress import alive_bar
from django.core.files import File
from wand.image import Image

from library.models import Paper, PDF
from library.utils.http import requests_session


def fetch_arxiv_pdf(paper: Paper) -> None:
    if not paper.arxiv_id:
        raise ValueError("no arxiv id given")
    with TemporaryFile("rb+") as fd:
        print(paper.arxiv_pdf_url)
        r = requests_session.get(paper.arxiv_pdf_url)
        sha256 = hashlib.sha256()
        if "Content-Length" in r.headers:
            size = int(r.headers["Content-Length"])
        else:
            size = None
        with alive_bar(size) as bar:
            for chunk in r.iter_content(chunk_size=1):
                fd.write(chunk)
                sha256.update(chunk)
                bar()
        pdf_file = File(fd)
        pdf_obj = PDF()
        pdf_obj.file.save(f"{paper.arxiv_id}.pdf", pdf_file, save=False)
        pdf_obj.sha256 = sha256.hexdigest()
        pdf_obj.type = "arxiv"
        pdf_obj.paper = paper
        pdf_obj.save()


def create_preview(pdf: PDF, width=1000) -> None:
    with Image(filename=f"pdf:{pdf.file.path}[0]", resolution=200) as img:
        img.trim(fuzz=0.2)
        img.format = "png"
        # new_height = width / img.width * img.height
        # img.thumbnail(width=width, height=int(new_height))
        with TemporaryFile("rb+") as tf:
            img.save(tf)
            preview = File(tf)
            pdf.preview.save(f"{pdf.paper.arxiv_id}.png", preview)
            run(["optipng", pdf.preview.path])


def pdf_to_text(pdf: PDF) -> None:
    output = run(["pdftotext", pdf.file.path, "-"], capture_output=True)
    pdf.full_text = output.stdout.decode().replace("\n", " ")
    pdf.save()
