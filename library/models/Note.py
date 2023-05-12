from django.db import models

from library.models import Paper


class Note(models.Model):
    text_md = models.TextField(blank=True)
    text_html = models.TextField(editable=False, blank=True)  # TODO: support HTML
    paper = models.OneToOneField(Paper, on_delete=models.CASCADE, primary_key=True, related_name="note")

    def __str__(self):
        return self.text_md[:20]

    class Meta:
        ordering = ["paper"]
