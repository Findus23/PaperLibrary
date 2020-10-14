from django.db import models


class Keyword(models.Model):
    name = models.CharField(unique=True, max_length=1000)
    schema = models.CharField(max_length=1000)

    def __str__(self):
        return self.name
