from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('profile', views.view_Profile,
         name='user_detail'),
    path('createProfile', views.create_Profile, name='create_Profile'),
    path('updateProfile', views.update_profile, name='Update_Profile'),
]
