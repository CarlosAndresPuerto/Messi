from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout
from django.contrib import messages
from django.http import HttpResponse
from .forms import CreateNewProject, CreateTaskForm, TaskUpdateForm,TaskSubmissionForm, CalificacionForm
from .forms import UserCustomRegisterForm
from .forms import EmailLoginForm
from .models import Project, Task, EntregaTarea

#Registro de usuario
def generate_unique_username(identity):
    return str(identity)

# Luego, dentro de la vista register
def register(request):
    if request.method == "POST":
        form = UserCustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = generate_unique_username(form.cleaned_data['identity'])
            user.save()
            messages.success(request, 'Cuenta creada correctamente!')
            return redirect('login')
    else:
        form = UserCustomRegisterForm()

    return render(request, 'crear_cuenta.html', {'form': form})

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

    if request.method == 'POST' and 'submit_task' in request.POST:
        return redirect('submit_task', task_id=task.id)

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
        action = request.POST.get('action')

        if action == 'enviar':
            form = TaskSubmissionForm(request.POST, request.FILES, instance=entrega_tarea)

            if form.is_valid():
                entrega_tarea = form.save(commit=False)
                entrega_tarea.tarea = task
                entrega_tarea.estudiante = request.user
                entrega_tarea.entregada = True
                entrega_tarea.save()

                messages.success(request, 'Tarea enviada correctamente.')
                return redirect('task_detail', task_id=task_id)
            else:
                messages.error(request, 'Por favor, confirma la entrega y adjunta un archivo o escribe un comentario.')

        elif action == 'anular':
            # Permitir la anulación solo si la tarea no está bloqueada
            if not entrega_tarea.bloqueada:
                entrega_tarea.delete()
                messages.success(request, 'Entrega anulada correctamente.')
            else:
                messages.error(request, 'No puedes anular una entrega bloqueada.')

            return redirect('task_detail', task_id=task_id)

    else:
        form = TaskSubmissionForm(instance=entrega_tarea)

    return render(request, 'submit_task.html', {'form': form, 'task': task, 'entrega': entrega_tarea})





@login_required
def anular_entrega(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    entrega_tarea = EntregaTarea.objects.get(tarea=task, estudiante=request.user)

    if request.method == 'POST':
        if not entrega_tarea.bloqueada:
            entrega_tarea.delete()

    return redirect('submit_task', task_id=task_id)

@login_required
def ver_entregas_profesor(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    entregas = EntregaTarea.objects.filter(tarea=task)

    print("Task:", task)
    print("Entregas:", entregas)

    return render(request, 'ver_entregas_profesor.html', {'task': task, 'entregas': entregas})

@login_required
def detalle_entrega(request, entrega_id):
    entrega = get_object_or_404(EntregaTarea, pk=entrega_id)
    
    if request.method == 'POST':
        form = CalificacionForm(request.POST)
        if form.is_valid():
            entrega.calificacion = form.cleaned_data['calificacion']
            entrega.save()
            # Redirigir a la vista 'ver_entregas_profesor' con el task_id adecuado
            return redirect('ver_entregas_profesor', task_id=entrega.tarea.id)
    else:
        form = CalificacionForm(initial={'calificacion': entrega.calificacion})

    return render(request, 'detalle_entrega.html', {'entrega': entrega, 'form': form})

