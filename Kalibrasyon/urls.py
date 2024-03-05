"""Kalibrasyon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path, include,re_path
from rest_framework import routers
from kalibrasyonApp import views
from django.conf.urls.static import static
from django.conf import settings
from knox import views as knox_views
router = routers.DefaultRouter()
# router.register(r'data',views.Finished_list, 'data')
# router.register(r'calibrator_data',views.Calibrator_data,'calibrator_data')
# router.register(r'template_data',views.Template_data,'template_data')
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
    path('kalibrasyonApp/',include("kalibrasyonApp.urls")),
    path('api/data/',views.Finished_list.as_view(), name='data'),
    path('api/template/',views.Template_data.as_view(),name="template"),
    path('api/template_name/',views.TemplateName.as_view(),name="templateName"),
    path('api/calibrator/',views.Calibrator_data.as_view(),name="calibrator"),
    path('api/task/',views.Task_data.as_view(),name="task_data"),
    path('api/login/', views.LoginView.as_view(), name='knox_login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    path('api/user/',views.UserId.as_view(),name="user")
   
]
