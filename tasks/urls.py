from django.urls import path

from tasks.views import (
    CommentDeleteView,
    CommentEditView,
    RegisterView,
    TaskCreateView,
    TaskDeleteView,
    TaskDetailView,
    TaskListView,
    TaskUpdateView,
)

app_name = "tasks"

urlpatterns = [
    path("", TaskListView.as_view(), name="task_list"),
    path("<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path("add/", TaskCreateView.as_view(), name="task_create"),
    path("<int:pk>/edit/", TaskUpdateView.as_view(), name="task_update"),
    path("<int:pk>/delete/", TaskDeleteView.as_view(), name="task_delete"),
    path("register/", RegisterView.as_view(), name="register"),
    path("comment/<int:pk>/edit/", CommentEditView.as_view(), name="comment_edit"),
    path(
        "comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment_delete"
    ),
]