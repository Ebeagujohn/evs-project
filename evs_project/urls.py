from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.onboarding, name='onboarding'),
    path('voters/', include('voters.urls')),
    path('candidates/', include('candidates.urls')),
    path('voting/', include('voting.urls')),
    path('dashboard/', include('dashboard.urls')),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]