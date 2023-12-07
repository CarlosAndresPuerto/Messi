from django import forms
from.models import CustomUser, Task, Project, EntregaTarea
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.utils.translation import gettext_lazy as _


ALLOWED_FILE_TYPES = ['pdf', 'doc', 'docx', 'txt']

class CustomUserForm(UserCreationForm):
    is_teacher = forms.BooleanField(required=False)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'identity', 'email', 'password1', 'password2', 'is_teacher']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_teacher = self.cleaned_data['is_teacher']

        # Asignar el valor de 'identity' al campo 'username'
        user.username = self.cleaned_data['identity']

        # Si no es profesor, establece automáticamente como estudiante
        if not user.is_teacher:
            user.is_student = True

        if commit:
            user.save()

        return user



class EmailLoginForm(forms.Form):
    identity = forms.IntegerField(label="Número de documento")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
  
class CreateNewProject(forms.Form):
    name = forms.CharField(label="Nombre del Proyecto", max_length=200, widget=forms.TextInput(attrs={'class': 'input'}))
    description = forms.CharField(label="Descripcion", max_length=100, widget=forms.TextInput(attrs={'class': 'input'}))
   
class CreateTaskForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.objects.all(), label='Proyecto', empty_label=None)
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'project']
        labels = {
            'title': 'Título',
            'description': 'Descripción',
            'deadline': 'Entrega',
        }
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline']
        labels = {
            'title': 'Título',
            'description': 'Descripción',
            'deadline': 'Fecha de entrega',
        }
        widgets = {

            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class TaskSubmissionForm(forms.ModelForm):
    confirmar_entrega = forms.BooleanField(
        required=False,
        widget=forms.HiddenInput(),
        initial=True,
    )

    class Meta:
        model = EntregaTarea
        fields = ['comentarios', 'archivos_adjuntos', 'calificacion', 'anulada']

    def __init__(self, *args, **kwargs):
        super(TaskSubmissionForm, self).__init__(*args, **kwargs)

        # Hacer que el campo de calificacion sea de solo lectura si ya tiene un valor
        if self.instance and self.instance.calificacion is not None:
            self.fields['calificacion'].widget.attrs['readonly'] = True
            self.fields['calificacion'].widget.attrs['disabled'] = True

    def clean_calificacion(self):
        calificacion = self.cleaned_data['calificacion']
        # Puedes agregar validaciones personalizadas aquí si lo deseas
        return calificacion

class CalificacionForm(forms.Form):
    calificacion = forms.IntegerField(
        label='Calificación',
        required=False,
        min_value=0,
        max_value=100,
        help_text='Ingrese una calificación entre 0 y 100'
    )