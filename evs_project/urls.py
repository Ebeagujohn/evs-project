from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),

     # Visiting the bare root URL (e.g. http://127.0.0.1:8000/) sends the
    # user straight to the registration page instead of a 404.
    path('', RedirectView.as_view(pattern_name='voters:voters_register', permanent=False)),
    
    path('voters/', include('voters.urls')),
    path('candidates/', include('candidates.urls')),
    path('voting/', include('voting.urls')),
    path('dashboard/', include('dashboard.urls')),  # optional, for admin users only
]
