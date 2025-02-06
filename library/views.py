# Create your views here.
from django.db.models import Prefetch
from django.http import HttpResponse, HttpRequest
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from library.models import Paper, Author, Keyword, PDF, Note
from library.serializers import PaperSerializer, AuthorSerializer, PDFSerializer, KeywordSerializer, NoteSerializer
from library.utils.bibtex import papers_to_bibtex_file


class PaperViewSet(viewsets.ModelViewSet):
    queryset = (Paper.objects.all()
                .select_related("first_author")
                .select_related("publication")
                .select_related("doctype")
                .select_related("note")
                .prefetch_related("pdfs")
                .prefetch_related("authors")
                .prefetch_related("tags")
                .prefetch_related("keywords")
                .prefetch_related("recommended_by")
                )
    serializer_class = PaperSerializer
    permission_classes = [permissions.IsAuthenticated]


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = (Author.objects.all()
    .prefetch_related(Prefetch(
        "papers", queryset=Paper.objects.defer("abstract", "bibtex")
    ))
    .prefetch_related(Prefetch(
        "papers__pdfs", queryset=PDF.objects.defer("full_text")
    ))
    )
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]


class KeywordViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.all().prefetch_related("papers").prefetch_related("papers__pdfs")
    serializer_class = KeywordSerializer
    permission_classes = [permissions.IsAuthenticated]


class PDFViewSet(viewsets.ModelViewSet):
    queryset = PDF.objects.all()
    serializer_class = PDFSerializer
    permission_classes = [permissions.IsAuthenticated]


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def bibtex(request: HttpRequest):
    tag = request.GET.get("tag", None)
    if tag:
        query = Paper.objects.filter(tags__name=tag)
    else:
        query = Paper.objects.all()

    code = papers_to_bibtex_file(query)
    return HttpResponse(code, content_type="text/plain")
