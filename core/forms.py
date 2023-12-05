from django import forms
from.models import CustomUser, Task, Project, EntregaTarea
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.utils.translation import gettext_lazy as _


ALLOWED_FILE_TYPES = ['pdf', 'doc', 'docx', 'txt']

class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'identity', 'email', 'password1', 'password2']
        labels = {
            'first_name': _('Nombre'),
            'last_name': _('Apellido'),
            'identity': _('Número de Documento'),
            'email': _('Correo Electrónico'),
            'password1': _('Contraseña'),
            'password2': _('Confirmación de Contraseña'),
        }
        
    widgets = {
        'first_name': forms.TextInput(attrs={'maxlength': 15}),
        'last_name': forms.TextInput(attrs={'maxlength': 15}),
        'identity': forms.TextInput(attrs={'type': 'number'}),
    }

    error_messages = {
        'password_mismatch': _('Las contraseñas no coinciden.'),
        'password_too_short': _('Tu contraseña debe tener al menos 8 caracteres.'),
        'password_entirely_numeric': _('Tu contraseña no puede ser completamente numérica.'),
        'password_common': _('Tu contraseña no puede ser una contraseña comúnmente utilizada.'),
        'identity_invalid': _('Asegúrese de que este valor es menor o igual a 10.'),
        'name_alpha': _('Este campo solo puede contener letras.'),
        'surname_alpha': _('Este campo solo puede contener letras.'),
        'identity_numeric': _('Este campo solo puede contener números.'),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].error_messages.update(self.error_messages)

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name.isalpha():
            raise forms.ValidationError(self.error_messages['name_alpha'])
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name.isalpha():
            raise forms.ValidationError(self.error_messages['surname_alpha'])
        return last_name

    def clean_identity(self):
        identity = self.cleaned_data['identity']
        if not str(identity).isdigit():
            raise forms.ValidationError(self.error_messages['identity_numeric'])
        return identity

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if len(password1) < 8:
            raise forms.ValidationError(self.error_messages['password_too_short'])
        if len(password1) > 10:
            raise forms.ValidationError(self.error_messages['password_entirely_numeric'])
        return password1

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