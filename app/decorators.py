from functools import wraps
from django.shortcuts import redirect
from authentication.models import User

def logged_in_redirect(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home_page')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def only_admin(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args,**kwargs):
        if request.user.is_anonymous:
            return redirect('auth_login')
        if request.user.user_role == User.Role.MEMBER or request.user.user_role == User.Role.SBM_COORDINATOR or request.user.user_role == User.Role.CHAIRPERSON or request.user.user_role == User.Role.KPI:
            return redirect('index')
        return view_func(request,*args,**kwargs)
    
    return _wrapped_view

def only_user(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args,**kwargs):
        if request.user.user_role == User.Role.ADMIN_USER:
            return redirect('home_page')
        if request.user.user_role == User.Role.KPI:
            return redirect('improvement')
        if request.user.user_role == User.Role.SBM_COORDINATOR:
            return redirect('yearly_indicator')
        if request.user.user_role == User.Role.CHAIRPERSON:
            return redirect('task_manager')
        return view_func(request,*args,**kwargs)
    
    return _wrapped_view

def only_kpi(view_func):
    @wraps(view_func)
    def _wrapped_view(request,*args,**kwargs):
        if request.user.user_role != User.Role.KPI:
            return redirect('home_page')
        return view_func(request,*args,**kwargs)
    
    return _wrapped_view

def only_leader(view_func):
    @wraps(view_func)
    def _wrapped_view(request,*args,**kwargs):
        if request.user.user_role == User.Role.MEMBER:
            return redirect('home_page')
        return view_func(request,*args,**kwargs)
    
    return _wrapped_view