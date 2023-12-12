from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
import uuid
from django.utils.deconstruct import deconstructible
import os
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import PermissionsMixin


@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = f"{uuid.uuid4().hex}.{ext}"
        return os.path.join(self.path, filename)

upload_path = PathAndRename("archivos/")

def validate_alpha(value):
    if not value.isalpha():
        raise ValidationError('Este campo solo puede contener letras.')

def validate_numeric(value):
    if not str(value).isdigit():
        raise ValidationError('Este campo solo puede contener números.')

class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    identity = models.CharField(max_length=20, unique=True, null=True)
    email = models.EmailField(max_length=50, unique=True, null=True)

class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)

class Project(models.Model):
    name = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    teacher = models.ForeignKey('core.Teacher', on_delete=models.SET_NULL, null=True, default=None)
    archivos_adjuntos = models.FileField(upload_to='archivos/', blank=True, null=True)


    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    created = models.TextField(blank=True, null=True)
    datecompleted = models.DateTimeField(auto_now_add=True, null=True)
    deadline = models.DateTimeField(null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    attachment = models.FileField(upload_to='task_attachments/', null=True, blank=True)
    additional_notes = models.TextField(blank=True, null=True)
    done = models.BooleanField(default=False, null=True)
    archivos_adjuntos = models.FileField(upload_to='archivos/', blank=True, null=True)


    def __str__(self):
        title = self.title if self.title else "Sin título"
        project_name = self.project.name if self.project and self.project.name else "Sin proyecto"
        return f"{title} - {project_name}"

class EntregaTarea(models.Model):
    tarea = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)
    estudiante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    entregada = models.BooleanField(default=False)
    fecha_entrega = models.DateTimeField(auto_now_add=True, null=True)
    comentarios = models.TextField(blank=True, null=True)
    comentarios_profesor = models.TextField(blank=True, null=True)  # Nuevo campo para comentarios del profesor
    archivos_adjuntos = models.FileField(upload_to='archivos/', blank=True, null=True)
    calificacion = models.IntegerField(blank=True, null=True)
    bloqueada = models.BooleanField(default=False, null=True)
    anulada = models.BooleanField(default=False, null=True)

    def con_retraso(self):
        return self.entregada and self.fecha_entrega > self.tarea.datecompleted

    def get_tarea_info(self):
        return f"{self.tarea.title} - {self.tarea.project.name}"

    def save(self, *args, **kwargs):
        self.entregada = True
        super(EntregaTarea, self).save(*args, **kwargs)

    def __str__(self):
        return self.get_tarea_info()