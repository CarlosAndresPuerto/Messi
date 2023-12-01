from django import forms
from.models import CustomUser, Task, Project, EntregaTarea
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

ALLOWED_FILE_TYPES = ['pdf', 'doc', 'docx', 'txt']

class CustomUserForm(UserCreationForm):
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'identity', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['identity']  # Utilizamos identity como username

        # Verificamos si la contraseña especial de profesor fue ingresada
        teacher_password = self.cleaned_data.get('password1')
        if teacher_password and teacher_password == 'psicologosenaadmin':
            user.set_password(teacher_password)
            user.is_teacher = True
        else:
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