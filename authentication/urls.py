from django.urls import path
from authentication.views import auth_login,auth_logout,auth_register,auth_finish_profile

urlpatterns = [
    path('',auth_login,name='auth_login'),
    path('register/',auth_register,name='auth_register'),
    path('finish/',auth_finish_profile,name='finish'),
    path('logout/',auth_logout,name='auth_logout')
]