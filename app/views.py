from django.http import FileResponse, HttpResponse,JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from app.decorators import only_admin
from app.models import AssessmentScore, Document,Task,AccessRate,SchoolYear,Efficiency,QualityRate,PerformanceImprovementInterpretation,AssessmentScoreInterpretation,FinalRatingInterpretation,Rating
from django.core.paginator import Paginator
import os
from main.settings import MEDIA_ROOT
from authentication.models import User
from django.utils import timezone
from django.db.models import Q
@login_required(login_url=reverse_lazy('auth_login'))
def get_path(request):
    return request.path

def transform_school_years(years):
    transformed_years = []
    final_transformed_years = []


    for i in range(0, len(years), 3):
        start_year = years[i]
        end_year = years[i + 2] if i + 2 < len(years) else years[i]
        transformed_years.append(f"{start_year}-{end_year}")

    for year_range in transformed_years:
        year_parts = year_range.split('-')    
        final_transformed_years.append(f"{year_parts[0]}-{year_parts[3]}")

    return final_transformed_years

@only_admin
@login_required(login_url=reverse_lazy('auth_login'))
def home_page(request):
    context = {}
    context['home_path'] = get_path(request)
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
    return render(request,'index.html',context)


def progress_indicator(request):
    context = {}
    context['efficiency_school_years'] = Efficiency.objects.all()
    context['quality_school_years'] = QualityRate.objects.all()
    context['access_school_years'] = AccessRate.objects.all()
    context['graduation_school_years'] = Efficiency.objects.select_related('graduation_school_year_one','graduation_school_year_two','graduation_school_year_three')
    context['progress_indicator'] = get_path(request)
    return render(request,"progress_indicator.html",context)

@only_admin
@login_required(login_url=reverse_lazy('auth_login'))
def manage_document(request):
    context = {}

    years_obj = SchoolYear.objects.all()
    current_years = []
    for year in years_obj:
        current_years.append(year)
    context['current_years'] = current_years

    if 'principle' in request.GET and request.GET.get('principle') != 'default' and 'year' in request.GET:

        document = Document.objects.exclude(Q(document_type='png') | Q(document_type='jpeg') | Q(document_type='jpg')).order_by('-document_type').filter(task__current_sy=request.GET.get('year')).filter(task__principle=request.GET.get('principle'))
        context['selected_option'] = request.GET.get('principle')
        
    elif 'principle' in request.GET and request.GET.get('principle') == 'default' and request.GET.get('year') == '':
        document = Document.objects.exclude(Q(document_type='png') | Q(document_type='jpeg') | Q(document_type='jpg')).order_by('-document_type')
        context['selected_option'] = None
    else:
        document = Document.objects.exclude(Q(document_type='png') | Q(document_type='jpeg') | Q(document_type='jpg')).order_by('-document_type')
        context['selected_option'] = request.GET.get('principle')


    paginator = Paginator(document,8)
    page = request.GET.get('page')
    objects = paginator.get_page(page)

    context['documents'] = objects
    context['manage_document'] = get_path(request)
    context['options'] = AssessmentScore.AssessmentPrincipleType
    return render(request,'manage_documents.html',context)


@only_admin
@login_required(login_url=reverse_lazy('auth_login'))
def manage_media(request):
    context = {}
    document = Document.objects.exclude(Q(document_type='pdf') | Q(document_type='docx') | Q(document_type='doc')).order_by('-document_type')
    paginator = Paginator(document,8)
    page = request.GET.get('page')
    objects = paginator.get_page(page)

    context['medias'] = objects
    context['manage_media'] = get_path(request)
    return render(request,'manage_media.html',context)


@login_required(login_url=reverse_lazy('auth_login'))
def download_file(request,document_id):
    document_id = document_id
    document_instance = Document.objects.get(id=document_id)
    document_instance.download_count = document_instance.download_count + 1
    document_instance.save()
    document_path = os.path.join(MEDIA_ROOT,'document',document_instance.document.path)
    response = FileResponse(open(document_path, 'rb'))
    return response

@login_required(login_url=reverse_lazy('auth_login'))
def view_pdf(request,document_id):
    document_instance = Document.objects.get(id=document_id)
    document_path = os.path.join(MEDIA_ROOT,'document',document_instance.document.path)

    with open(document_path,'rb') as pdf:
        response = HttpResponse(pdf.read(),content_type='application/pdf')
        response['Content-Disposition'] = f'filename="{str(document_instance.document_name)}"'
        return response
    

