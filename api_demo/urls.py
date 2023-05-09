"""api_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path, include

import sample.views.api as sample_views_api
import sample.views.demo as sample_views_demo

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api-auth/', include('rest_framework.urls')),

    path("accounts/", include("django.contrib.auth.urls")),

    # API
    path('api/long-running-task/', sample_views_api.long_running_task, name='api_long_running_task'),
    path('api/tuned-long-running-task/', sample_views_api.long_running_task_with_tuning,
         name='api_long_running_task_with_tuning'),
    path('api/tuned-long-running-task/<str:task_id>/', sample_views_api.get_long_running_task_status,
         name='api_get_long_running_task_status'),

    # Demo
    path('', sample_views_demo.index, name='index'),
    path('submit-default', sample_views_demo.submit_default, name='submit_default'),
    path('submit-with-tuning', sample_views_demo.submit_with_tuning, name='submit_with_tuning'),
]
