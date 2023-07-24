from django.urls import path
from . import views

app_name = 'csaadmin'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('list_candidates/', views.list_candidates, name='list_candidates'),
    path('list_employers/', views.list_employers, name='list_employers'),
    path('list_jobs/', views.list_jobs, name='list_jobs'),
    path('delete_job/<int:job_id>/', views.delete_job, name='delete_job'),
    path('delete_employer/<int:employer_id>/', views.delete_employer, name='delete_employer'),
    path('delete_candidate/<int:candidate_id>/', views.delete_candidate, name='delete_candidate'),
]

