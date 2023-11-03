from django.conf import settings
from django.shortcuts import render, redirect, HttpResponse
from .forms import UserCustomRegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import EmailLoginForm
from django.contrib.auth.decorators import login_required
from .models import Project, Task, EntregaTarea, UserCustom
from .forms import CreateNewProject, CreateTaskForm, TaskUpdateForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User
from core.models import UserCustom






#Registro de usuario
def register(request):
    if request.method == "POST":
        form = UserCustomRegisterForm(request.POST)
        if form.is_valid():
            identity = form.cleaned_data.get('identity')
            password = form.cleaned_data.get('password')
            User = get_user_model()
            user = User.objects.create_user(username=identity, password=password)
            messages.success(request, f'Cuenta creada para {identity}!')
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
            task.deadline = form.cleaned_data['deadline']  # Actualiza la fecha y hora de entrega
            form.save()  # Guarda los cambios en la tarea

            return redirect('task_detail', task_id=pk)  # Redirige a los detalles de la tarea actualizada
    else:
        form = TaskUpdateForm(instance=task)

    return render(request, 'task_update.html', {'form': form, 'task': task})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    
    # Obtiene la información de los estudiantes que entregaron la tarea
    entregas = EntregaTarea.objects.filter(tarea=task)
    
    # Recopila la lista de estudiantes que entregaron la tarea y los que no
    estudiantes_entregaron = UserCustom.objects.filter(entregatarea__entregada=True, entregatarea__tarea=task)
    estudiantes_no_entregaron = UserCustom.objects.filter(entregatarea__entregada=False, entregatarea__tarea=task)

    return render(request, 'task_detail.html', {'task': task, 'entregas': entregas, 'estudiantes_entregaron': estudiantes_entregaron, 'estudiantes_no_entregaron': estudiantes_no_entregaron})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

    return render(request, 'task_delate_confirm.html', {'task': task})

def list_users(request):
    UserCustom = get_user_model()  # Obtén el modelo de usuario personalizado

    users = UserCustom.objects.all()  # Obtiene todos los usuarios registrados
    users = UserCustom.objects.filter(is_superadmin=False)

    return render(request, 'list_users.html', {'users': users})

