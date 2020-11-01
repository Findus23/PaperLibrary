import hashlib

from django.db import models

from library.models import Paper
from library.utils.pdf import create_preview


class PDF(models.Model):
    file = models.FileField(upload_to="pdfs")
    sha256 = models.CharField(max_length=64, editable=False)
    full_text = models.TextField(blank=True)
    paper = models.ForeignKey(Paper, on_delete=models.PROTECT, related_name="pdfs")
    type = models.CharField(max_length=100, default="other")
    preview = models.FileField(upload_to="previews", null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file.name

    def save(self, *args, **kwargs):
        super(PDF, self).save(*args, **kwargs)
        with self.file.open("rb") as f:
            hash = hashlib.sha256()
            if f.multiple_chunks():
                for chunk in f.chunks():
                    hash.update(chunk)
            else:
                hash.update(f.read())
        self.sha256 = hash.hexdigest()
        super(PDF, self).save(*args, **kwargs)
