from django.urls import path
from . import views

app_name = "student_portal"
urlpatterns = [
    #write paths to pages
    path('', views.index),
]