from django.shortcuts import render, redirect
from .forms import UserCustomRegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import EmailLoginForm
from django.contrib.auth.decorators import login_required
from .models import Project, Task
from .forms import CreateNewProject, CreateNewTask
from django.shortcuts import render, redirect, get_object_or_404

#Registro de usuario
def register(request):
    if request.method == "POST":
        form = UserCustomRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            identity = form.cleaned_data.get('identity')
            messages.success(request, f'Cuenta creada para {identity}!')
            return redirect('login')
    else:
        form = UserCustomRegisterForm()
    return render(request, 'crear_cuenta.html', {'form': form})



#Inicio de sesión
def user_login(request):
    if request.method == "POST":
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            identity = form.cleaned_data['identity']
            password = form.cleaned_data['password']
            user = authenticate(request, identity=identity, password=password)
            if user is not None:
                messages.success(request, f'Iniciaste sesión')
                login(request, user)
                return redirect('profile')
            else:
                messages.error(request, 'Verifique su número de identidad o contraseña.')
    else:
        form = EmailLoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def profile(request):
	return render(request, 'profile.html')


def projects(request):
   # projects =list(Project.objects.values())
    projects = Project.objects.all()
    return render(request, "projects.html", {
        "projects": projects
    })

def tasks(request):
   # task = Task.objects.get(title=name)
    tasks = Task.objects.all()
    return render(request, "tasks.html", {
        "tasks": tasks
    })

def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': CreateNewTask()
        })
    else:
        Task.objects.create(title=request.POST['title'],
                            description=request.POST['description'], project_id=2)
        return redirect('tasks')
    
def create_project(request):
    if request.method == "GET":
        return render(request, "create_project.html", {
            'form': CreateNewProject()
        })
    else:
        Project.objects.create(name=request.POST["name"])
        return redirect('projects')
    
def project_detail(request, id):
    project = get_object_or_404(Project, id=id)
    tasks = Task.objects.filter(project_id=id)
    return render(request, 'projects/detail.html', {
        'project': project,
        'tasks': tasks
    })