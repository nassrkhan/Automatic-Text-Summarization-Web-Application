from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),

    #path('profile_update', views.profile_update, name='profile_update'),

    #path('profile', views.profile, name='profile'),
]