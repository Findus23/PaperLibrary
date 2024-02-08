import re

import ads
import django_rq
from ads.search import Article
from django.core.exceptions import ValidationError
from django.db import models

from library.models import Author, Keyword, Publication, DocType, Tag, AuthorAlias
from paperlibrary.settings import ADS_AUTH_TOKEN


def get_or_create_author(name: str):
    try:
        return Author.objects.get(name=name)
    except Author.DoesNotExist:
        try:
            return AuthorAlias.objects.get(name=name).author
        except AuthorAlias.DoesNotExist:
            return Author.objects.create(name=name)


def valid_bibtex_key(key: str) -> None:
    if " " in key:
        raise ValidationError("key is not allowed to contain spaces")
    for character in ["\"#'(),={}%"]:
        if character in key:
            raise ValidationError(f"key is not allowed to contain {character}")


def merge_fields(*args):
    for value in args:
        if value != "-" and value is not None:
            return value


def fix_none_for_zip(*args):
    fixed_args = []
    length = len(args[0])
    for a in args:
        if a is None:
            a = [None] * length
        fixed_args.append(a)
    return fixed_args


class Paper(models.Model):
    title = models.CharField(max_length=1000)
    abstract = models.TextField(null=True)
    bibcode = models.CharField(unique=True, max_length=50, null=True, blank=True)
    doi = models.CharField(unique=True, max_length=50, null=True)
    bibtex = models.TextField(blank=True)
    first_author = models.ForeignKey(Author, on_delete=models.RESTRICT, related_name="first_author_papers")
    authors = models.ManyToManyField(Author, related_name="papers")
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    doctype = models.ForeignKey(DocType, on_delete=models.CASCADE)
    arxiv_id = models.CharField(unique=True, max_length=20, blank=True, null=True)
    arxiv_class = models.CharField(null=True)
    year = models.IntegerField()
    pubdate = models.DateField()
    entry_date = models.DateField()
    citation_count = models.IntegerField(null=True, blank=True)
    keywords = models.ManyToManyField(Keyword, related_name="papers")
    custom_title = models.CharField(max_length=1000, blank=True)
    recommended_by = models.ManyToManyField(Author, related_name="recommendations", blank=True)
    tags = models.ManyToManyField(Tag, related_name="notes", blank=True)
    citation_key = models.CharField(max_length=50, unique=True, blank=True, null=True, validators=[valid_bibtex_key])
    ads_version = models.PositiveBigIntegerField()
    citename = models.CharField(max_length=1000, blank=True, null=True, editable=False)

    class Meta:
        ordering = ["title"]

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

    @property
    def ads_url(self):
        return f"https://ui.adsabs.harvard.edu/abs/{self.bibcode}/abstract"

    @property
    def citation_key_or_pk(self):
        if self.citation_key is not None:
            return self.citation_key
        return self.pk

    def save(self, *args, **kwargs):
        ads.config.token = ADS_AUTH_TOKEN
        bibtex_regex = re.compile(r"(@\w+{)(\S+),")
        self.bibtex = bibtex_regex.sub(f"\\g<1>{self.citation_key_or_pk},", self.bibtex, 1)
        insert = True
        if self.id:
            insert = False
            papers = ads.SearchQuery(bibcode=self.bibcode, fl=["_version_"])
            paper: Article = next(papers)
            if self.ads_version == paper._raw["_version_"]:
                return super(Paper, self).save(*args, **kwargs)

        if not self.bibcode:
            otherpublication, _ = Publication.objects.get_or_create(name="other")
            self.publication = otherpublication
            otherdoctype, _ = DocType.objects.get_or_create(name="other")
            self.doctype = otherdoctype
            self.year = 2020
            self.title = self.custom_title or ""
            self.pubdate = self.entry_date = "2020-01-01"
            otherauthor, _ = Author.objects.get_or_create(name="unknown")
            self.first_author = otherauthor
            return super(Paper, self).save(*args, **kwargs)

        cols = [
            "title", "author", "first_author", "year", "bibcode", "id", "pubdate", "doi",
            "identifier", "pub", "citation_count", "abstract", "bibtex", "doctype", "keyword",
            "orcid_pub", "orcid_user", "orcid_other", "aff", "_version_", "arxiv_class", "entry_date",
            "keyword_schema"
        ]

        print(self.bibcode)
        papers = ads.SearchQuery(bibcode=self.bibcode, fl=cols)
        paper: Article = next(papers)

        self.ads_version = paper._raw["_version_"]

        self.title = paper.title[0]
        self.publication, _ = Publication.objects.get_or_create(name=paper.pub)
        self.abstract = paper.abstract
        bibtex_query = ads.ExportQuery(self.bibcode)
        self.bibtex = bibtex_query.execute()
        self.bibtex = bibtex_regex.sub(f"\\g<1>{self.citation_key_or_pk},", self.bibtex, 1)
        self.year = int(paper.year)
        self.entry_date = paper._get_field("entry_date").split("T")[0]
        self.citation_count = int(paper.citation_count)
        self.doctype, _ = DocType.objects.get_or_create(name=paper.doctype)
        self.first_author = get_or_create_author(name=paper.first_author)

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
        if paper.arxiv_class:
            self.arxiv_class = paper.arxiv_class[0]

        super(Paper, self).save(*args, **kwargs)
        for author_name, o1, o2, o3, aff in zip(*fix_none_for_zip(
                paper.author,
                paper.orcid_pub, paper.orcid_user, paper.orcid_other,
                paper.aff
        )):
            orcid_id = merge_fields(o1, o3)
            if orcid_id:
                try:
                    author = Author.objects.get(orcid_id=orcid_id)
                except Author.DoesNotExist:
                    author = get_or_create_author(name=author_name)
                    author.orcid_id = orcid_id
                    author.save()
            else:
                author = get_or_create_author(name=author_name)
            author.affiliation = aff
            author.save()
            self.authors.add(author)
        if paper._get_field("keyword_schema"):
            for kw in zip(paper.keyword, paper._get_field("keyword_schema")):
                keyword_name, keyword_schema = kw
                keyword, created = Keyword.objects.get_or_create(
                    name=keyword_name, kw_schema=keyword_schema, defaults={"name": keyword_name}
                )
                self.keywords.add(keyword)
        if insert:
            queue = django_rq.get_queue()
            queue.enqueue("library.tasks.fetch_pdfs")
