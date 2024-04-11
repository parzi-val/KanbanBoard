# urls.py
from django.urls import path
from .views import (switch_project_and_board,
                    create_project,create_board,
                    create_task,show_project,
                    setStatusTask,show_board,
                    show_assigned_tasks,show_task,
                    user_registration,
                    login_view,logout_view,current,
                    delete_project,delete_board,delete_task)

urlpatterns = [
    path('switch/', switch_project_and_board, name='switch_project_and_board'),
    path('projects/create/', create_project, name='create-project'),
    path('boards/create/',create_board,name='create-board'),
    path('boards/add-task/',create_task,name='create_task'),
    path('projects/get-info/',show_project,name='project-get-info'),
    path('boards/get-info/',show_board,name='board-get-info'),
    path('boards/tasks/status/',setStatusTask,name='task-status'),
    path('register/', user_registration, name='user-register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('projects/delete/',delete_project,name='delete-project'),
    path('boards/delete/',delete_board,name='delete-board'),
    path('boards/tasks/delete/',delete_task,name='delete=task'),
    path('tasks/',show_assigned_tasks,name='show_assigned_tasks'),
    path('board/task/',show_task,name='show_task'),
    path('current/',current,name='current')
]

