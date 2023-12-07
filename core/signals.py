# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

# Elimina esta señal si ya no es necesaria
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         if instance.is_teacher:
#             # Crear o actualizar el modelo Teacher
#             teacher, _ = Teacher.objects.get_or_create(user=instance)
#             teacher.approved_by_admin = False  # Inicialmente, el profesor no está aprobado
#             teacher.save()
