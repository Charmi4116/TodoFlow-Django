from django.urls import path
from . import views


urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('task/<int:id>/', views.todo_detail, name='todo_detail'),
    path('delete/<int:id>/', views.todo_delete, name='todo_delete'),
    path('update-status/<int:id>/', views.update_status, name='update_status'),
]