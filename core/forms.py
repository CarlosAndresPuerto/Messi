from django import forms
from.models import UserCustom, Task
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
    identity = forms.IntegerField()
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
   


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'project']
 
class CreateNewProject(forms.Form):
    name = forms.CharField(label="Nombre del Proyecto", max_length=200, widget=forms.TextInput(attrs={'class': 'input'}))