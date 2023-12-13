from django.urls import path
from .views import register, user_login, profile, projects, tasks, create_task, create_project, project_detail, signout, task_detail, task_update, delete_task, list_users, submit_task, ver_entregas_profesor, detalle_entrega, anular_entrega, review_teacher, project_delete_confirm, project_delete, edit_project, delete_task_attachment

urlpatterns = [
    path('register/', register, name="registro"),
    path('login/', user_login, name='login'),
    path('profile/', profile, name='profile'),
    path('projects/', projects, name="projects"),
    path('projects/<int:project_id>/', project_detail, name='project_detail'),
    path('core/tasks/<int:task_id>/', task_detail, name='task_detail'),
    path('tasks/', tasks, name="tasks"),
    path('create_task/', create_task, name="create_task"),
    path("create_project/", create_project, name="create_project"),
    path('logout/', signout, name='logout'),
    path('tasks/<int:pk>/update/', task_update, name='task_update'),
    path('tasks/<int:task_id>/delete/', delete_task, name='delete_task'),
    path('list_users/', list_users,name='list_users'),
    path('tasks/<int:task_id>/submit/', submit_task, name='submit_task'),
    path('ver_entregas_profesor/<int:task_id>/', ver_entregas_profesor, name='ver_entregas_profesor'),
    path('detalle_entrega/<int:entrega_id>/', detalle_entrega, name='detalle_entrega'),
    path('entrega/anular/<int:task_id>/', anular_entrega, name='anular_entrega'),
    path('admin/review-teacher/<int:user_id>/', review_teacher, name='admin_review_teacher'),
    path('project/<int:project_id>/delete/', project_delete_confirm, name='project_delete_confirm'),
    path('project/<int:project_id>/delete/confirmed/', project_delete, name='project_delete'),
    path('edit_project/<int:project_id>/', edit_project, name='edit_project'),
    path('delete_task_attachment/<int:task_id>/', delete_task_attachment, name='delete_task_attachment'),



] 

