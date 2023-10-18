from django.db import models
from users.models import CustomUser


# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='post_for_posting')
    is_deleted = models.BooleanField(null=True, blank=True, default=False)
    tags = models.ForeignKey(
        Tag,on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='tag_for_posting')

    def __int__(self):
        return self.id
