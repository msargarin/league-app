"""
URL configuration for league project.
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    path('', include('api.urls')),
]
