# Create your views here.
from django.http import HttpResponse, HttpRequest
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view

from library.models import Paper, Author, Keyword, PDF, Note
from library.serializers import PaperSerializer, AuthorSerializer, PDFSerializer, KeywordSerializer, NoteSerializer


class PaperViewSet(viewsets.ModelViewSet):
    queryset = Paper.objects.all().select_related("first_author") \
        .select_related("publication").select_related("doctype").select_related("note") \
        .prefetch_related("pdfs").prefetch_related("authors").prefetch_related("tags") \
        .prefetch_related("keywords").prefetch_related("recommended_by")
    serializer_class = PaperSerializer
    permission_classes = [permissions.IsAuthenticated]


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().prefetch_related("papers").prefetch_related("papers__pdfs")
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
def bibtex(request: HttpRequest):
    tag = request.GET.get("tag", None)
    if tag:
        query = Paper.objects.filter(tags__name=tag)
    else:
        query = Paper.objects.all()

    code = "% Encoding: UTF-8\n\n"
    for paper in query.order_by("citation_key"):
        code += paper.bibtex + "\n\n"

    code += "@Comment{jabref-meta: databaseType:biblatex;}\n"
    return HttpResponse(code, content_type="text/plain")
