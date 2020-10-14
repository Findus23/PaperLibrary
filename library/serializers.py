from rest_framework import serializers

from library.models import Paper, Author, Keyword, PDF, DocType, Publication


class PDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDF
        exclude = ["full_text", "paper"]


class SimplePaperSerializer(serializers.HyperlinkedModelSerializer):
    pdfs = PDFSerializer(many=True)

    class Meta:
        model = Paper
        fields = ["id", "url", "title", "pdfs", "doi"]


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    papers = SimplePaperSerializer(many=True)

    class Meta:
        model = Author
        fields = "__all__"


class KeywordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Keyword
        fields = "__all__"


class PaperSerializer(serializers.HyperlinkedModelSerializer):
    keywords = serializers.SlugRelatedField("name", many=True, queryset=Keyword.objects.all())
    authors = serializers.SlugRelatedField("name", many=True, queryset=Author.objects.all())
    first_author = serializers.SlugRelatedField("name", queryset=Author.objects.all())
    publication = serializers.SlugRelatedField("name", queryset=Publication.objects.all())
    doctype = serializers.SlugRelatedField("name", queryset=DocType.objects.all())
    pdfs = PDFSerializer(many=True)

    class Meta:
        model = Paper
        exclude = ["abstract", "bibtex"]
