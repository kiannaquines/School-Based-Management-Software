from django.urls import path
from client.views import member_index_page,user_logout,member_upload_page,upload,my_uploads_page,performance_improvement,assessment_score,final_rating,access_form_manage,quality_form_manage,efficiency_form_manage,task_manager,addtask,DeleteTaskView,updatetask,update_profile,view_description,member_manage_media,upload_profile_picture,coordinator_progress_indicator,coordinator_home_page,verify_task
from django.urls import reverse

from app.views import home_page,progress_indicator

urlpatterns = [
    path('',member_index_page,name='index'),
    path('logout/',user_logout,name='member_logout'),
    path('upload/<int:task_id>',member_upload_page,name='upload_files'),
    path('upload_file/',upload,name='upload_file'),
    path('upload/my/files',my_uploads_page,name='my_files'),
    path('tool/performance/performance-improvement/',performance_improvement,name='improvement'),
    path('tool/performance/sbm-assessment-score/',assessment_score,name='assessment_score'),
    path('tool/performance/final-rating/',final_rating,name='myfinal_rating'),
    path('save/access_form_manage',access_form_manage,name="access_form_manage"),
    path('save/efficiency_form_manage',efficiency_form_manage,name="efficiency_form_manage"),
    path('save/quality_form_manage',quality_form_manage,name="quality_form_manage"),
    path('task/manage',task_manager,name="task_manager"),
    path('task/manage/add',addtask,name="addtask"),
    path('task/manage/remove/<int:task_id>',DeleteTaskView.as_view(),name="remove_task"),
    path('task/manage/edit/<int:task_id>',updatetask,name="edit_task"),
    path('task/manage/verify/<int:task_id>',verify_task,name="verify_task"),


    path('profile/update-profile', update_profile, name="update_profile"),
    path('task/description/view', view_description, name="view_description"),
    path('pictures/list',member_manage_media,name="member_manage_media"),

    path('upload/profile',upload_profile_picture,name="upload_profile_picture"),


    path('graphs/yealy/indicators',coordinator_home_page,name="yearly_indicator"),
    path('graphs/year/indicators',coordinator_progress_indicator,name="year_indicator")
]