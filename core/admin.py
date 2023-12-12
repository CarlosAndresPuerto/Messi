from django.contrib import admin, messages
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_student', 'is_teacher')

# Registra la clase CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
