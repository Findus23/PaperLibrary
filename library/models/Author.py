from django.db import models


class Author(models.Model):
    name = models.CharField(unique=True, max_length=1000)
    affiliation = models.CharField(max_length=1000, null=True, blank=True)
    orcid_id = models.CharField(unique=True, max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
