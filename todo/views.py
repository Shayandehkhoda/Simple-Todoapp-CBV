from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import TaskUpdateForm
from django.views import View
from .models import Task


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "todo/task_list.html"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title"]
    success_url = reverse_lazy("todo:task_list")
    template_name = "todo/task_update.html"


    def form_valid(self, form):
        task = form.save(commit=False)
        task.user = self.request.user
        task.save()
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    success_url = reverse_lazy("todo:task_list")
    form_class = TaskUpdateForm
    template_name = "todo/task_update.html"

    def dispatch(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['pk'])
        if not request.user == task.user:
            messages.error(request, "You cant update other user's task", 'danger')
            return redirect(reverse_lazy('todo:task_list'))
        return super().dispatch(request, *args, **kwargs)



class TaskDoneView(LoginRequiredMixin, View):
    model = Task
    success_url = reverse_lazy("todo:task_list")

    def get(self, request, pk, *args, **kwargs):
        task = Task.objects.get(id=pk)
        task.done = True
        task.save()
        return redirect(self.success_url)


class TaskDeleteView(LoginRequiredMixin, View):

    def get(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)
        if not request.user == task.user:
            messages.error(request, "You cant delete other user's task", 'danger')
            return redirect(reverse_lazy('todo:task_list'))
        task.delete()
        return redirect(reverse_lazy("todo:task_list"))