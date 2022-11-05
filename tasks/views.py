from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView
from .forms import TaskForm
from .models import Tasks
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Task ListView
@login_required
def tasks(request):
    tasks = Tasks.objects.filter(user=request.user, completed_date__isnull=True)
    return render(request, 'tasks.html', {'tasks' : tasks})

@login_required
def tasks_completed(request):
    tasks = Tasks.objects.filter(user=request.user, completed_date__isnull=False)
    return render(request, 'tasks.html', {'tasks' : tasks})

'''
class tasks(LoginRequiredMixin, ListView):
    model = Tasks
    template_name = 'tasks.html'

    def get_queryset(self):
        return Tasks.objects.filter(user=self.request.user, completed_date__isnull=True)

class tasks_completed(LoginRequiredMixin, ListView):
    model = Tasks
    template_name = 'tasks.html'

    def get_queryset(self):
        return Tasks.objects.filter(user=self.request.user, completed_date__isnull=False).order_by('-completed_date')
'''

# Task CreateView
@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
            'form': TaskForm,
            'error': 'Please provide valid data'
        })


# Task Detail
@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Tasks, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Tasks, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
            'form': TaskForm(instance=task),
            'error': 'Please provide valid data'
        })


# Task complete
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Tasks, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.completed_date = timezone.now()
        task.save()
        return redirect('tasks')


# Task delete
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Tasks, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')