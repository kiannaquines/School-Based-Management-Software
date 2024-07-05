from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.contrib.auth import login,logout,authenticate
from authentication.forms import RegisterForm, LoginForm
from django.contrib import messages
from authentication.models import MemberUser
from app.decorators import logged_in_redirect
from django.contrib.auth.decorators import login_required

@logged_in_redirect
def auth_login(request):
    context = {}
    form = LoginForm()

    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():

            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            context['form'] = login_form

            user_login = authenticate(request, username=username, password=password)

            if user_login:
                if user_login.is_active:
                    login(request,user_login)
                    return redirect(reverse_lazy('home_page'))
            else:
                messages.error(request,'Username/Password is invalid or account is not activated, please try again.',extra_tags="username_not_exist")
                return render(request,'login.html',context)


    context['form'] = form

    return render(request,'login.html',context)

       
@logged_in_redirect
def auth_register(request):
    context = {}

    form = RegisterForm()

    if request.method == "POST":

        register_form = RegisterForm(request.POST)

        context['form'] = register_form

        if MemberUser.objects.filter(username=request.POST.get('username')):
            messages.error(request, 'Username already taken choose another username and please try again!',extra_tags="taken_username")
            return render(request,'register.html',context)
        
        if request.POST.get('username') == "" or request.POST.get('password1') == "" or request.POST.get('password2') == "":
            messages.error(request, 'All fields are required, please try again!',extra_tags="all_fields_required")
            return render(request,'register.html',context)

        if request.POST.get('password1') != request.POST.get('password2'):
            messages.error(request, 'Password do not matched, please try again.',extra_tags="invalid_password")
            return render(request,'register.html',context)

        if register_form.is_valid():
            register_form.save()
            messages.success(request, 'You have successfully registered, please wait until 24hrs to activate  your account.',extra_tags="register_success")
            return redirect('auth_login')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.',extra_tags="register_unsuccess")
            return render(request,'register.html',context)

    context['form'] = form
    return render(request,'register.html',context)


@login_required(login_url=reverse_lazy('auth_login'))
def auth_finish_profile(request):
    return render(request,'finish_profile.html')

@login_required(login_url=reverse_lazy('auth_login'))
def auth_logout(request):
    logout(request)
    return redirect(reverse_lazy('auth_login'))
