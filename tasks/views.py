from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import UpdateView, DeleteView

from .forms import TaskForm, CommentForm
from .mixins import UserIsOwnerMixin, SuccessMessageMixin
from .models import Task, Comment, CommentLike


class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"


class TaskDetailView(DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.all().order_by("-created_at")
        context["form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.task = self.object
            comment.save()

        return redirect("tasks:task_detail", pk=self.object.pk)

class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:task_list")
    success_message = "Завдання успішно створено!"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class RegisterView(CreateView):
    template_name = "registration/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("tasks:task_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:task_list")
    success_message = "Завдання успішно оновлено!"


class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("tasks:task_list")


class CommentEditView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "tasks/comment_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "tasks:task_detail",
            kwargs={"pk": self.object.task.pk},
        )

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "tasks/comment_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy(
            "tasks:task_detail",
            kwargs={"pk": self.object.task.pk},
        )

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


@login_required
def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    like = CommentLike.objects.filter(
        comment=comment,
        user=request.user
    )

    if like.exists():
        like.delete()
    else:
        CommentLike.objects.create(
            comment=comment,
            user=request.user
        )

    return redirect("tasks:task_detail", pk=comment.task.pk)