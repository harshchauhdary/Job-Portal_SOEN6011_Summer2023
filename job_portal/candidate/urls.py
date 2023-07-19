from django.urls import path
from . import views

urlpatterns = [
    path('job/apply/<uuid:jpk>', views.apply_Job, name="apply_Job"),
    path('createResume', views.create_Resume, name="Create_Resume"),
    path('resume', views.view_Resume, name="View_Resume"),
    path('downloadResume', views.download, name="Download_Resume"),
    path('updateResume', views.update_Resume, name="Update_Resume"),
    path('createProfile', views.create_Candidate_Profile, name="create profile"),
    path('updateProfile', views.update_candidate_profile, name="update profile"),
    path('profile', views.view_candidate_profile, name="view profile"),
    path('', views.view_Jobs, name="view jobs"),
    path('job/<uuid:jpk>', views.view_Job, name="view job")
]
