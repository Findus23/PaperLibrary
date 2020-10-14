import ads
from ads.search import Article
from django.db import models

from library.models import Author, Keyword, Publication, DocType
from paperlibrary.settings import ADS_AUTH_TOKEN


class Paper(models.Model):
    title = models.CharField(max_length=1000)
    abstract = models.TextField()
    doi = models.CharField(unique=True, max_length=50)
    bibtex = models.TextField()
    first_author = models.ForeignKey(Author, on_delete=models.RESTRICT)
    authors = models.ManyToManyField(Author, related_name="papers")
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    doctype = models.ForeignKey(DocType, on_delete=models.CASCADE)
    arxiv_id = models.CharField(unique=True, max_length=10)
    bibcode = models.CharField(unique=True, max_length=20)
    year = models.IntegerField()
    pubdate = models.DateField()
    entry_date = models.DateField()
    citation_count = models.IntegerField()
    keywords = models.ManyToManyField(Keyword, related_name="papers")

    def __str__(self):
        return self.title

    @property
    def arxiv_url(self):
        if not self.arxiv_id:
            return None
        return f"https://arxiv.org/abs/{self.arxiv_id}"

    @property
    def arxiv_pdf_url(self):
        if not self.arxiv_id:
            return None
        return f"https://export.arxiv.org/pdf/{self.arxiv_id}.pdf"

    def save(self, *args, **kwargs):
        if self.id:
            return super(Paper, self).save(*args, **kwargs)

        ads.config.token = ADS_AUTH_TOKEN
        cols = [
            "title", "author", "first_author", "year", "bibcode", "id", "pubdate", "doi",
            "identifier", "pub", "citation_count", "abstract", "bibtex", "doctype", "keyword"
        ]
        # ads.ExportQuery
        papers = ads.SearchQuery(doi=self.doi, fl=cols)
        paper: Article = next(papers)
        self.title = paper.title[0]
        self.publication, _ = Publication.objects.get_or_create(name=paper.pub)
        self.abstract = paper.abstract
        self.bibtex = paper.bibtex
        self.year = int(paper.year)
        self.entry_date = paper._get_field("entry_date").replace("T00:00:00Z", "")
        self.citation_count = int(paper.citation_count)
        self.doctype, _ = DocType.objects.get_or_create(name=paper.doctype)
        self.first_author, _ = Author.objects.get_or_create(name=paper.first_author)

        self.year = paper.year
        self.pubdate = paper.pubdate.replace("-00", "-01").replace("T", "")
        if paper.doi and len(paper.doi) > 0:
            self.doi = paper.doi[0]
        else:
            self.doi = None
        arxiv_papers = [ident for ident in paper.identifier if "arXiv:" in ident]
        if len(arxiv_papers) > 0:
            self.arxiv_id = arxiv_papers[0].split("arXiv:")[-1]
        else:
            self.arxiv_id = None

        super(Paper, self).save(*args, **kwargs)
        for author_name in paper.author:
            author, created = Author.objects.get_or_create(name=author_name)
            self.authors.add(author)

        for kw in zip(paper.keyword, paper._get_field("keyword_schema")):
            keyword_name, keyword_schema = kw
            keyword, created = Keyword.objects.get_or_create(name=keyword_name, schema=keyword_schema)
            self.keywords.add(keyword)
