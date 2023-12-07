# core/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import CustomUser
from django.urls import reverse
from django.http import HttpResponse


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_student', 'is_teacher_candidate_display', 'is_teacher', 'action_review')

    def is_teacher_candidate_display(self, obj):
        return obj.is_teacher_candidate

    is_teacher_candidate_display.short_description = 'Is Teacher Candidate'


    @admin.action(description='Revisión')
    def action_review(self, request, queryset=None):
        if not queryset:
            self.message_user(request, "No se seleccionaron usuarios para revisar.", level='warning')
            return HttpResponse()  # Cambiado a HttpResponse

        for user in queryset:
            if user.is_teacher_candidate:
                teacher = user.teacher
                teacher.approved_by_admin = True  # Aprobado por el administrador
                teacher.save()
                message = f"Se aprobó a {user.username} como profesor."
                self.message_user(request, message, level='success')
            else:
                message = f"{user.username} no es candidato a profesor."
                self.message_user(request, message, level='info')

        return HttpResponse()  # Cambiado a HttpResponse

    action_review.short_description = 'Revisión'
    


# Registra la clase CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
