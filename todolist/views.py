from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo
from .forms import TodoForm
# Create your views here.

def todo_list(request):
    todos = Todo.objects.all().order_by('created_at')

    total_tasks = Todo.objects.count()
    completed_tasks = Todo.objects.filter(completed=True).count()
    pending_tasks = Todo.objects.filter(completed=False).count()
    high_priority_tasks = Todo.objects.filter(priority='High').count()

    return render(request, 'todo_list.html', {
        'todos': todos,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'high_priority_tasks': high_priority_tasks,
    })

def todo_detail(request, id):
    todo = get_object_or_404(Todo, id=id)
    return render(request, 'todo_detail.html', {'todo': todo})

def todo_create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = TodoForm()

    return render(request, 'todo_form.html', {
        'form': form,
        'title': 'Add New Task',
        'button_text': 'Save Task',
    })

def todo_update(request, id):
    todo = get_object_or_404(Todo, id=id)

    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)

        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = TodoForm(instance=todo)

    return render(request, 'todo_form.html', {
        'form': form,
        'title': 'Update Task',
        'button_text': 'Update Task',
    })

def todo_delete(request, id):
    todo = get_object_or_404(Todo, id=id)
    todo.delete()
    return redirect('todo_list')