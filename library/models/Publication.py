from django.db import models


class Publication(models.Model):
    name = models.CharField(unique=True, max_length=1000)

    def __str__(self):
        return self.name
