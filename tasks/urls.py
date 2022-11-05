from django.urls import path
from .views import *

urlpatterns = [
    path('list/', tasks, name='tasks'),
    path('list/tasks_completed', tasks_completed, name='tasks_completed'),
    #path('list/', tasks.as_view(), name='tasks'),
    #path('list/tasks_completed', tasks_completed.as_view(), name='tasks_completed'),
    path('create/', create_task, name='create_task'),
    path('detail/<int:task_id>', task_detail, name='task_detail'),
    path('detail/<int:task_id>/complete', complete_task, name='complete_task'),
    path('detail/<int:task_id>/delete', delete_task, name='delete_task')
]
