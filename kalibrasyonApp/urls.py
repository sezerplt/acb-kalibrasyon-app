from unicodedata import name
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "kalibrasyonApp"
urlpatterns = [
    path(r"logout/", views.logout_request, name="logout"),
    path(r"home/<str:username>/", views.home, name="home"),
    path(r"home/<str:username>/task_list/", views.task_list, name="tasklist"),
    path(r"home/<str:username>/task_list/finished_task/", views.finished_task, name="finished_task"),
    path(r"home/<str:username>/task_list/finished_task/measurement/<str:taskname>/", views.measurement, name="task_name"),
    path(r"excel_view/", views.excel_upload, name="excel_upload"),
   
    
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
