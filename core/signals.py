from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print("Is teacher:", instance.is_teacher)  # Agrega esta línea
        if instance.is_teacher and not instance.teacher_password:
            instance.set_password('psicologosenaadmin')
        instance.save()
