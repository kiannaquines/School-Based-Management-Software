from app.decorators import only_user,only_leader,only_kpi
from django.contrib.auth import logout
from app.views import get_path, transform_school_years
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy,reverse
from django.utils import timezone
from django.http import JsonResponse,HttpResponse
from django.core.paginator import Paginator
from app.forms import AccessRateForm,QualityRateForm,EfficiencyForm,AssessmentScoreForm,ImprovementScoreForm
from client.forms import UpdateClientProfileForm,ChairTaskForm
from django.views.generic import DeleteView
from django.forms import BaseModelForm
from django.contrib import messages
from django.db.models import Q
from app.models import Document, SchoolYear,Task,PerformanceImprovementInterpretation,AssessmentScoreInterpretation,AssessmentScore,FinalRatingInterpretation,ImprovementScore,Rating
from app.models import AccessRate,Efficiency,QualityRate
from authentication.models import User


@login_required(login_url=reverse_lazy("auth_login"))
def get_performance_improvement_sub_total(request):
    return round(float(request.session.get('access_result',0)) + float(request.session.get('efficiency_result',0)) + float(request.session.get('quality_result',0)),2)

@login_required(login_url=reverse_lazy("auth_login"))
def get_sbm_assessment_sub_total(request):
    if request:
        return round(float(request.session.get('leadership_result',0)) + float(request.session.get('curriculum_result',0)) + float(request.session.get('accountability_result',0)) + float(request.session.get('management_of_resources_result',0)),2)
    
    return float(0) 


@login_required(login_url=reverse_lazy("auth_login"))
def get_final_rating_sub_total(request):
    if request:
        return round(float(request.session.get('sbm_assessment_perf_score')) + float(request.session.get('sbm_assessment_score')),2)
    return float(0)

@login_required(login_url=reverse_lazy("auth_login"))
def fash_kpi_session(request):
    
    my_kpi_session = {
        'access_result',
        'efficiency_result',
        'leadership_result',
        'curriculum_result',
        'accountability_result',
        'management_of_resources_result',
        'sbm_assessment_perf_score',
        'sbm_assessment_score',
        'access_id',
        'efficiency_data',
        'efficiency_id',
        'quality_result',
        'quality_id',
        'leadership_id',
        'curriculum_id',
        'accountability_id',
        'management_id',
        'performance_id',
        'assessment_id',
        'curriculum_id',
    }

    for kpi_key in my_kpi_session:
        request.session.pop(kpi_key)

    request.session.save()

def user_logout(request):
    logout(request)
    return redirect('auth_login') 

@login_required(login_url=reverse_lazy("auth_login"))
def verify_task(request,task_id):
    task = Task.objects.get(id=task_id)

    if task.status == Task.TaskStatus.VERIFIED:
        messages.success(request,f"The task assigned to {task.assigned_to} is already verified, thank you!",extra_tags="already_verified")
        return redirect('task_manager')

    task.status = Task.TaskStatus.VERIFIED
    task.save()
    return redirect('task_manager')

@login_required(login_url=reverse_lazy('auth_login'))
def upload_profile_picture(request):
    if request.method == "POST":
        profile_img = request.FILES.get('file')
        user = User.objects.get(id=request.user.id)
        user.user_profile = profile_img
        user.save()
        return JsonResponse({'message':'success'})

@login_required(login_url=reverse_lazy('auth_login'))
def view_description(request):
    if request.method == "POST":

        try:
            task = Task.objects.get(id=request.POST.get('task_id'))
            return JsonResponse({'descrition':task.task_description})
        except Task.DoesNotExist:
            return JsonResponse({'message':'not_valid'})
         
    return JsonResponse({'message':'invalid'})

@login_required(login_url=reverse_lazy('auth_login'))
def update_profile(request):
    context = {}
    if request.method == "POST":
        my_profile = UpdateClientProfileForm(request.POST,instance=request.user)

        if my_profile.is_valid():
            my_profile.save()
            messages.success(request,"You have successfully update your profile information.",extra_tags="profile_updated")
            return redirect('update_profile')
    context['update_profile_path'] = get_path(request)
    context['form'] = UpdateClientProfileForm(instance=request.user)
    return render(request,"update_profile.html",context)

@login_required(login_url=reverse_lazy("auth_login"))
@only_user
def member_index_page(request):
    context = {}
    task_obj = Task.objects.filter(assigned_to=request.user)
    context['my_index_path'] = get_path(request)
    context['my_task'] = task_obj
    context['task_count'] = task_obj.count()
    return render(request,"members/member.html",context)

