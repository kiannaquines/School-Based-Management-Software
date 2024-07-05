from django import urls
from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static

urlpatterns = [
    path('', include('app.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('client/', include('client.urls')),
]


urlpatterns += [
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)