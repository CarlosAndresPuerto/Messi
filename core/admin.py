from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import admin  # Agrega esta importación
from django.utils.html import format_html  # Agrega esta importación
from .models import CustomUser 

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_student', 'is_teacher_candidate', 'is_teacher', 'action_review')

    def action_review(self, obj):
        if obj.is_teacher_candidate:
            return format_html('<a class="button" href="{}">Revisar</a>', reverse('admin:review_teacher', args=[obj.pk]))
        return ''

    action_review.short_description = 'Revisión'

admin.site.register(CustomUser, CustomUserAdmin)
