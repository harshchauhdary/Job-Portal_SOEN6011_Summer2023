from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('register', views.registration, name='register'),
    path('logout', views.logout, name='logout')
]
