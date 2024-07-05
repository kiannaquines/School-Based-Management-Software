from django.views.generic import UpdateView,DeleteView
from django.shortcuts import render,redirect
from authentication.models import User 
from app.forms import UpdateUserForm,NewUserForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.forms import BaseModelForm
from django.http import HttpResponse
from app.decorators import only_admin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from app.views import get_path
from django.core.paginator import Paginator

@only_admin
@login_required(login_url=reverse_lazy("auth_login"))
def activate(request,user_id):
    user = User.objects.get(id=user_id)

    if user.is_active:
        messages.success(request,f"You have already activated the user {user}, thank you!",extra_tags="user_already_verified")
        return redirect('user_list')

    user.is_active = True
    user.save()
    messages.success(request,f"User {user} is completely activated, thank you!",extra_tags="activated_user")
    return redirect('user_list')

@only_admin
@login_required(login_url=reverse_lazy('auth_login'))
def adduser(request):
    context = {}

    if request.method == "POST":
        new_user_form = NewUserForm(request.POST)

        if new_user_form.is_valid():
            new_user_form.save()
            messages.success(request,"You have successfully added new user.",extra_tags="added_new_user")
            return redirect(reverse_lazy('adduser'))
        else:
            context['errors'] = new_user_form.errors
            context['form'] = new_user_form
            return render(request,'form_templates/add_user.html',context)

    context['add_user'] = get_path(request)
    context['form'] = NewUserForm()
    return render(request,'form_templates/add_user.html',context)

@only_admin
@login_required(login_url=reverse_lazy('auth_login'))
def user_list(request):
    context = {}
    context['user_path'] = get_path(request)
    users = User.objects.all()
    paginator = Paginator(users,9)
    page = request.GET.get('page')
    objects = paginator.get_page(page)

    context['user_list'] = objects

    return render(request,'user_list.html',context)

class EditUserView(UpdateView):
    model = User
    form_class = UpdateUserForm
    success_url = reverse_lazy('edituser')
    pk_url_kwarg = 'id'
    template_name = 'form_templates/edit_user.html'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        messages.success(self.request, "User has been updated successfully.", extra_tags="update_user")
        return response
    
    def get_success_url(self):
        return reverse_lazy("edituser", kwargs={'id': self.object.pk})
    

class RemoveUserView(DeleteView):
    model = User
    success_url = reverse_lazy('user_list')
    pk_url_kwarg = 'id'
    template_name = 'form_templates/delete_user.html'