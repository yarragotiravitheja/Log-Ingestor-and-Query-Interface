"""
URL configuration for log_ingestor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import process_log, get_log_levels, get_resources, get_init_filter_data, fetch_logs

urlpatterns = [
    path('', view=process_log),
    path('admin/', admin.site.urls),
    path('levels', view=get_log_levels),
    path('resources', view=get_resources),
    path('init_filter', view=get_init_filter_data),
    path('fetch_logs', view=fetch_logs),
    path('django-rq/', include('django_rq.urls'))
]