@login_required(login_url=reverse_lazy("auth_login"))
@only_user
def my_uploads_page(request):
    context = {}

    document = Document.objects.filter(uploaded_by=request.user).exclude(Q(document_type='jpg') | Q(document_type='png') |  Q(document_type='jpeg')).order_by('-document_type')
    paginator = Paginator(document,8)
    page = request.GET.get('page')
    objects = paginator.get_page(page)
    context['documents'] = objects
    context['my_task_path'] = get_path(request)
    return render(request,"members/my_uploads.html",context)

@login_required(login_url=reverse_lazy('auth_login'))
@only_user
def member_manage_media(request):
    context = {}
    document = Document.objects.filter(uploaded_by=request.user).exclude(Q(document_type='pdf') | Q(document_type='docx') | Q(document_type='doc')).order_by('-document_type')
    paginator = Paginator(document,8)
    page = request.GET.get('page')
    objects = paginator.get_page(page)

    context['medias'] = objects
    context['member_media_path'] = get_path(request)
    return render(request,'members/my_media.html',context)

@login_required(login_url=reverse_lazy("auth_login"))
@only_user
def member_upload_page(request,task_id):
    context = {}        
    context['my_upload_path'] = get_path(request)
    context['task_id'] = task_id
    return render(request,"members/upload.html",context)

@login_required(login_url=reverse_lazy("auth_login"))
@only_user
def upload(request):

    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('file')

        task = Task.objects.get(id=request.POST.get('task_id'))
        task.task_status = True
        task.save()

        allowed_types = [
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/pdf',
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'image/png',
            'image/jpeg',
        ]

        for upload_file in uploaded_files:
            if upload_file.content_type in allowed_types:
                file_size = upload_file.size
                file_name = upload_file.name
                file_extension = upload_file.name.split('.')[-1].lower()
                Document.objects.create(document=upload_file,document_name=file_name,document_type=file_extension,document_size=file_size,uploaded_by=request.user,task=task)
            else:
                return JsonResponse({'message': 'invalid_file'})
        
        return JsonResponse({'message':"uploaded"})
    
    return JsonResponse({'message':'invalid_request'})

@only_kpi
@login_required(login_url=reverse_lazy('auth_login'))
def performance_improvement(request):
    context = {}
    context['performance'] = get_path(request)
    my_session_data = request.session.get('efficiency_data',None)

    if my_session_data:
        context['efficiency'] = EfficiencyForm(initial=my_session_data)
    else:
        context['efficiency'] = EfficiencyForm()

    context['access_form'] = AccessRateForm()
    context['quality_form'] = QualityRateForm()

    return render(request,"kpi/performance_improvement.html",context)

@only_kpi
@login_required(login_url=reverse_lazy('auth_login'))
def access_form_manage(request):
    context = {}    
    if request.method == "POST":
        access_form = AccessRateForm(request.POST)
        if access_form.is_valid():
            request.session['access_result'] = request.POST.get('final_result')
            instance = access_form.save()
            request.session['access_id'] = instance.id
            request.session.save()
            return redirect(reverse('improvement') + f'?page=efficiency&sub=dropout&step=1')
        else:

            if access_form.has_error('school_year_one'):
                messages.success(request,access_form.errors.get('school_year_one').as_text(),extra_tags="school_year_one_error")
            elif access_form.has_error('school_year_two'):
                messages.success(request,access_form.errors.get('school_year_two').as_text(),extra_tags="school_year_two_error")
            elif access_form.has_error('school_year_three'):
                messages.success(request,access_form.errors.get('school_year_three').as_text(),extra_tags="school_year_three_error")

            return redirect('improvement')

@only_kpi
@login_required(login_url=reverse_lazy('auth_login'))
def efficiency_form_manage(request):
    context = {}
   
    if request.method == "POST":
        if request.POST.get('nextGraduation') == 'nextGraduation':
            request.session['efficiency_data'] = request.POST
            return redirect(reverse('improvement') + f'?page=efficiency&sub=graduation&step=2')
        
        if request.POST.get('nextPromotion') == 'nextPromotion':
            request.session['efficiency_data'] = request.POST
            return redirect(reverse('improvement') + f'?page=efficiency&sub=promotion&step=3')
        
        my_final_request = request.POST.copy()
        my_final_request['sub_total'] = round(((int(request.POST.get('dropout_base_line_status')) + int(request.POST.get('graduation_base_line_status')) + int(request.POST.get('promotion_base_line_status'))) / 3),2)
        my_final_request['final_result'] = round(my_final_request['sub_total'] * 0.25,2)
        request.session['efficiency_result'] = my_final_request['final_result']
        my_final_form = EfficiencyForm(my_final_request)

        if my_final_form.is_valid():
            instance = my_final_form.save()
            request.session['efficiency_id'] = instance.id
            request.session.save()
            return redirect(reverse('improvement') + f'?page=quality')
        else:
            print(request.POST.get('sub_total'))

