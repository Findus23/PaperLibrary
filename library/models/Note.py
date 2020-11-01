from django.db import models

from library.models import Paper, Author


class Note(models.Model):
    paper = models.OneToOneField(Paper, on_delete=models.CASCADE, primary_key=True)
    custom_title = models.CharField(max_length=1000, blank=True)
    notes_md = models.TextField(blank=True)
    notes_html = models.TextField(editable=False, blank=True)  # TODO: support HTML
    recommended_by = models.ManyToManyField(Author, related_name="recommendations", blank=True)

    # def clean(self):
    #     self.notes_html = md_to_html(self.notes_html)

    def __str__(self):
        return self.paper.title
