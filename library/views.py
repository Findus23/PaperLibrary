# Create your views here.
from django.http import HttpResponse
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view

from library.models import Paper, Author, Keyword, PDF
from library.serializers import PaperSerializer, AuthorSerializer, PDFSerializer, KeywordSerializer


class PaperViewSet(viewsets.ModelViewSet):
    queryset = Paper.objects.all().select_related("first_author") \
        .select_related("publication").select_related("doctype") \
        .prefetch_related("pdfs").prefetch_related("authors") \
        .prefetch_related("keywords")
    serializer_class = PaperSerializer
    permission_classes = [permissions.IsAuthenticated]


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]


class KeywordViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer
    permission_classes = [permissions.IsAuthenticated]


class PDFViewSet(viewsets.ModelViewSet):
    queryset = PDF.objects.all()
    serializer_class = PDFSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
def bibtex(request):
    code = "% Encoding: UTF-8\n\n"
    for paper in Paper.objects.all().order_by("citation_key"):
        code += paper.bibtex + "\n\n"

    code += "@Comment{jabref-meta: databaseType:biblatex;}\n"
    return HttpResponse(code, content_type="text/plain")
