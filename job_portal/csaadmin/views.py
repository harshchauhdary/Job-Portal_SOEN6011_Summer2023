from django.shortcuts import render, get_object_or_404, redirect
from .models import User, Employer, Candidate, Job
from django.http import HttpResponseRedirect

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
    return redirect('/csaadmin/list_jobs')

def delete_employer(request, employer_id):
    if not is_admin(request):
        return HttpResponseRedirect('/') 
    employer = get_object_or_404(Employer, pk=employer_id)
    employer.delete()
    return redirect('/csaadmin/list_employers')

def delete_candidate(request, candidate_id):
    if not is_admin(request):
        return HttpResponseRedirect('/') 
    candidate = get_object_or_404(Candidate, pk=candidate_id)
    candidate.delete()
    return redirect('/csaadmin/list_candidates')

