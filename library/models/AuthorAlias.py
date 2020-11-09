from django.db import models

from library.models import Author


class AuthorAlias(models.Model):
    name = models.CharField(unique=True, max_length=1000)
    author = models.ForeignKey(Author,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
