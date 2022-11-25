
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf.urls.static import static
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path('',include('Something.urls')),
    re_path(r'^media/(?P<path>.*)$',serve, {'document_root': settings.MEDIA_ROOT}),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
