from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=User)
def username_check(sender, instance, *args, **kwargs):
    if not instance.pk and not instance.username:
        instance.username = instance.email