@only_kpi
@login_required(login_url=reverse_lazy('auth_login'))
def quality_form_manage(request):    
    if request.method == "POST":
        quality_form = QualityRateForm(request.POST)
        if quality_form.is_valid():
            instance = quality_form.save()
            request.session['quality_result'] = request.POST.get('quality_final_result')
            request.session['quality_id'] = instance.id
            request.session.save()

            current_access = AccessRate.objects.get(id=request.session.get('access_id'))
            current_efficiency = Efficiency.objects.get(id=request.session.get('efficiency_id'))
            current_quality = QualityRate.objects.get(id=request.session.get('quality_id'))

            create_interpretation = PerformanceImprovementInterpretation()
            create_interpretation.access = current_access
            create_interpretation.efficiency = current_efficiency
            create_interpretation.quality = current_quality
            create_interpretation.rating = get_performance_improvement_sub_total(request)

            create_interpretation.save()

            return redirect(reverse('assessment_score') + f'?page=assessment_score')
        else:
            print(quality_form.errors)

@only_kpi
@login_required(login_url=reverse_lazy('auth_login'))
def assessment_score(request):
    context = {}
    context['assessment_rating'] = get_path(request)
    context['form'] = AssessmentScoreForm()

    if request.method == "POST":
        form = AssessmentScoreForm(request.POST)

        if form.is_valid():

            if request.POST.get('principle') == 'LEADERSHIP':
                request.session['leadership_result'] = request.POST.get('result')
                instance = form.save()
                request.session['leadership_id'] = instance.id
                request.session.save()

            if request.POST.get('principle') == 'CURRICULUM & LEARNING':
                request.session['curriculum_result'] = request.POST.get('result')
                instance = form.save()
                request.session['curriculum_id'] = instance.id
                request.session.save()


            if request.POST.get('principle') == 'ACCOUNTABILITY':
                request.session['accountability_result'] = request.POST.get('result')
                instance = form.save()
                request.session['accountability_id'] = instance.id
                request.session.save()


            if request.POST.get('principle') == 'RESOURCE MANAGEMENT':
                request.session['management_of_resources_result'] = request.POST.get('result')
                instance = form.save()
                request.session['management_id'] = instance.id
                request.session.save()


                instance_leadership = AssessmentScore.objects.get(id=request.session.get('leadership_id'))
                instance_curriculum = AssessmentScore.objects.get(id=request.session.get('curriculum_id'))
                instance_accountability = AssessmentScore.objects.get(id=request.session.get('accountability_id'))
                instance_management = AssessmentScore.objects.get(id=request.session.get('management_id'))



                create_interpretation = AssessmentScoreInterpretation()
                create_interpretation.leadership = instance_leadership
                create_interpretation.curriculum = instance_curriculum
                create_interpretation.accountability = instance_accountability
                create_interpretation.management = instance_management
                create_interpretation.rating = get_sbm_assessment_sub_total(request)

                create_interpretation.save()
                return redirect(reverse('myfinal_rating') + f"?page=final_rating&step=third")

    return render(request,"kpi/cal_assessment_score.html",context)

