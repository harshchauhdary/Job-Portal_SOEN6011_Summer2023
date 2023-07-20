# from django.urls import path
# from . import views

# urlpatterns = [
#     path('browse_candidates/', views.browse_candidates, name='browse_candidates'),
#     path('addJob/', views.add_job, name='add_job'),
#     path('viewJob/<int:job_id>/', views.view_job, name='view_job'),
#     path('updateJob/<int:job_id>/', views.update_job, name='update_job'),
# ]

from django.urls import path
from . import views

app_name = 'employer'

urlpatterns = [
    path('browseCandidates/<int:job_id>/', views.browse_candidates, name='browse_candidates'),
    path('browseCandidatesAll/', views.browse_candidates_all, name='browse_candidates_all'),
    path('addJob/', views.add_job, name='add_job'),
    path('viewJob/<int:job_id>/', views.view_job, name='view_job'),
    path('updateJob/<int:job_id>/', views.update_job, name='update_job'),
    path('profile/', views.view_employer_profile, name='view_employer_profile'),
    path('profile/create/', views.create_employer_profile, name='create_employer_profile'),
    path('profile/update/', views.update_employer_profile, name='update_employer_profile'),
    path('viewJobs/', views.view_jobs, name='view_jobs'),
]
