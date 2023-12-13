from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout
from django.contrib import messages
from django.http import HttpResponse
from .forms import CreateNewProject, CreateTaskForm, TaskUpdateForm,TaskSubmissionForm, CalificacionForm, EditProjectForm, CustomUserForm, EmailLoginForm
from .models import Project, Task, EntregaTarea, Teacher, Student, CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging
from django.shortcuts import render, get_object_or_404  # Agrega estas importaciones
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import CustomUser 
from django.utils import timezone



#Registro de usuario
def generate_unique_username(identity):
    return str(identity)

def register(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada correctamente!')
            return redirect('login')
        else:
            pass
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
                
                if user.is_teacher:
                    pass

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
    user = request.user 

    user_type = 'profesor' if user.is_teacher else 'estudiante'

    return render(request, 'profile.html', {'user': user, 'user_type': user_type})

@login_required
def list_users(request):
    UserCustom = get_user_model()

    users = UserCustom.objects.all()
    return render(request, 'list_users.html', {'users': users})

@login_required
def projects(request):
    user = request.user

    if user.is_authenticated and user.is_teacher:
        try:
            teacher = Teacher.objects.get(user=user)
            projects = Project.objects.filter(teacher=teacher)
        except Teacher.DoesNotExist:
            projects = []
    else:
        projects = Project.objects.all()

    return render(request, "projects.html", {"projects": projects})

@login_required
def create_project(request):
    if not request.user.is_authenticated or not request.user.is_teacher:
        messages.error(request, 'Solo los profesores pueden crear proyectos.')
        return redirect('projects')

    if request.method == "POST":
        form = CreateNewProject(request.POST, request.FILES)

        if form.is_valid():
            teacher, created = Teacher.objects.get_or_create(user=request.user)

            project = form.save(commit=False)
            project.teacher = teacher

            project.save()

            messages.success(request, f'Proyecto "{project.name}" creado exitosamente.')
            return redirect('projects')
        else:
            print(form.errors)
            messages.error(request, 'Por favor, corrija los errores en el formulario.')

    else:
        form = CreateNewProject()

    return render(request, "create_project.html", {'form': form})

@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if not request.user.is_authenticated or not request.user.is_teacher or project.teacher.user != request.user:
        messages.error(request, 'Solo los profesores pueden editar proyectos.')
        return redirect('projects')

    if request.method == 'POST':
        form = EditProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, f'Proyecto "{project.name}" editado exitosamente.')
            return redirect('projects')
    else:
        form = EditProjectForm(instance=project)

    print(form.fields['archivos_adjuntos'].required)  # Imprime el valor de required
    return render(request, 'edit_project.html', {'form': form, 'project': project})

@login_required
def project_detail(request, project_id):
    if not request.user.is_authenticated:
        return render(request, 'error_page.html', {'message': 'Inicia sesión para ver detalles del proyecto.'})

    project = get_object_or_404(Project, pk=project_id)

    user_is_teacher = request.user.is_teacher if hasattr(request.user, 'is_teacher') else False
    if user_is_teacher and project.teacher.user == request.user:
        tasks = Task.objects.filter(project_id=project_id)
        attachment = project.archivos_adjuntos
        return render(request, 'project_detail.html', {'project': project, 'tasks': tasks, 'attachment': attachment})

    tasks = Task.objects.filter(project_id=project_id)
    attachment = project.archivos_adjuntos
    return render(request, 'project_detail.html', {'project': project, 'tasks': tasks, 'attachment': attachment})

@login_required
def project_delete_confirm(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'project_delete_confirm.html', {'project': project})

