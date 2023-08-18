from django.shortcuts import render, get_object_or_404, redirect
from .models import User, Employer, Candidate, Job
from django.http import HttpResponseRedirect, FileResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password

def is_admin(request):
    # Assuming you have a custom User model with a 'role' field
    user_id = request.session.get('a_id')
    if user_id:
        try:
            user = User.objects.get(pk=user_id)
            return user.role == 'A'
        except User.DoesNotExist:
            pass
    return False

def home(request):
    if not is_admin(request):
        return HttpResponseRedirect('/') 

    num_candidates = Candidate.objects.count()
    num_employers = Employer.objects.count()
    num_jobs = Job.objects.count()

    context = {
        'num_candidates': num_candidates,
        'num_employers': num_employers,
        'num_jobs': num_jobs,
    }

    return render(request, 'csaadmin/home.html', context)

def list_candidates(request):
    if not is_admin(request):
        return HttpResponseRedirect('/') 
    candidates = Candidate.objects.all()
    return render(request, 'csaadmin/list_candidates.html', {'candidates': candidates})

def list_employers(request):
    if not is_admin(request):
        return HttpResponseRedirect('/') 
    employers = Employer.objects.all()
    return render(request, 'csaadmin/list_employers.html', {'employers': employers})

def list_jobs(request):
    if not is_admin(request):
        return HttpResponseRedirect('/') 
    jobs = Job.objects.all()
    return render(request, 'csaadmin/list_jobs.html', {'jobs': jobs})

def delete_job(request, job_id):
    if not is_admin(request):
        return HttpResponseRedirect('/') 
    job = get_object_or_404(Job, pk=job_id)
    job.delete()
    return redirect('/csaadmin/list_jobs/')

def delete_employer(request, employer_id):
    if not is_admin(request):
        return HttpResponseRedirect('/') 
    employer = get_object_or_404(Employer, pk=employer_id)
    employer.userID.delete()
    return redirect('/csaadmin/list_employers/')

def delete_candidate(request, candidate_id):
    if not is_admin(request):
        return HttpResponseRedirect('/') 
    candidate = get_object_or_404(Candidate, pk=candidate_id)
    candidate.user.delete()
    return redirect('/csaadmin/list_candidates/')

def candidate_profile(request, pk):
    if not is_admin(request):
        return HttpResponseRedirect('/')
    candidate = get_object_or_404(Candidate, pk=pk)
    return render(request, 'csaadmin/candidate_profile.html', {'candidate': candidate})

def employer_profile(request, pk):
    if not is_admin(request):
        return HttpResponseRedirect('/')
    employer = get_object_or_404(Employer, pk=pk)
    return render(request, 'csaadmin/employer_profile.html', {'employer': employer})

def download(request, pk):
    # get candidate  from session
    if not is_admin(request):
        return HttpResponseRedirect('/')
    c = get_object_or_404(Candidate, pk=pk)
    obj = c.resume
    filename = obj.file.path
    response = FileResponse(open(filename, 'rb'))
    return response

def view_resume(request, pk):
    # get candidate  from session
    if not is_admin(request):
        return HttpResponseRedirect('/')
    candidate = get_object_or_404(Candidate, pk=pk)
    return render(request, 'csaadmin/view_resume.html', {'candidate': candidate})

def view_employer_jobs(request, pk):
    if not is_admin(request):
        return HttpResponseRedirect('/') 
    employer = get_object_or_404(Employer, pk=pk)
    jobs = Job.objects.filter(employer=employer)
    return render(request, 'csaadmin/list_jobs.html', {'jobs': jobs})

def view_job(request, pk):
    if not is_admin(request):
        return HttpResponseRedirect('/') 
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'csaadmin/view_job.html', {'job': job})

def reset_password(request, role, pk):
    # Assuming you have a method to check if the logged-in user is an admin
    if not is_admin(request):
        return redirect('/')

    if role=='c':
        user = get_object_or_404(Candidate, id=pk).user
    else:
        user = get_object_or_404(Employer, id=pk).userID

    if request.method == 'POST':
        if not is_admin(request):
            return redirect('/')
        user.password = request.POST.get('password')
        user.save()
        messages.success(request, 'Password reset successfully.')
        if role=='c':
            return redirect(f'/csaadmin/candidate_profile/{pk}')  # Replace '/admin/users/' with the appropriate URL to list all users
        else:
            return redirect(f'/csaadmin/employer_profile/{pk}') 
    return render(request, 'csaadmin/reset_password.html', {'user': user})

def change_email(request, role, pk):
    # Assuming you have a method to check if the logged-in user is an admin
    if not is_admin(request):
        return redirect('/')

    if role=='c':
        user = get_object_or_404(Candidate, id=pk).user
    else:
        user = get_object_or_404(Employer, id=pk).userID

    if request.method == 'POST':
        if not is_admin(request):
            return redirect('/')
        new_email = request.POST.get('email')
        user.email = new_email
        user.save()
        messages.success(request, 'Email changed successfully.')
        if role=='c':
            return redirect(f'/csaadmin/candidate_profile/{pk}')  # Replace '/admin/users/' with the appropriate URL to list all users
        else:
            return redirect(f'/csaadmin/employer_profile/{pk}') 
        
    return render(request, 'csaadmin/change_email.html', {'user': user})