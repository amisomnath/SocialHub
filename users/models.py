from django.contrib.auth.models import AbstractUser
from django.db import models
from constants.users import GENDER_CHOICES


class CustomUser(AbstractUser):
    is_agreed = models.BooleanField(verbose_name='Agree with Terms & Conditions', default=False)
    age = models.PositiveSmallIntegerField(blank=True, default=0)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    is_account_active = models.BooleanField(blank=True, null=True, default=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.email


class BlockedUser(models.Model):
    blocker = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blocked_users')
    blocked_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blockers')
    blocked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id