@login_required
def project_delete(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    project.delete()
    messages.success(request, f'Proyecto "{project.name}" eliminado correctamente.')
    return redirect('projects')

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
        form = CreateTaskForm(request.POST, request.FILES)
        if form.is_valid():
            fecha_entrega = form.cleaned_data.get('deadline')

            if fecha_entrega and fecha_entrega.date() < timezone.now().date():
                form.add_error('deadline', 'La fecha de entrega debe ser en el futuro.')
                return render(request, 'create_task.html', {'form': form})

            task = form.save(commit=False)
            task.project_id = form.cleaned_data['project'].id
            task.save()
            return redirect('task_detail', task_id=task.id)
    else:
        # Utiliza un formulario vacío en lugar de uno prellenado
        form = CreateTaskForm()

    return render(request, 'create_task.html', {'form': form})

@login_required
def task_update(request, pk):
    user = request.user
    task = get_object_or_404(Task, pk=pk)

    if not user.is_authenticated or (not user.is_teacher or task.project.teacher.user != user):
        return render(request, 'error_page.html', {'message': 'No tienes permisos para actualizar esta tarea.'})

    if request.method == 'POST':
        form = TaskUpdateForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            if 'done' in request.POST:
                task.done = True
            else:
                task.done = False
            task.deadline = form.cleaned_data['deadline']
            task.save()

            return redirect('task_detail', task_id=pk)
    else:
        form = TaskUpdateForm(instance=task)

    return render(request, 'task_update.html', {'form': form, 'task': task})

@login_required
def task_detail(request, task_id):
    user = request.user
    task = get_object_or_404(Task, pk=task_id)
    entrega = EntregaTarea.objects.filter(tarea=task, estudiante=user).first()
    archivos_adjuntos = task.archivos_adjuntos if task.archivos_adjuntos else None
    is_teacher = user.is_authenticated and user.is_teacher

    if request.method == 'POST':
        if not is_teacher and not entrega:
            form = TaskSubmissionForm(request.POST, request.FILES)
            if form.is_valid():
                # Guardar la entrega de la tarea
                form.instance.tarea = task
                form.instance.estudiante = user
                form.save()
                return redirect('task_detail', task_id=task.id)
        else:
            return redirect('task_detail', task_id=task.id)
    else:
        if not is_teacher and not entrega:
            form = TaskSubmissionForm()
        else:
            form = None

    return render(request, 'task_detail.html', {'task': task, 'entrega': entrega, 'form': form, 'archivos_adjuntos': archivos_adjuntos})

@login_required
def delete_task_attachment(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if task.archivos_adjuntos:
        task.archivos_adjuntos.delete()

    return redirect('task_detail', task_id=task.id)

@login_required
def delete_task(request, task_id):
    user = request.user
    task = get_object_or_404(Task, id=task_id)

    if not user.is_authenticated or (not user.is_teacher or task.project.teacher.user != user):
        return render(request, 'error_page.html', {'message': 'No tienes permisos para eliminar esta tarea.'})

    if request.method == 'POST':
        task.delete()
        messages.success(request, f'Tarea "{task.title}" eliminada correctamente.')
        return redirect('tasks')

    return render(request, 'task_delete_confirm.html', {'task': task})

@login_required
def submit_task(request, task_id):
    user = request.user
    task = get_object_or_404(Task, pk=task_id)
    entrega_tarea, created = EntregaTarea.objects.get_or_create(tarea=task, estudiante=user)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'enviar':
            form = TaskSubmissionForm(request.POST, request.FILES, instance=entrega_tarea)

            if form.is_valid():
                entrega_tarea = form.save(commit=False)
                entrega_tarea.tarea = task
                entrega_tarea.estudiante = user
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

    form.fields['calificacion'].widget.attrs['readonly'] = True

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
            entrega.comentarios_profesor = form.cleaned_data['comentarios_profesor']
            entrega.save()
            return redirect('ver_entregas_profesor', task_id=entrega.tarea.id)
    else:
        form = CalificacionForm(initial={'calificacion': entrega.calificacion, 'comentarios_profesor': entrega.comentarios_profesor})

    return render(request, 'detalle_entrega.html', {'entrega': entrega, 'form': form})


@user_passes_test(lambda u: u.is_staff)
def review_teacher(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)

    if request.method == 'POST':
        if hasattr(user, 'is_teacher_candidate') and hasattr(user, 'is_teacher'):
            if 'approve' in request.POST:
                user.is_teacher_candidate = False
                user.is_teacher = True
                user.is_student = False  
                user.save()

                message = f"Se aprobó a {user.username} como profesor."
                messages.add_message(request, messages.SUCCESS, message)

                return HttpResponseRedirect(reverse('admin:core_customuser_changelist'))

    return render(request, 'admin/review_teacher.html', {'user': user})
