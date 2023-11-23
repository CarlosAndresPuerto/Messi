from django.conf import settings
from django.shortcuts import render, redirect
from .forms import UserCustomRegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import EmailLoginForm
from django.contrib.auth.decorators import login_required
from .models import Project, Task, EntregaTarea, UserCustom
from .forms import CreateNewProject, CreateTaskForm, TaskUpdateForm,TaskSubmissionForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User
from core.models import UserCustom
from django.http import HttpResponse  # Agrega esta importación para los logs
from django.utils import timezone


#Registro de usuario
def register(request):
    if request.method == "POST":
        form = UserCustomRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada correctamente!')
            return redirect('login')
    else:
        form = UserCustomRegisterForm()

    return render(request, 'crear_cuenta.html', {'form': form})

def generate_unique_username(identity):
    username = str(identity)
    return username

@login_required
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
                login(request, user)
                return redirect('profile')
            else:
                messages.error(request, 'Verifique su número de identidad o contraseña.')
    else:
        form = EmailLoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def profile(request):
    user = request.user  # Obtén el usuario autenticado
    return render(request, 'profile.html', {'user': user})

@login_required
def list_users(request):
    UserCustom = get_user_model()

    users = UserCustom.objects.all()
    return render(request, 'list_users.html', {'users': users})

@login_required
def projects(request):
   # projects =list(Project.objects.values())
    projects = Project.objects.all()
    return render(request, "projects.html", {
        "projects": projects
    })

@login_required
def create_project(request):
    if request.method == "GET":
        return render(request, "create_project.html", {
            'form': CreateNewProject()
        })
    else:
        Project.objects.create(name=request.POST["name"])
        return redirect('projects')

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    tasks = Task.objects.filter(project_id=project_id)
    return render(request, 'project_detail.html', {'project': project, 'tasks': tasks})

@login_required
def tasks(request):
    tasks = Task.objects.all()
    return render(request, "tasks.html", {
        "tasks": tasks
    })

@login_required
def create_task(request):
    if request.method == 'POST':
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project_id = form.cleaned_data['project'].id
            task.save()
            return redirect('task_detail', task_id=task.id)
    else:
        form = CreateTaskForm()

    return render(request, 'create_task.html', {'form': form})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        form = TaskUpdateForm(request.POST, instance=task)
        if form.is_valid():
            if 'done' in request.POST:
                task.done = True
            else:
                task.done = False
            task.deadline = form.cleaned_data['deadline']
            form.save()

            return redirect('task_detail', task_id=pk)
    else:
        form = TaskUpdateForm(instance=task)

    return render(request, 'task_update.html', {'form': form, 'task': task})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    entrega = EntregaTarea.objects.filter(tarea=task, estudiante=request.user).first()

    if entrega is not None:
        if request.method == 'POST' and 'submit_task' in request.POST:
                return redirect('submit_task', entrega_id=entrega.id)

    return render(request, 'task_detail.html', {'task': task, 'entrega': entrega})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

    return render(request, 'task_delate_confirm.html', {'task': task})

@login_required
def submit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    entrega_tarea, created = EntregaTarea.objects.get_or_create(tarea=task, estudiante=request.user)

    if request.method == 'POST':
        form = TaskSubmissionForm(request.POST, instance=entrega_tarea)
        if form.is_valid():
            entrega_tarea = form.save(commit=False)
            entrega_tarea.tarea = task
            entrega_tarea.estudiante = request.user
            entrega_tarea.entregada = True  # Establecer entregada en True
            entrega_tarea.save()

            if isinstance(entrega_tarea, EntregaTarea):
                print(f"Entrega guardada: {entrega_tarea.get_tarea_info()}")
            else:
                print("No hay entrega guardada.")                         
            
            return redirect('task_detail', task_id=task_id)
        else:  
            print(f"Errores en el formulario: {form.errors}")
    else:
        # Inicializar el formulario sin establecer manualmente 'tarea' y 'estudiante'
        form = TaskSubmissionForm(instance=entrega_tarea, initial={'entregada': True})

    return render(request, 'submit_task.html', {'form': form, 'task': task, 'entrega': entrega_tarea})



@login_required
def ver_entregas_profesor(request, task_id):
    task = Task.objects.get(pk=task_id)
    entregas = EntregaTarea.objects.filter(tarea=task)
    return render(request, 'ver_entregas_profesor.html', {'task': task, 'entregas': entregas})
