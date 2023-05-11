from django.db import models


class Author(models.Model):
    name = models.CharField(unique=True, max_length=1000)
    pretty_name = models.CharField(max_length=1000, null=True, blank=True)
    affiliation = models.CharField(max_length=1000, null=True, blank=True)
    orcid_id = models.CharField(unique=True, max_length=100, null=True, blank=True)

    def __str__(self):
        return self.pretty_name if self.pretty_name else self.name

    def get_absolute_url(self):
        if self.orcid_id:
            return f"https://orcid.org/{self.orcid_id}"
        return f"https://ui.adsabs.harvard.edu/search/q=%20author%3A%22{self.name}%22"

    class Meta:
        ordering = ["name"]
