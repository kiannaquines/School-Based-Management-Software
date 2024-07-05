from django.urls import path 
from app.myviews.users import user_list,adduser, EditUserView, RemoveUserView,activate
from app.views import manage_document,home_page,download_file,view_pdf,progress_indicator,dropout_progress_tracker, national_achievement_test_tracker, enrollment_progress_tracker, graduation_progress_tracker,efficacy_improvement_list,assessment_score_list,final_rating_list, rating_assessment_list,rating_view_matrix,manage_media
from app.myviews.task import all_task,CreateTaskView,UpdateTaskView,DeleteTaskView,admin_verify_task

urlpatterns = [
    path('',home_page,name='home_page'),
    path('progress/indicator',progress_indicator,name="progress_indicator"),
    path('users/list',user_list,name='user_list'),
    path('users/add', adduser, name='adduser'),
    path('users/edit/<int:id>', EditUserView.as_view(), name='edituser'),
    path('users/remove/<int:id>', RemoveUserView.as_view(), name='deleteuser'),
    path('user/active/<int:user_id>',activate,name="activate"),

    path('documents/manage',manage_document,name='manage_document'),
    path('document/download/<int:document_id>',download_file,name="download_file"),
    path('document/view/<int:document_id>',view_pdf,name="view_pdf"),


    path('task/list',all_task,name='manage_task'),
    path('task/add',CreateTaskView.as_view(),name='add_task'),
    path('task/remove/<int:task_id>',DeleteTaskView.as_view(),name="delete_task"),
    path('task/edit/<int:task_id>',UpdateTaskView.as_view(),name="update_task"),


    path('indicator/dropout-tracker',dropout_progress_tracker,name="dropout_tracker"),
    path('indicator/nat-tracker',national_achievement_test_tracker,name="nat_tracker"),
    path('indicator/enollment-tracker',enrollment_progress_tracker,name="enrollment_tracker"),
    path('indicator/graduates-tracker',graduation_progress_tracker,name="graduates_tracker"),


    path('analyzer/efficacy-improvement/list',efficacy_improvement_list,name="efficacy_improvement_list"),
    path('analyzer/assessment-score/list',assessment_score_list,name="assessment_score_list"),
    path('analyzer/final-rating-list/list',final_rating_list,name="final_rating_list"),

    path('analyzer/rating/list',rating_assessment_list,name="rating_list"),
    path('analyzer/rating/view/<int:rating_id>',rating_view_matrix,name="matrix_view"),

    path('media/manage/list',manage_media,name="manage_media"),
    path('task/list/verify/<int:task_id>',admin_verify_task,name="admin_verify_task"),
]