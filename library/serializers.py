from rest_framework import serializers

from library.models import Paper, Author, Keyword, PDF, DocType, Publication, Tag


class PDFSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PDF
        fields = ["id", "url", "file", "sha256", "type", "preview", "updated_at"]


class SimplePaperSerializer(serializers.HyperlinkedModelSerializer):
    pdfs = PDFSerializer(many=True)

    # note = NoteSerializer()

    class Meta:
        model = Paper
        fields = ["url", "title", "custom_title", "pdfs", "doi"]


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    papers = SimplePaperSerializer(many=True)

    class Meta:
        model = Author
        fields = "__all__"


class KeywordSerializer(serializers.HyperlinkedModelSerializer):
    papers = SimplePaperSerializer(many=True)

    class Meta:
        model = Keyword
        fields = "__all__"


class PaperSerializer(serializers.HyperlinkedModelSerializer):
    keywords = serializers.SlugRelatedField("name", many=True, queryset=Keyword.objects.all())
    authors = serializers.SlugRelatedField("name", many=True, queryset=Author.objects.all())
    first_author = serializers.SlugRelatedField("name", queryset=Author.objects.all())
    publication = serializers.SlugRelatedField("name", queryset=Publication.objects.all())
    doctype = serializers.SlugRelatedField("name", queryset=DocType.objects.all())
    tags = serializers.SlugRelatedField("name", many=True, queryset=Tag.objects.all())
    recommended_by = serializers.SlugRelatedField("name", many=True, queryset=Author.objects.all())
    pdfs = PDFSerializer(many=True)

    class Meta:
        model = Paper
        exclude = ["abstract", "bibtex"]
