from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('UPLOAD', views.upload_document, name='upload_document'),

    #path('profile_update', views.profile_update, name='profile_update'),

    #path('profile', views.profile, name='profile'),
]