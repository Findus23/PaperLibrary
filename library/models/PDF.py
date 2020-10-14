from django.db import models

from library.models import Paper


class PDF(models.Model):
    file = models.FileField(upload_to="pdfs")
    sha265 = models.CharField(max_length=64, editable=False)
    full_text = models.TextField(blank=True)
    paper = models.ForeignKey(Paper, on_delete=models.PROTECT, related_name="pdfs")
    type = models.CharField(max_length=100, default="other")
    preview = models.FileField(upload_to="previews", null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file.name
