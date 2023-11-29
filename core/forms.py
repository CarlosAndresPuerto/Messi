from django import forms
from.models import UserCustom, Task, Project, EntregaTarea
from django.contrib.auth.forms import UserCreationForm
ALLOWED_FILE_TYPES = ['pdf', 'doc', 'docx', 'txt']



class UserCustomRegisterForm(UserCreationForm):
    first_name = forms.CharField(label="Nombre")
    last_name = forms.CharField(label="Apellido")
    email = forms.EmailField(label="Correo electrónico")
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    class Meta:
        model = UserCustom
        fields = ['first_name', 'last_name', 'identity', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class EmailLoginForm(forms.Form):
    identity = forms.IntegerField(label="Numero de documento")
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
        widget=forms.HiddenInput(),  # Utiliza un campo oculto para confirmar la entrega
        initial=True,  # Establece el valor inicial en True para indicar la confirmación
    )

    class Meta:
        model = EntregaTarea
        fields = ['comentarios', 'archivos_adjuntos', 'calificacion', 'anulada']

    def __init__(self, *args, **kwargs):
        super(TaskSubmissionForm, self).__init__(*args, **kwargs)

        # Ocultar y deshabilitar el campo de calificación para el estudiante
        if self.instance and self.instance.calificacion is not None:
            self.fields['calificacion'].widget = forms.HiddenInput()
    # Validar el campo de calificación si es necesario

    
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