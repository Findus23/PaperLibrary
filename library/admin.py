from django.contrib import admin
from django.forms import ModelForm
from djangoql.admin import DjangoQLSearchMixin

from library.models import Paper, Author, Keyword, PDF, Tag, AuthorAlias, Publication, DocType, Note


class AddPaperForm(ModelForm):
    class Meta:
        model = Paper
        fields = ['bibcode']


class PDFInlineAdmin(admin.TabularInline):
    model = PDF
    fields = ["file", "type"]
    extra = 0


class NoteInline(admin.StackedInline):
    model = Note


class PaperAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    # form = AddPaperForm
    fields = ["bibcode", "title", "custom_title", "first_author", "authors", "year",
              "citation_key", "tags",
              "doi", "pubdate", "entry_date", "keywords", "publication",
              "doctype", "arxiv_id", "citation_count", "abstract", "recommended_by",
              "bibtex"]
    readonly_fields = ["title", "first_author", "authors", "doi", "pubdate", "entry_date", "keywords", "publication",
                       "doctype", "arxiv_id", "year", "citation_count", "abstract"]
    date_hierarchy = "entry_date"
    list_filter = ["tags", "doctype", "arxiv_class", "publication", "year",
                   ("pdfs", admin.EmptyFieldListFilter), ("arxiv_id", admin.EmptyFieldListFilter),
                   ("doi", admin.EmptyFieldListFilter),
                   "keywords", "authors"]
    list_display = ["title", "first_author", "citation_key"]
    search_fields = ["@abstract"]
    filter_horizontal = ["tags", "recommended_by", "keywords", "authors"]
    save_on_top = True
    inlines = [PDFInlineAdmin, NoteInline]

    def get_readonly_fields(self, request, obj=None):
        if not obj:  # editing an existing object
            return self.readonly_fields
        if not obj.bibcode:
            return []
        return self.readonly_fields + ['bibcode']


class PDFAdmin(admin.ModelAdmin):
    search_fields = ["@full_text"]
    list_filter = ["type", ("preview", admin.EmptyFieldListFilter), ("full_text", admin.EmptyFieldListFilter)]
    date_hierarchy = "updated_at"
    readonly_fields = ["updated_at", "sha256"]


class AuthorAdmin(admin.ModelAdmin):
    list_filter = [("affiliation", admin.EmptyFieldListFilter), ("orcid_id", admin.EmptyFieldListFilter), "affiliation"]


class KeywordAdmin(admin.ModelAdmin):
    list_filter = ["kw_schema"]


class AuthorAliasAdmin(admin.ModelAdmin):
    list_display = ["name", "author"]


class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]


admin.site.register(Paper, PaperAdmin)
# admin.site.register(Note, NoteAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(AuthorAlias, AuthorAliasAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Publication)
admin.site.register(DocType)
admin.site.register(PDF, PDFAdmin)
