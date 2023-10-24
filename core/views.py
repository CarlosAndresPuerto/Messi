from django.shortcuts import render, redirect, HttpResponse
from .forms import UserCustomRegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import EmailLoginForm
from django.contrib.auth.decorators import login_required
from .models import Project, Task
from .forms import CreateNewProject, CreateTaskForm, TaskUpdateForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import UpdateView


#Registro de usuario
def register(request):
    if request.method == "POST":
        form = UserCustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = generate_unique_username(user.identity)  # Reemplaza esto con tu lógica
            user.save()
            identity = form.cleaned_data.get('identity')
            messages.success(request, f'Cuenta creada para {identity}!')
            return redirect('login')
    else:
        form = UserCustomRegisterForm()
    return render(request, 'crear_cuenta.html', {'form': form})

def generate_unique_username(identity):
    username = str(identity)
    return username

def signout(request):
    logout(request)
    return redirect('home')

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
    tasks = Task.objects.all()
    return render(request, "tasks.html", {
        "tasks": tasks
    })

def create_task(request):
    if request.method == 'POST':
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            print(f"Task ID before save: {task.id}")  # Agregar esta línea para depuración
            task.save()
            print(f"Task ID after save: {task.id}")  # Agregar esta línea para depuración
            return redirect('task_detail', task_id=task.id)
    else:
        form = CreateTaskForm()
    return render(request, 'create_task.html', {'form': form})

def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'task_detail.html', {'task': task})

def create_project(request):
    if request.method == "GET":
        return render(request, "create_project.html", {
            'form': CreateNewProject()
        })
    else:
        Project.objects.create(name=request.POST["name"])
        return redirect('projects')
    
def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    tasks = Task.objects.filter(project_id=project_id)
    return render(request, 'project_detail.html', {'project': project, 'tasks': tasks})

def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        form = TaskUpdateForm(request.POST, instance=task)
        if form.is_valid():
            if 'done' in request.POST:
                task.done = True
            else:
                task.done = False
            form.save()  # Guarda los cambios en la tarea

            return redirect('task_detail', task_id=pk)  # Redirige a los detalles de la tarea actualizada
    else:
        form = TaskUpdateForm(instance=task)

    return render(request, 'task_update.html', {'form': form, 'task': task})

