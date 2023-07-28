from django.urls import path
from . import views

# app_name="users"
urlpatterns = [
    path('', views.login_view, name='login'),
    path('tasks.html', views.tasks_view, name= "tasks")
]