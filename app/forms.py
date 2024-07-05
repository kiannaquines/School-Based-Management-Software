from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth import get_user_model
from authentication.models import User
from app.models import SchoolYear, Task,AccessRate,Efficiency,QualityRate,AssessmentScore,ImprovementScore
from django_ckeditor_5.widgets import CKEditor5Widget

class NewUserForm(UserCreationForm):
    def __init__(self, *args,**kwargs):
        super(NewUserForm,self).__init__(*args,**kwargs)

        self.fields['username'].required = True
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['password1'].required = True
        self.fields['password2'].required = True
        self.fields['user_role'].required = True


        self.fields['username'].label = "Enter username"
        self.fields['email'].label = "Enter email address"
        self.fields['first_name'].label = "Enter firstname"
        self.fields['last_name'].label = "Enter lastname"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"
        self.fields['user_role'].label = "Select User Role"


        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email address'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Firstname'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Lastname'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})

    class Meta:
        model = get_user_model()
        fields = ("username","email","first_name","last_name","user_role","password1","password2")

class UpdateUserForm(UserChangeForm):
    def __init__(self, *args,**kwargs):
        super(UpdateUserForm,self).__init__(*args,**kwargs)

        self.fields['username'].required = True
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['user_role'].required = True


        self.fields['username'].label = "Enter username"
        self.fields['email'].label = "Enter email address"
        self.fields['first_name'].label = "Enter firstname"
        self.fields['last_name'].label = "Enter lastname"
        self.fields['user_role'].label = "Select User Role"


        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email address'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Firstname'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Lastname'})

    class Meta:
        model = get_user_model()
        fields = ("username","email","first_name","last_name","user_role")


class TaskForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(TaskForm,self).__init__(*args,**kwargs)
        self.fields['task_name'].label = 'Enter your task name'
        self.fields['task_description'].label = 'Enter your task description'
        self.fields['task_description'].required = False
        self.fields['assigned_to'].label = 'Select Assgined to'
        self.fields['assigned_by'].label = 'Select Assigned by'
        self.fields['is_active'].label = 'Task Active Status'
        self.fields['task_status'].label = 'Task Submission Status'
        self.fields['status'].label = 'Select task status'
        self.fields['task_due'].label = 'Enter the task due'
        self.fields['is_active'].widget.attrs.update({'class':'form-check-input'})
        self.fields['task_status'].widget.attrs.update({'class':'form-check-input'})
        
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'task_due': forms.TextInput(attrs=({'type':'date'})),
            'task_description': CKEditor5Widget(attrs=({'class':'django_ckeditor_5'}),config_name="extends")
        }


class AccessRateForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(AccessRateForm,self).__init__(*args,**kwargs)

        self.fields['school_year_one'].required = True
        self.fields['school_year_two'].required = True
        self.fields['school_year_three'].required = True
        self.fields['enrollment_increase_one'].required = True
        self.fields['enrollment_increase_two'].required = True
        self.fields['enrollment_increase_three'].required = True
        self.fields['school_year_one'].label = "Enter school year"
        self.fields['school_year_two'].label = "Enter school year"
        self.fields['school_year_three'].label = "Enter school year"
        self.fields['enrollment_increase_one'].label = "School year enrollment increase"
        self.fields['enrollment_increase_two'].label = "School year enrollment increase"
        self.fields['enrollment_increase_three'].label = "School year enrollment increase"
        self.fields['percent_increase_two'].label = "% Increase"
        self.fields['percent_increase_three'].label = "% Increase"
        self.fields['average'].label = "Average"
        self.fields['final_result'].label = "Result"

        self.fields['school_year_one'].queryset = SchoolYear.objects.filter(is_active=True)
        self.fields['school_year_two'].queryset = SchoolYear.objects.filter(is_active=True)
        self.fields['school_year_three'].queryset = SchoolYear.objects.filter(is_active=True)

    class Meta:
        model = AccessRate
        fields = '__all__'

        widgets = {
            'school_year_one': forms.Select(),
            'school_year_two': forms.Select(),
            'school_year_three': forms.Select(),
            'enrollment_increase_one': forms.TextInput(attrs=({'type':'number','placeholder':'Enrollment Increase'})),
            'enrollment_increase_two': forms.TextInput(attrs=({'type':'number','placeholder':'Enrollment Increase'})),
            'enrollment_increase_three': forms.TextInput(attrs=({'type':'number','placeholder':'Enrollment Increase'})),
            'percent_increase_two': forms.TextInput(attrs=({'placeholder':'Calculated Increase','readonly':'true'})),
            'percent_increase_three': forms.TextInput(attrs=({'placeholder':'Calculated Increase','readonly':'true'})),
            'average': forms.TextInput(attrs=({'placeholder':'Calculated Average','readonly':'true'})),
            'final_result': forms.TextInput(attrs=({'placeholder':'Calculated Final Result','readonly':'true'})),
        }

class EfficiencyForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(EfficiencyForm,self).__init__(*args,**kwargs)
        # DROPOUT
        self.fields['drop_school_year_one'].required = True
        self.fields['drop_school_year_two'].required = True
        self.fields['drop_school_year_three'].required = True

        self.fields['drop_school_year_one'].queryset = SchoolYear.objects.filter(is_active=True)
        self.fields['drop_school_year_two'].queryset = SchoolYear.objects.filter(is_active=True)
        self.fields['drop_school_year_three'].queryset = SchoolYear.objects.filter(is_active=True)

        self.fields['drop_dropoutrate_one'].required = True
        self.fields['drop_dropoutrate_two'].required = True
        self.fields['drop_dropoutrate_three'].required = True
        # GRADUATION
        self.fields['graduation_school_year_one'].required = True
        self.fields['graduation_school_year_two'].required = True
        self.fields['graduation_school_year_three'].required = True

        self.fields['graduation_school_year_one'].queryset = SchoolYear.objects.filter(is_active=True)
        self.fields['graduation_school_year_two'].queryset = SchoolYear.objects.filter(is_active=True)
        self.fields['graduation_school_year_three'].queryset = SchoolYear.objects.filter(is_active=True)

        self.fields['graduation_rate_one'].required = True
        self.fields['graduation_rate_two'].required = True
        self.fields['graduation_rate_three'].required = True
        # PROMOTION
        self.fields['promotion_school_year_one'].required = True
        self.fields['promotion_school_year_two'].required = True
        self.fields['promotion_school_year_three'].required = True


        self.fields['promotion_school_year_one'].queryset = SchoolYear.objects.filter(is_active=True)
        self.fields['promotion_school_year_two'].queryset = SchoolYear.objects.filter(is_active=True)
        self.fields['promotion_school_year_three'].queryset = SchoolYear.objects.filter(is_active=True)

        self.fields['promotion_rate_one'].required = True
        self.fields['promotion_rate_two'].required = True
        self.fields['promotion_rate_three'].required = True

        # GRADUATION
        self.fields['graduation_school_year_one'].label = "Enter school year"
        self.fields['graduation_school_year_two'].label = "Enter school year"
        self.fields['graduation_school_year_three'].label = "Enter school year"
        self.fields['graduation_rate_one'].label = "Enter school year graduation rate"
        self.fields['graduation_rate_two'].label = "Enter school year graduation rate"
        self.fields['graduation_rate_three'].label = "Enter school year graduation rate"
        self.fields['graduation_rate_average'].label = "Increase Average"
        self.fields['graduation_increase_per_two'].label = "% Increase"
        self.fields['graduation_increase_per_three'].label = "% Increase"
        self.fields['graduation_increase_average'].label = "% Increase Average"

        self.fields['graduation_base_line_status'].widget.attrs.update({'readonly':'true'})

        # PROMOTION
        self.fields['promotion_school_year_one'].label = "Enter school year"
        self.fields['promotion_school_year_two'].label = "Enter school year"
        self.fields['promotion_school_year_three'].label = "Enter school year"
        self.fields['promotion_rate_one'].label = "Promotion Rate"
        self.fields['promotion_rate_two'].label = "Promotion Rate"
        self.fields['promotion_rate_three'].label = "Promotion Rate"
        self.fields['promotion_rate_average'].label = "Promotion Average"
        self.fields['promotion_increase_per_two'].label = "% Increase"
        self.fields['promotion_increase_per_three'].label = "% Increase"
        self.fields['promotion_increase_average'].label = "% Increase Average"

        self.fields['promotion_base_line_status'].widget.attrs.update({'readonly':'true'})
        # DROPOUT
        self.fields['drop_school_year_one'].label = "Enter school year"
        self.fields['drop_school_year_two'].label = "Enter school year"
        self.fields['drop_school_year_three'].label = "Enter school year"
        self.fields['drop_dropoutrate_one'].label = "School year dropout rate"
        self.fields['drop_dropoutrate_two'].label = "School year dropout rate"
        self.fields['drop_dropoutrate_three'].label = "School year dropout rate"
        self.fields['drop_percent_increase_two'].label = "% Increase"
        self.fields['drop_percent_increase_three'].label = "% Increase"
        self.fields['drop_percent_decrease'].label = "% Decrease"
        self.fields['drop_average'].label = "Average"


        self.fields['sub_total'].label = "Sub-total"


        self.fields['dropout_base_line_status'].widget.attrs.update({'readonly':'true'})

    class Meta:
        model = Efficiency
        fields = '__all__'
        widgets = {
            # Dropout Rate
            'drop_percent_increase_two': forms.TextInput(attrs=({'readonly':'true'})),
            'drop_percent_increase_three': forms.TextInput(attrs=({'readonly':'true'})),
            'drop_percent_decrease': forms.TextInput(attrs=({'readonly':'true'})),
            'drop_average': forms.TextInput(attrs=({'readonly':'true'})),

            # Graduation Rate
            'graduation_rate_average': forms.NumberInput(attrs=({'readonly':'true'})),
            'graduation_increase_average': forms.TextInput(attrs=({'readonly':'true'})),
            'percent_increase_two': forms.TextInput(attrs=({'readonly':'true'})),
            'percent_increase_three': forms.TextInput(attrs=({'readonly':'true'})),
            'average': forms.TextInput(attrs=({'readonly':'true'})),
            'graduation_increase_per_two':forms.TextInput(attrs=({'readonly':'true'})),
            'graduation_increase_per_three':forms.TextInput(attrs=({'readonly':'true'})),

             # Promotion Rate
            'promotion_rate_average': forms.TextInput(attrs=({'readonly':'true'})),
            'promotion_increase_average': forms.TextInput(attrs=({'readonly':'true'})),
            'promotion_increase_per_two':forms.TextInput(attrs=({'readonly':'true'})),
            'promotion_increase_per_three':forms.TextInput(attrs=({'readonly':'true'})),

            'sub_total':forms.TextInput(attrs=({'type':'number','readonly':'true'})),
        }


class QualityRateForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(QualityRateForm,self).__init__(*args,**kwargs)

        self.fields['quality_school_year_one'].queryset = SchoolYear.objects.filter(is_active=True)
        self.fields['quality_school_year_two'].queryset = SchoolYear.objects.filter(is_active=True)
        self.fields['quality_school_year_three'].queryset = SchoolYear.objects.filter(is_active=True)

        self.fields['quality_school_year_one'].required = True
        self.fields['quality_school_year_two'].required = True
        self.fields['quality_school_year_three'].required = True
        self.fields['quality_rate_one'].required = True
        self.fields['quality_rate_two'].required = True
        self.fields['quality_rate_three'].required = True
    
        self.fields['quality_school_year_one'].label = "Enter school year"
        self.fields['quality_school_year_two'].label = "Enter school year"
        self.fields['quality_school_year_three'].label = "Enter school year"
        self.fields['quality_rate_one'].label = "Quality Rate"
        self.fields['quality_rate_two'].label = "Quality Rate"
        self.fields['quality_rate_three'].label = "Quality Rate"
        self.fields['quality_rate_average'].label = "Average"
        self.fields['quality_rate_two_percentage'].label = "% Increase"
        self.fields['quality_rate_three_percentage'].label = "% Increase"
        self.fields['quality_rate_average_percentage'].label = "% Increase Average"
        self.fields['quality_final_result'].label = "Final Result"


        self.fields['quality_rate_average'].widget.attrs.update({'readonly':'true'})
        self.fields['quality_final_result'].widget.attrs.update({'readonly':'true'})
        self.fields['quality_rate_three_percentage'].widget.attrs.update({'readonly':'true'})
        self.fields['quality_rate_two_percentage'].widget.attrs.update({'readonly':'true'})
        self.fields['quality_rate_average_percentage'].widget.attrs.update({'readonly':'true'})
        

    class Meta:
        model = QualityRate
        fields = '__all__'

        widgets = {
            'quality_school_year_one': forms.Select(),
            'quality_school_year_two': forms.Select(),
            'quality_school_year_three': forms.Select(),
            'quality_final_result': forms.TextInput(attrs=({'type':'number', 'placeholder':'Calculated Final Result','readonly':'true'})),
        }



class AssessmentScoreForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(AssessmentScoreForm,self).__init__(*args,**kwargs)
        self.fields['principle'].label = 'Select Principle'
        self.fields['weight'].label = 'Select Principle Weight'
        self.fields['principle_score'].label = 'Principle Score'
        self.fields['cumulative_score'].label = 'Cumulative Score'
        self.fields['result'].label = 'Result'

        self.fields['cumulative_score'].widget.attrs.update({
            'readonly':'true'
        })

        self.fields['result'].widget.attrs.update({
            'readonly':'true'
        })
    
    class Meta:
        model = AssessmentScore
        fields = '__all__'



class ImprovementScoreForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(ImprovementScoreForm,self).__init__(*args,**kwargs)
        self.fields['area'].label = 'Select Area'
        self.fields['weight'].label = 'Select Weight'
        self.fields['rating'].label = 'Rating'
        self.fields['result'].label = 'Result'

        self.fields['result'].widget.attrs.update({
            'readonly':'true'
        })
    
    class Meta:
        model = ImprovementScore
        fields = '__all__'