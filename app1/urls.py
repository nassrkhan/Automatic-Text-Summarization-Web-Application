from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('UPLOAD', views.upload_document, name='upload_document'),
    path('summary', views.summarization, name='summary'),
]