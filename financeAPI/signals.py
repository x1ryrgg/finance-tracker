from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver
from .models import *
import os


@receiver(pre_delete, sender=Profile)
def image_model_delete(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(False)