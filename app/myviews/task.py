from django.views.generic import CreateView,UpdateView,DeleteView
from django.contrib import messages
from django.core.paginator import Paginator
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from app.models import Task
from app.forms import TaskForm
from django.shortcuts import render,redirect
from app.views import get_path
from app.decorators import only_admin

@login_required(login_url=reverse_lazy('auth_login'))
def all_task(request):
    context = {}
    context['tasks'] = Task.objects.all()
    context['manage_task_path'] = get_path(request)
    return render(request,"task.html",context)


@only_admin
@login_required(login_url=reverse_lazy("auth_login"))
def admin_verify_task(request,task_id):
    task = Task.objects.get(id=task_id)

    if task.status == Task.TaskStatus.VERIFIED:
        messages.success(request,f"The task assigned to {task.assigned_to} is already verified, thank you!",extra_tags="already_verified")
        return redirect('manage_task')

    task.status = Task.TaskStatus.VERIFIED
    task.save()
    return redirect('manage_task')

class CreateTaskView(CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('manage_task')
    template_name = 'form_templates/add_task.html'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        messages.success(self.request,"You have successfully added the new task.",extra_tags="added_task")
        return response

class UpdateTaskView(UpdateView):
    model = Task
    form_class = TaskForm
    pk_url_kwarg = 'task_id'
    success_url = reverse_lazy('manage_task')
    template_name = 'form_templates/edit_task.html'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        messages.success(self.request,f"You have successfully updated the existing task assigned to {form.cleaned_data['assigned_to']}.",extra_tags="update_task")
        return response
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        print(form.errors)
        return super().form_invalid(form)

class DeleteTaskView(DeleteView):
    model = Task
    pk_url_kwarg = 'task_id'
    template_name = 'form_templates/delete_task.html'
    success_url = reverse_lazy('manage_task')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        messages.success(self.request,"You have successfully removed the existing task.",extra_tags="delete_task")
        return response