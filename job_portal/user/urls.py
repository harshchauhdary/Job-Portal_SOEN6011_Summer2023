from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='clogin'),
    path('register', views.registration, name='cregister'),
    path('logout', views.logout, name='clogout')
]
