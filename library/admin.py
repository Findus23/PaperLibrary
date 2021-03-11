from django.contrib import admin
from django.forms import ModelForm
from djangoql.admin import DjangoQLSearchMixin

from library.models import Paper, Author, Keyword, PDF, Tag, AuthorAlias


class AddPaperForm(ModelForm):
    class Meta:
        model = Paper
        fields = ['bibcode']


class PDFInlineAdmin(admin.TabularInline):
    model = PDF
    fields = ["file", "type"]
    extra = 0


class PaperAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    # form = AddPaperForm
    fields = ["bibcode", "title", "custom_title", "first_author", "authors", "year",
              "citation_key",
              "notes_md", "tags",
              "doi", "pubdate", "entry_date", "keywords",
              "publication",
              "doctype", "arxiv_id", "citation_count", "abstract", "recommended_by",
              "bibtex"]
    readonly_fields = ["title", "first_author", "authors", "doi", "pubdate", "entry_date", "keywords", "publication",
                       "doctype", "arxiv_id", "year", "citation_count", "abstract"]
    date_hierarchy = "entry_date"
    list_filter = ["authors", "publication", "year", "tags", "keywords", "doctype"]
    list_display = ["title", "first_author", "custom_title"]
    search_fields = ["@abstract"]
    filter_horizontal = ["tags", "recommended_by", "keywords", "authors"]
    save_on_top = True
    inlines = [PDFInlineAdmin]

    def get_readonly_fields(self, request, obj=None):
        if not obj:  # editing an existing object
            return self.readonly_fields
        if not obj.bibcode:
            return []
        return self.readonly_fields + ['bibcode']


class PDFAdmin(admin.ModelAdmin):
    search_fields = ["@full_text"]


admin.site.register(Paper, PaperAdmin)
# admin.site.register(Note, NoteAdmin)
admin.site.register(Author)
admin.site.register(AuthorAlias)
admin.site.register(Keyword)
admin.site.register(Tag)
admin.site.register(PDF, PDFAdmin)
