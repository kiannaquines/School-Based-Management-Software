from django import forms
from app.models import Task
from django_ckeditor_5.widgets import CKEditor5Widget
from authentication.models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

class ChairTaskForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super(ChairTaskForm,self).__init__(*args,**kwargs)
        self.fields['task_name'].label = 'Enter your task name'
        self.fields['task_description'].label = 'Enter your task description'
        self.fields['task_description'].required = False
        self.fields['assigned_to'].label = 'Select Assgined to'
        self.fields['is_active'].label = 'Task Active Status'
        self.fields['task_status'].label = 'Task Submission Status'
        self.fields['status'].label = 'Select task status'
        self.fields['task_due'].label = 'Enter the task due'
        self.fields['principle'].label = 'Select task principle'
        self.fields['is_active'].widget.attrs.update({'class':'form-check-input'})
        self.fields['task_status'].widget.attrs.update({'class':'form-check-input'})

        users_with_pending_tasks = Task.objects.filter(status=Task.TaskStatus.PENDING).values_list('assigned_to', flat=True)
        queryset = User.objects.exclude(id__in=users_with_pending_tasks).filter(user_role=User.Role.MEMBER)
        self.fields['assigned_to'].queryset = queryset


    class Meta:
        model = Task
        fields = '__all__'

        widgets = {
            "task_description": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="extends"
            ),
            "task_due": forms.TextInput(attrs={'type':'date'})
        }


class UpdateClientProfileForm(UserChangeForm):
    def __init__(self, *args,**kwargs):
        super(UpdateClientProfileForm,self).__init__(*args,**kwargs)

        self.fields['username'].required = True
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

        self.fields['username'].label = "Enter username"
        self.fields['email'].label = "Enter email address"
        self.fields['user_mobile'].label = "Enter mobile number"
        self.fields['first_name'].label = "Enter firstname"
        self.fields['middle_name'].label = "Enter middlename"
        self.fields['last_name'].label = "Enter lastname"

        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email address'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Firstname'})
        self.fields['middle_name'].widget.attrs.update({'placeholder': 'Middlename'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Lastname'})
        self.fields['user_mobile'].widget.attrs.update({'placeholder': 'Ex: 09050686933'})

    class Meta:
        model = get_user_model()
        fields = ("username","email","first_name","last_name","middle_name","user_mobile",)

