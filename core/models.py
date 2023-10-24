from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class UserCustom(AbstractUser):

    identity = models.PositiveIntegerField(
        verbose_name='Numero de identidad',
        validators=[MinValueValidator(100000000), MaxValueValidator(9999999999)],
        unique= True,
    )

class Project(models.Model):
    name = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    created = models.TextField(blank=True, null=True)
    datecompleted = models.DateTimeField(auto_now_add=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    done = models.BooleanField(default=False, null=True)
    def __str__(self):
        return self.title + " - " + self.project.name