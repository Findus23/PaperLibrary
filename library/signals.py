from django.db.models.base import ModelBase
from django.db.models.signals import post_save, ModelSignal
from django.dispatch import receiver

from library.models import Paper
from library.tasks import update_citenames


@receiver(post_save, sender=Paper)
def post_paper_save(
        signal: ModelSignal,
        sender: ModelBase,
        instance: Paper,
        created: bool,
        raw: bool,
        using: str,
        update_fields,
        **kwargs
):
    if raw:
        return
    update_citenames.delay()
