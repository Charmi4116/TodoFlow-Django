from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Todo
from .forms import TodoForm
from django.core.paginator import Paginator
# Create your views here.

def todo_list(request):

    if request.method == 'POST':
        edit_id = request.POST.get('edit_id')

        if edit_id:
            todo = get_object_or_404(
                Todo,
                id=edit_id,
                is_deleted=False
            )
            form = TodoForm(request.POST, instance=todo)
        else:
            form = TodoForm(request.POST)

        if form.is_valid():
            todo = form.save()
            todo.completed = (todo.status == 'Completed')
            todo.save()
            return redirect('todo_list')

    else:
        form = TodoForm()

    todos = Todo.objects.filter(is_deleted=False).order_by('created_at')
    search = request.GET.get('search', '')
    priority = request.GET.get('priority', '')
    status = request.GET.get('status', '')
    due_date = request.GET.get('due_date', '')
    today = timezone.localdate()

    if search:
        todos = todos.filter(task__icontains=search)

    if priority:
        todos = todos.filter(priority=priority)

    if status:
        todos = todos.filter(status=status)

    if due_date == 'Today':
        todos = todos.filter(due_date=timezone.localdate())

    elif due_date == 'Tomorrow':
        todos = todos.filter(
            due_date=timezone.localdate() + timedelta(days=1)
        )

    elif due_date == 'Overdue':
        todos = todos.filter(due_date__lt=timezone.localdate())

    elif due_date == 'No Deadline':
        todos = todos.filter(due_date__isnull=True)

    paginator = Paginator(todos, 5)
    page_number = request.GET.get('page')
    todos = paginator.get_page(page_number)

    total_tasks = Todo.objects.filter(is_deleted=False).count()

    completed_tasks = Todo.objects.filter(is_deleted=False,status='Completed').count()

    pending_tasks = Todo.objects.filter(is_deleted=False,status='Pending').count()

    high_priority_tasks = Todo.objects.filter(is_deleted=False,priority='High').count()

    return render(request, 'todo_list.html', {
        'todos': todos,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'high_priority_tasks': high_priority_tasks,
        'search': search,
        'priority': priority,
        'status': status,
        'due_date': due_date,
        'today': today,
        'form':form,
    })

def todo_detail(request, id):
    todo = get_object_or_404(Todo, id=id)
    return render(request, 'todo_detail.html', {'todo': todo})

def todo_delete(request, id):
    todo = get_object_or_404(Todo, id=id)
    todo.is_deleted = True
    todo.save()
    return redirect('todo_list')

def update_status(request, id):
    todo = get_object_or_404(Todo, id=id)

    if request.method == 'POST':
        status = request.POST.get('status')
        todo.status = status
        todo.completed = (status == 'Completed')
        todo.save()

    return redirect('todo_list')
