from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Task(models.Model):

    STATUS_CHOICES = [
        ("todo", "To Do"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    title = models.CharField(max_length=256)
    pole = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="medium")
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tasks",
        null=True,
        blank=True
    )
    file = models.FileField(upload_to="tasks/", blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("tasks:task_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["-status"]


class Comment(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def likes_count(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.author.username} — {self.content[:30]}"


class CommentLike(models.Model):
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="likes"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comment_likes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("comment", "user")

    def __str__(self):
        return f"{self.user.username} likes Comment #{self.comment.id}"