@login_required(login_url=reverse_lazy('auth_login'))
def dropout_progress_tracker(request):
    if request.method == "POST":
        if 'id' in request.POST:
            dropout = Efficiency.objects.get(id=request.POST.get('id'))
            data_json = {
                'school_year_one':{
                    'dropout_sy_one': dropout.drop_school_year_one.school_year,
                    'rate': dropout.drop_dropoutrate_one,
                },
                'school_year_two':{
                    'dropout_sy_two': dropout.drop_school_year_two.school_year,
                    'rate': dropout.drop_dropoutrate_two,
                },
                'school_year_three':{
                    'dropout_sy_three': dropout.drop_school_year_three.school_year,
                    'rate': dropout.drop_dropoutrate_three,
                }
            }
            return JsonResponse({'data': data_json })
        
        return JsonResponse({'message':'empty_id'})
    
    return JsonResponse({'message':'invalid_request'})

@login_required(login_url=reverse_lazy('auth_login'))
def national_achievement_test_tracker(request):
    if request.method == "POST":
        if 'id' in request.POST:
            nat = QualityRate.objects.get(id=request.POST.get('id'))
            data_json = {
                'school_year_one':{
                    'nat_sy_one': nat.quality_school_year_one.school_year,
                    'rate': nat.quality_rate_one,
                },
                'school_year_two':{
                    'nat_sy_two': nat.quality_school_year_two.school_year,
                    'rate': nat.quality_rate_two,
                },
                'school_year_three':{
                    'nat_sy_three': nat.quality_school_year_three.school_year,
                    'rate': nat.quality_rate_three,
                }
            }
            return JsonResponse({'data': data_json })
        
        return JsonResponse({'message':'empty_id'})
    
    return JsonResponse({'message':'invalid_request'})

@login_required(login_url=reverse_lazy('auth_login'))
def enrollment_progress_tracker(request):
    if request.method == "POST":
        if 'id' in request.POST:
            access = AccessRate.objects.get(id=request.POST.get('id'))
            data_json = {
                'enrollment_year_one':{
                    'sy': access.school_year_one.school_year,
                    'rate': access.enrollment_increase_one,
                },
                'enrollment_year_two':{
                    'sy': access.school_year_two.school_year,
                    'rate': access.enrollment_increase_two,
                },
                'enrollment_year_three':{
                    'sy': access.school_year_three.school_year,
                    'rate': access.enrollment_increase_three,
                }
            }
            return JsonResponse({'data': data_json })
        
        return JsonResponse({'message':'empty_id'})
    
    return JsonResponse({'message':'invalid_request'})

@login_required(login_url=reverse_lazy('auth_login'))
def graduation_progress_tracker(request):
    if request.method == "POST":
        if 'id' in request.POST:
            graduates = Efficiency.objects.get(id=request.POST.get('id'))
            data_json = {
                'graduates_year_one':{
                    'sy': graduates.graduation_school_year_one.school_year,
                    'rate': graduates.graduation_rate_one,
                },
                'graduates_year_two':{
                    'sy': graduates.graduation_school_year_two.school_year,
                    'rate': graduates.graduation_rate_two,
                },
                'graduates_year_three':{
                    'sy': graduates.graduation_school_year_three.school_year,
                    'rate': graduates.graduation_rate_three,
                }
            }
            return JsonResponse({'data': data_json })
        
        return JsonResponse({'message':'empty_id'})
    
    return JsonResponse({'message':'invalid_request'})




def efficacy_improvement_list(request):
    context = {}
    context['efficacy_path'] = get_path(request)

    efficacy_instances = PerformanceImprovementInterpretation.objects.all()
    paginator = Paginator(efficacy_instances,6)
    page = request.GET.get('page')
    objects = paginator.get_page(page)
    context['efficacy_list'] = objects

    return render(request,"efficacy_improvement.html",context)


def assessment_score_list(request):
    context = {}
    assessment_instances = AssessmentScoreInterpretation.objects.all()
    paginator = Paginator(assessment_instances,6)
    page = request.GET.get('page')
    objects = paginator.get_page(page)
    context['assessment_score_path'] = get_path(request)
    context['assessment_list'] = objects
    return render(request,"assessment_score.html",context)


def final_rating_list(request):
    context = {}
    context['final_rating_path'] = get_path(request)
    final_rating_instances = FinalRatingInterpretation.objects.all()
    paginator = Paginator(final_rating_instances,6)
    page = request.GET.get('page')
    objects = paginator.get_page(page)
    context['final_rating_list'] = objects
    return render(request,"final_rating.html",context)



def rating_assessment_list(request):
    context = {}
    context['rating_list_path'] = get_path(request)
    rating_document = Rating.objects.all()
    paginator = Paginator(rating_document,6)
    page = request.GET.get('page')
    objects = paginator.get_page(page)
    context['rating_list'] = objects
    return render(request,"rating_interpretation.html",context)

def rating_view_matrix(request,rating_id):
    context = {}
    context['matrix_data'] = Rating.objects.get(id=rating_id)
    context['matrix_view_path'] = get_path(request)
    return render(request,"view_matrix.html",context)
