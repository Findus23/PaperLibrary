from django.db import models


class Author(models.Model):
    name = models.CharField(unique=True, max_length=1000)
    pretty_name = models.CharField(max_length=1000, null=True, blank=True)
    affiliation = models.CharField(max_length=1000, null=True, blank=True)
    orcid_id = models.CharField(unique=True, max_length=100, null=True, blank=True)

    def __str__(self):
        return self.pretty_name if self.pretty_name else self.name
