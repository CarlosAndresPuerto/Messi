from django.urls import path
from .views import register, user_login, profile, projects, tasks, create_task, create_project, project_detail, signout, task_detail, task_update

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


]