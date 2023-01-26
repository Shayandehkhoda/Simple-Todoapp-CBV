from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path("", views.TaskListView.as_view(), name="task_list"),
    path("create/", views.TaskCreateView.as_view(), name="create_task"),
    path("update/<int:pk>/", views.TaskUpdateView.as_view(), name="update_task"),
    path("done/<int:pk>/", views.TaskDoneView.as_view(), name="done_task"),
    path("delete/<int:pk>/", views.TaskDeleteView.as_view(), name="delete_task"),
]


