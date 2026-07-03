from django.contrib import messages
from django.core.exceptions import PermissionDenied


class UserIsOwnerMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.creator != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class SuccessMessageMixin:
    success_message = "Операція виконана успішно!"

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)