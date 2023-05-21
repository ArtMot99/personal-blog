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
        ordering = ["name"]

    def str(self) -> str:
        return self.name
