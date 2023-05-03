from django.urls import path
from . import views

app_name = "learning"
urlpatterns = [
    #write paths to pages
    path('', views.index),
]