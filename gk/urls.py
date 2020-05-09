from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('calculator/', include('backend.calculator.urls')),
    path('accounts/', include('allauth.urls')),
    path('feedback/', include('backend.feedback.urls')),
    path('profile/', include('backend.profile.urls')),
    path('', include('backend.news.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
