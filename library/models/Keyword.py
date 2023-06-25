from django.db import models


class Keyword(models.Model):
    name = models.CharField(max_length=1000)
    kw_schema = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        unique_together = [["name", "kw_schema"]]
