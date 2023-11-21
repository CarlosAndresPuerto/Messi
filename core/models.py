from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import FileExtensionValidator



class UserCustom(AbstractUser):
    identity = models.PositiveIntegerField(
        verbose_name='Numero de identidad',
        validators=[MinValueValidator(100000000), MaxValueValidator(9999999999)],
        unique=True,
    )
    first_name = models.CharField(max_length=30) 
    last_name = models.CharField(max_length=30)
    is_superadmin = models.BooleanField(default=False)

    def __str__(self):
        return self.username  

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
    deadline = models.DateTimeField(null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    attachment = models.FileField(upload_to='task_attachments/', null=True, blank=True)
    additional_notes = models.TextField(blank=True, null=True) 
 

    done = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.title + " - " + self.project.name
    
class EntregaTarea(models.Model):
    tarea = models.ForeignKey(Task, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    entregada = models.BooleanField(default=False)
    confirmada = models.BooleanField(default=False)  # Nuevo campo para confirmar tarea
    fecha_entrega = models.DateTimeField(null=True, blank=True)

    def con_retraso(self):
        return self.entregada and self.fecha_entrega > self.tarea.datecompleted

    def get_tarea_info(self):
        return f"{self.tarea.title} - {self.tarea.project.name}"

