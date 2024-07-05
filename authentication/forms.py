from django import forms
from authentication.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class RegisterForm(UserCreationForm):
    def __init__(self,*args,**kwargs):
        super(RegisterForm,self).__init__(*args,**kwargs)

        self.fields['username'].required = True
        self.fields['password1'].required = True
        self.fields['password2']. required = True

        self.fields['first_name'].label = "Firstname"
        self.fields['last_name'].label = "Lastname"

        self.fields['first_name'].widget.attrs.update({'placeholder': 'Enter your firstname'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Enter your lastname'})

        self.fields['username'].widget.attrs.update({'placeholder': 'Enter your username'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_role = User.Role.MEMBER
        user.is_active = False
        if commit:
            user.save()
        return user
    
    class Meta:
        model = get_user_model()
        fields = ('username','first_name','last_name','password1', 'password2')

class LoginForm(forms.Form):
    def __init__(self,*args,**kwargs):
        super(LoginForm,self).__init__(*args,**kwargs)

        self.fields['username'].required = True
        self.fields['password'].required = True

        self.fields['username'].label = "Username"
        self.fields['password'].label = "Password"

    username = forms.CharField(widget=forms.TextInput(attrs=({'placeholder':'Username'})), max_length=255,)
    password = forms.CharField(widget=forms.PasswordInput(attrs=({'placeholder':'Password'})),max_length=255)
