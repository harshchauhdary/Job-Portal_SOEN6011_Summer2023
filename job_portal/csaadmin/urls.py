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
    path('candidate_profile/<int:pk>/', views.candidate_profile, name='candidate_profile'),
    path('employer_profile/<int:pk>/', views.employer_profile, name='employer_profile'),
    path('view_resume/<int:pk>/', views.view_resume, name='view_resume'),
    path('download/<int:pk>/', views.download, name='download'),
    path('view_employer_jobs/<int:pk>/', views.view_employer_jobs, name='view_employer_jobs'),
    path('view_job/<int:pk>/', views.view_job, name='view_job'),
    path('change_email/<str:role>/<int:pk>/', views.change_email, name='change_email'),
    path('reset_password/<str:role>/<int:pk>/', views.reset_password, name='reset_password'),
]

