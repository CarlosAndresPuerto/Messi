from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout
from django.contrib import messages
from django.http import HttpResponse
from .forms import CreateNewProject, CreateTaskForm, TaskUpdateForm,TaskSubmissionForm, CalificacionForm
from .forms import CustomUserForm
from .forms import EmailLoginForm
from .models import Project, Task, EntregaTarea, Teacher, Student, CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging
from django.shortcuts import render, get_object_or_404  # Agrega estas importaciones
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import CustomUser 



#Registro de usuario
def generate_unique_username(identity):
    return str(identity)

def register(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            if not user.is_teacher_candidate:
                user.is_student = True

            user.save()

            # Agregar mensaje de éxito
            messages.success(request, 'Cuenta creada correctamente!')
            
            # Redireccionar a una página específica o al inicio de sesión
            return redirect('login')
    else:
        form = CustomUserForm()

    return render(request, 'crear_cuenta.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            identity = form.cleaned_data['identity']
            password = form.cleaned_data['password']

            print(f"Identity: {identity}, Password: {password}")

            user = authenticate(request, identity=identity, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenido, {user.username}!")
                return redirect('profile')
            else:
                messages.error(request, 'Verifique su número de identidad o contraseña.')

    else:
        form = EmailLoginForm()

    return render(request, 'login.html', {'form': form})

@login_required
def signout(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    user = request.user  # Obtén el usuario autenticado

    # Determina el tipo de usuario
    user_type = 'profesor' if user.is_teacher else 'estudiante'

    # Pasa el tipo de usuario al contexto
    return render(request, 'profile.html', {'user': user, 'user_type': user_type})

@login_required
def list_users(request):
    UserCustom = get_user_model()

    users = UserCustom.objects.all()
    return render(request, 'list_users.html', {'users': users})

@login_required
def projects(request):
    user = request.user
    
    try:
        teacher = Teacher.objects.get(user=user)
        projects = Project.objects.filter(teacher=teacher)
    except ObjectDoesNotExist:
        # Manejo de excepción si el usuario no tiene un objeto Teacher asociado
        projects = []

    return render(request, "projects.html", {"projects": projects})

@login_required
def create_project(request):
    if not request.user.is_authenticated or not request.user.is_teacher:
        messages.error(request, 'Solo los profesores pueden crear proyectos.')
        return redirect('projects')

    if request.method == "GET":
        return render(request, "create_project.html", {
            'form': CreateNewProject()
        })
    else:
        teacher = Teacher.objects.get(user=request.user)
        project = Project.objects.create(name=request.POST["name"], teacher=teacher)
        messages.success(request, f'Proyecto "{project.name}" creado exitosamente.')
        return redirect('projects')

@login_required
def project_detail(request, project_id):
    if not request.user.is_authenticated or not request.user.is_teacher:
        return render(request, 'error_page.html', {'message': 'Solo los profesores pueden ver detalles de proyectos.'})

    project = get_object_or_404(Project, pk=project_id)
    tasks = Task.objects.filter(project_id=project_id)
    
    return render(request, 'project_detail.html', {'project': project, 'tasks': tasks})

@login_required
def tasks(request):
    user = request.user

    if user.is_teacher:
        tasks = Task.objects.filter(project__teacher__user=user)
    elif user.is_student:
        tasks = Task.objects.filter(entregatarea__estudiante=user)
    else:
        tasks = Task.objects.all()

    return render(request, "tasks.html", {"tasks": tasks})

@login_required
def create_task(request):
    if not request.user.is_authenticated or not request.user.is_teacher:
        return render(request, 'error_page.html', {'message': 'Solo los profesores pueden crear tareas.'})

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
    if not request.user.is_authenticated or not request.user.is_teacher:
        return render(request, 'error_page.html', {'message': 'Solo los profesores pueden actualizar tareas.'})

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
    if not request.user.is_authenticated or not request.user.is_teacher:
        return render(request, 'error_page.html', {'message': 'Solo los profesores pueden ver detalles de tareas.'})

    task = get_object_or_404(Task, pk=task_id)
    entrega = EntregaTarea.objects.filter(tarea=task, estudiante=request.user).first()

    if request.method == 'POST' and 'submit_task' in request.POST:
        return redirect('submit_task', task_id=task.id)

    return render(request, 'task_detail.html', {'task': task, 'entrega': entrega})

@login_required
def delete_task(request, task_id):
    if not request.user.is_authenticated or not request.user.is_teacher:
        return render(request, 'error_page.html', {'message': 'Solo los profesores pueden eliminar tareas.'})

    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

    return render(request, 'task_delete_confirm.html', {'task': task})

@login_required
def submit_task(request, task_id):
    if not request.user.is_authenticated or (not request.user.is_teacher and not request.user.is_student):
        return render(request, 'error_page.html', {'message': 'Solo los profesores y estudiantes pueden enviar tareas.'})

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
    if not request.user.is_authenticated or not request.user.is_student:
        return render(request, 'error_page.html', {'message': 'Solo los estudiantes pueden anular entregas de tareas.'})

    task = get_object_or_404(Task, pk=task_id)
    entrega_tarea = EntregaTarea.objects.get(tarea=task, estudiante=request.user)

    if request.method == 'POST':
        if not entrega_tarea.bloqueada:
            entrega_tarea.delete()

    return redirect('submit_task', task_id=task_id)

@login_required
def ver_entregas_profesor(request, task_id):
    if not request.user.is_authenticated or not request.user.is_teacher:
        return render(request, 'error_page.html', {'message': 'Solo los profesores pueden ver las entregas de tareas.'})

    task = get_object_or_404(Task, pk=task_id)
    entregas = EntregaTarea.objects.filter(tarea=task)

    return render(request, 'ver_entregas_profesor.html', {'task': task, 'entregas': entregas})

@login_required
def detalle_entrega(request, entrega_id):
    if not request.user.is_authenticated or not request.user.is_teacher:
        return render(request, 'error_page.html', {'message': 'Solo los profesores pueden ver detalles y calificar entregas.'})

    entrega = get_object_or_404(EntregaTarea, pk=entrega_id)
    
    if request.method == 'POST':
        form = CalificacionForm(request.POST)
        if form.is_valid():
            entrega.calificacion = form.cleaned_data['calificacion']
            entrega.save()
            return redirect('ver_entregas_profesor', task_id=entrega.tarea.id)
    else:
        form = CalificacionForm(initial={'calificacion': entrega.calificacion})

    return render(request, 'detalle_entrega.html', {'entrega': entrega, 'form': form})

@user_passes_test(lambda u: u.is_staff)
def review_teacher(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)

    if request.method == 'POST':
       
        if hasattr(user, 'is_teacher_candidate') and hasattr(user, 'is_teacher'):
            if 'approve' in request.POST:
                user.is_teacher_candidate = False
                user.is_teacher = True
                user.is_student = False  # Asegúrate de desactivar el estado de estudiante
                user.save()

                messages.success(request, f"Se aprobó a {user.username} como profesor.")

                return HttpResponseRedirect(reverse('admin:core_customuser_changelist'))

    return render(request, 'admin/review_teacher.html', {'user': user})
