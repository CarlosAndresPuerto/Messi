from django import forms
from.models import UserCustom, Task, Project
from django.contrib.auth.forms import UserCreationForm


class UserCustomRegisterForm(UserCreationForm):
    first_name = forms.CharField(label="Nombre")
    last_name = forms.CharField(label="Apellido")
    email = forms.EmailField(label="Correo electrónico")
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)
    class Meta:
        model = UserCustom
        fields = ['first_name','last_name', 'identity', 'email', 'password1', 'password2']

class EmailLoginForm(forms.Form):
    identity = forms.IntegerField(label="Numero de documento")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
   
class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'project']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

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

class TaskSubmissionForm(forms.ModelForm):
    additional_notes = forms.CharField(label='Notas Adicionales', required=False, widget=forms.Textarea)

    class Meta:
        model = Task
        fields = ['attachment', 'additional_notes']
        labels = {
            'attachment':'Archivos adjuntos',
        }

class CreateNewProject(forms.Form):
    name = forms.CharField(label="Nombre del Proyecto", max_length=200, widget=forms.TextInput(attrs={'class': 'input'}))
    description = forms.CharField(label="Descripcion", max_length=100, widget=forms.TextInput(attrs={'class': 'input'}))

class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'done', 'deadline']
        labels = {
            'title': 'Título',
            'description': 'Descripción',
            'done': 'Completada',
        }
        widgets = {
            'done': forms.RadioSelect(choices=[(True, 'Sí'), (False, 'No')]),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

