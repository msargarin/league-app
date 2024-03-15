"""
URL configuration for league project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # DRF basic authentication urls
    path('api-auth/', include('rest_framework.urls')),

    # Django admin
    path('admin/', admin.site.urls),
]
