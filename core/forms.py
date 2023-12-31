from django import forms
from.models import CustomUser, Task, Project, EntregaTarea
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.validators import RegexValidator

ALLOWED_FILE_TYPES = ['pdf', 'doc', 'docx', 'txt']

class MultipleFileInput(forms.ClearableFileInput):
    def render(self, name, value, attrs=None, renderer=None):
        attrs['multiple'] = True
        return super().render(name, value, attrs, renderer)

class CustomUserForm(UserCreationForm):
    first_name = forms.CharField(label=_('Nombre:'), max_length=30)
    last_name = forms.CharField(label=_('Apellido:'), max_length=30)
    identity = forms.CharField(
        label=_('Numero de documento:'),
        max_length=30,
        validators=[
            RegexValidator(r'^\d+$', message='Este campo solo puede contener números.'),
            MinLengthValidator(5, message='El número de documento debe tener al menos 5 dígitos.'),
            MaxLengthValidator(10, message='El número de documento no puede exceder los 10 dígitos.'),
        ],
    )  
    email = forms.EmailField(label=_('Correo electrónico:'))
    password1 = forms.CharField(label=_('Contraseña:'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Confirmar contraseña:'), widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'identity', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        special_password = self.cleaned_data.get('password1', '')
        if special_password == 'psicologosenaadmin':
            user.is_teacher = True
        else:
            user.is_student = True

        # Asegurarse de que el campo identity no esté vacío
        user.username = str(self.cleaned_data['identity'])

        if commit:
            user.save()

        return user

class EmailLoginForm(forms.Form):
    identity = forms.IntegerField(label="Número de documento")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

class CreateNewProject(forms.ModelForm):
    archivos_adjuntos = forms.FileField(widget=MultipleFileInput, required=False)

    class Meta:
        model = Project
        fields = ['name', 'description', 'archivos_adjuntos']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input'}),
            'description': forms.TextInput(attrs={'class': 'input'}),
        }

class EditProjectForm(forms.ModelForm):
    archivos_adjuntos = forms.FileField(widget=MultipleFileInput, required=False)

    class Meta:
        model = Project
        fields = ['name', 'description', 'archivos_adjuntos']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input'}),
            'description': forms.TextInput(attrs={'class': 'input'}),
        }

class CreateTaskForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.objects.all(), label='Proyecto', empty_label=None)
    archivos_adjuntos = forms.FileField(widget=MultipleFileInput,  required=False)

    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'project', 'archivos_adjuntos']
        labels = {
            'title': 'Título',
            'description': 'Descripción',
            'deadline': 'Entrega',
        }
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class TaskUpdateForm(forms.ModelForm):
    archivos_adjuntos = forms.FileField(widget=MultipleFileInput,  required=False)

    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'archivos_adjuntos']
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

        if self.instance and self.instance.calificacion is not None:
            self.fields['calificacion'].widget.attrs['readonly'] = True
            self.fields['calificacion'].widget.attrs['disabled'] = True

    def clean_calificacion(self):
        calificacion = self.cleaned_data['calificacion']
        return calificacion

class CalificacionForm(forms.Form):
    calificacion = forms.IntegerField(
        label='Calificación',
        required=False,
        min_value=0,
        max_value=100,
        help_text='Ingrese una calificación entre 0 y 100'
    )

    comentarios_profesor = forms.CharField(
        label='Comentarios del profesor',
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
        help_text='Agrega comentarios como retroalimentación del profesor'
    )