@only_kpi
@login_required(login_url=reverse_lazy('auth_login'))
def final_rating(request):
    context = {}
    context['final_rating'] = get_path(request)
    context['form'] = ImprovementScoreForm()
    context['perf_sub_total'] = get_performance_improvement_sub_total(request)
    context['assess_sub_total'] = get_sbm_assessment_sub_total(request)

    if request.method == "POST":
        form = ImprovementScoreForm(request.POST)

        if form.is_valid():

            if request.POST.get('area') == "Performance Improvement":
                request.session['sbm_assessment_perf_score'] = request.POST.get('result')
                instance = form.save()
                request.session['performance_id'] = instance.id
                request.session.save()

            if request.POST.get('area') == "SBM Assessment Score (DOD)":
                request.session['sbm_assessment_score'] = request.POST.get('result')
                instance = form.save()
                request.session['assessment_id'] = instance.id
                request.session.save()


                instance_performance = ImprovementScore.objects.get(id=request.session.get('performance_id'))
                instance_assessment = ImprovementScore.objects.get(id=request.session.get('assessment_id'))

                create_interpretation = FinalRatingInterpretation()
                create_interpretation.performance = instance_performance
                create_interpretation.assessment = instance_assessment
                create_interpretation.rating = get_final_rating_sub_total(request)
                create_interpretation.save()


                rating = Rating()
                rating.access_id = AccessRate.objects.get(id=request.session.get('access_id'))
                rating.efficiency_id = Efficiency.objects.get(id=request.session.get('efficiency_id'))
                rating.quality_id = QualityRate.objects.get(id=request.session.get('quality_id'))
                rating.leadership_id = AssessmentScore.objects.get(id=request.session.get('leadership_id'))
                rating.curriculum_id = AssessmentScore.objects.get(id=request.session.get('curriculum_id'))
                rating.accountability_id = AssessmentScore.objects.get(id=request.session.get('accountability_id'))
                rating.management_id = AssessmentScore.objects.get(id=request.session.get('management_id'))
                rating.performance_id = ImprovementScore.objects.get(id=request.session.get('performance_id'))
                rating.sbm_assessment_id = ImprovementScore.objects.get(id=request.session.get('assessment_id'))
                rating.save()

                fash_kpi_session(request)
                return redirect(reverse('improvement') + f'?status=complete')
            
        else:
            print(form.errors)

    return render(request,"kpi/cal_final_rating.html",context)

@only_leader
@login_required(login_url=reverse_lazy('auth_login'))
def task_manager(request):
    context = {}

    my_created_task = Task.objects.filter(assigned_by__id=request.user.id).all()
    context['created_task'] = my_created_task
    context['task_manager'] = get_path(request)
    return render(request,'chairperson/task_manager.html',context)

@only_leader
@login_required(login_url=reverse_lazy('auth_login'))
def addtask(request):
    context = {}

    if request.method == 'POST':
        task_data = request.POST.copy()
        task_data['assigned_by'] = request.user.id
        task_form = ChairTaskForm(task_data)

        if task_form.is_valid():
            messages.success(request,"You have successfully added new task.",extra_tags="added_task")
            task_form.save()
            return redirect(reverse_lazy('task_manager'))

    context['addtask'] = get_path(request)
    context['form'] = ChairTaskForm()
    return render(request,'chairperson/add_task.html',context)

@only_leader
@login_required(login_url=reverse_lazy('auth_login'))
def updatetask(request,task_id):
    context = {}

    task = Task.objects.get(id=task_id)

    if request.method == 'POST':
        task_data = request.POST.copy()
        task_data['assigned_by'] = request.user.id
        task_form = ChairTaskForm(task_data,instance=task)

        if task_form.is_valid():
            messages.success(request,f"You have successfully updated the existing task assigned to {task_form.cleaned_data['assigned_to']}.",extra_tags="update_task")
            task_form.save()
            return redirect(reverse_lazy('task_manager'))
        
    context['updatetask'] = get_path(request)
    context['form'] = ChairTaskForm(instance=task)
    return render(request,'chairperson/edit_task.html',context)

class DeleteTaskView(DeleteView):
    model = Task
    pk_url_kwarg = 'task_id'
    template_name = 'chairperson/delete_task.html'
    success_url = reverse_lazy('task_manager')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        messages.success(self.request,"You have successfully removed the existing task.",extra_tags="delete_task")
        return response
    
