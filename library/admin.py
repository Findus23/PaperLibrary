from django.contrib import admin
# Register your models here.
from django.forms import ModelForm
from djangoql.admin import DjangoQLSearchMixin

from library.models import Paper, Author, Keyword, PDF


class AddPaperForm(ModelForm):
    class Meta:
        model = Paper
        fields = ['bibcode']


class PaperAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    form = AddPaperForm
    readonly_fields = ["title", "first_author", "authors", "doi", "pubdate", "entry_date", "keywords", "publication",
                       "doctype", "arxiv_id", "bibtex"]
    date_hierarchy = "entry_date"
    list_filter = ["authors", "publication", "year", "keywords", "doctype"]
    list_display = ["title", "first_author"]
    search_fields = ["@abstract"]
    save_on_top = True


class PDFAdmin(admin.ModelAdmin):
    search_fields = ["@full_text"]


admin.site.register(Paper, PaperAdmin)
admin.site.register(Author)
admin.site.register(Keyword)
admin.site.register(PDF, PDFAdmin)

# Paper.objects.filter(pubdate__month=)
