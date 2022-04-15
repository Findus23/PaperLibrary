from django.db import models

from library.models import Author


class AuthorAlias(models.Model):
    name = models.CharField(unique=True, max_length=1000)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Author alias"
        verbose_name_plural = "Author aliases"

    def __str__(self):
        return self.name