@login_required(login_url=reverse_lazy('auth_login'))
def coordinator_home_page(request):
    context = {}
    context['coordinator_home_page_path'] = get_path(request)
    context['member_count'] = User.objects.filter(user_role=User.Role.MEMBER).count()
    context['chair_count'] = User.objects.filter(user_role=User.Role.CHAIRPERSON).count()
    context['sbm_coordinator_count'] = User.objects.filter(user_role=User.Role.SBM_COORDINATOR).count()
    context['admin_count'] = User.objects.filter(user_role=User.Role.ADMIN_USER).count()
    context['task_list'] = Task.objects.filter(task_date_added__date=timezone.now().date())
    context['task_count'] = Task.objects.filter(task_date_added__date=timezone.now().date()).count()

    context['new_user_added_data'] = User.objects.filter(date_joined__date=timezone.now().date()).count()
    context['new_leader_added_data'] = User.objects.filter(user_role=User.Role.CHAIRPERSON,date_joined__date=timezone.now().date()).count()
    context['new_coordinator_added_data'] = User.objects.filter(user_role=User.Role.SBM_COORDINATOR,date_joined__date=timezone.now().date()).count()
    context['new_admin_added_data'] = User.objects.filter(user_role=User.Role.ADMIN_USER,date_joined__date=timezone.now().date()).count()
    context['school_years'] = SchoolYear.objects.all()
    access_enrollment = AccessRate.objects.prefetch_related('school_year_one','school_year_two','school_year_three').order_by('school_year_one')
    efficiency_data = Efficiency.objects.prefetch_related('drop_school_year_one','drop_school_year_two','drop_school_year_three','graduation_school_year_one','graduation_school_year_two','graduation_school_year_three','promotion_school_year_one','promotion_school_year_two','promotion_school_year_three')

    quality_data = QualityRate.objects.prefetch_related('quality_school_year_one','quality_school_year_two','quality_school_year_three')

    dropout_rating = Efficiency.objects.prefetch_related('drop_school_year_one','drop_school_year_two','drop_school_year_three')
    graduation_rating = Efficiency.objects.prefetch_related('graduation_school_year_one','graduation_school_year_two','graduation_school_year_three').order_by('graduation_school_year_one')
    promotion_rating = Efficiency.objects.prefetch_related('promotion_school_year_one','promotion_school_year_two','promotion_school_year_three').order_by('promotion_school_year_one')


    context['dropout_rating'] = dropout_rating
    context['graduation_rating'] = graduation_rating
    context['promotion_rating'] = promotion_rating

    dropout_labels = []
    dropout_values = []

    graduation_labels = []
    graduation_values = []

    promotion_labels = []
    promotion_values = []

    enrollment_label = []
    enrollment_values = []

    years = []
    access_values = []
    efficiency_values = []
    quality_values = []

    for access in access_enrollment:
        current_sy_first = access.school_year_one.school_year
        current_sy_second = access.school_year_two.school_year
        current_sy_third = access.school_year_three.school_year
        years.extend([current_sy_first,current_sy_second,current_sy_third])

        access_values.extend([access.final_result])
    
    for efficiency in efficiency_data:
        efficiency_values.extend([efficiency.final_result])

    for quality in quality_data:
        quality_values.extend([quality.quality_final_result])

    for dropout in dropout_rating:
        dropout_labels.extend([dropout.drop_school_year_one.school_year,dropout.drop_school_year_two.school_year,dropout.drop_school_year_three.school_year])
        dropout_values.extend([dropout.drop_dropoutrate_one,dropout.drop_dropoutrate_two,dropout.drop_dropoutrate_three])

    for graduation in graduation_rating:
        graduation_labels.extend([graduation.graduation_school_year_one.school_year,graduation.graduation_school_year_two.school_year,graduation.graduation_school_year_three.school_year])
        graduation_values.extend([graduation.graduation_rate_one,graduation.graduation_rate_two,graduation.graduation_rate_three])
        
    for promotion in promotion_rating:
        promotion_labels.extend([promotion.promotion_school_year_one.school_year,promotion.promotion_school_year_two.school_year,promotion.promotion_school_year_three.school_year])
        promotion_values.extend([promotion.promotion_rate_one,promotion.promotion_rate_two,promotion.promotion_rate_three])
       
    for enrollment in access_enrollment:
        enrollment_label.extend([enrollment.school_year_one.school_year,enrollment.school_year_two.school_year,enrollment.school_year_three.school_year])
        enrollment_values.extend([enrollment.enrollment_increase_one,enrollment.enrollment_increase_two,enrollment.enrollment_increase_three])

    context['graph_labels'] = transform_school_years(years)
    context['enrollment_label'] = enrollment_label
    context['enrollment_values'] = enrollment_values

    context['dropout_label'] = dropout_labels
    context['dropout_values'] = dropout_values

    context['graduation_labels'] = graduation_labels
    context['graduation_values'] = graduation_values

    context['promotion_labels'] = promotion_labels
    context['promotion_values'] = promotion_values

    context['access_values'] = access_values
    context['efficiency_values'] = efficiency_values
    context['quality_values'] = quality_values
    return render(request,'coordinator/graph_yearly.html',context)


def coordinator_progress_indicator(request):
    context = {}
    context['efficiency_school_years'] = Efficiency.objects.all()
    context['quality_school_years'] = QualityRate.objects.all()
    context['access_school_years'] = AccessRate.objects.all()
    context['graduation_school_years'] = Efficiency.objects.select_related('graduation_school_year_one','graduation_school_year_two','graduation_school_year_three')
    context['coordinator_progress_indicator_path'] = get_path(request)
    return render(request,"coordinator/graph_year.html",context)