from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    class Meta:
        ordering = ['username']

    def __str__(self) -> str:
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def str(self) -> str:
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    categories = models.ManyToManyField(
        Category,
        related_name='posts'
    )
    image = models.ImageField(
        upload_to='post_images',
        default='',
        blank=True
    )

    class Meta:
        ordering = ['-created_at']

    def str(self) -> str:
        return self.title
