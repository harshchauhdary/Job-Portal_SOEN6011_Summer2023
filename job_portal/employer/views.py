# from django.shortcuts import render, redirect
# from django.http import FileResponse, HttpResponseForbidden, HttpResponseRedirect
# from django.shortcuts import get_object_or_404
# from .models import User, Job, Resume
# from .forms import JobForm

# # def browse_candidates(request):
# #     students = User.objects.filter(role='student')
# #     context = {
# #         'candidates': students
# #     }
# #     return render(request, 'employer/browse_candidates.html', context)

# def browse_candidates(request):
#     if 'user_id' in request.session:
#         cpk = request.session['user_id']
#         user = get_object_or_404(User, pk=cpk)
#         if user.role != 'employer':
#             return redirect('/users')
#     else:
#         return redirect('/users')

#     students = User.objects.filter(role='student')
#     context = {
#         'candidates': students
#     }
#     return render(request, 'employer/browse_candidates.html', context)


# # def add_job(request):
# #     if request.method == 'POST':
# #         form = JobForm(request.POST)
# #         if form.is_valid():
# #             job = form.save()
# #             return HttpResponseRedirect(f'/employer/viewJob/{job.id}/')
# #     else:
# #         form = JobForm()
# #     context = {
# #         'form': form,
# #     }
# #     return render(request, 'employer/add_job.html', context)

# def add_job(request):
#     if 'user_id' in request.session:
#         cpk = request.session['user_id']
#         user = get_object_or_404(User, pk=cpk)
#         if user.role != 'employer':
#             return redirect('/users')
#     else:
#         return redirect('/users')

#     if request.method == 'POST':
#         form = JobForm(request.POST)
#         if form.is_valid():
#             job = form.save()
#             return HttpResponseRedirect(f'/employer/viewJob/{job.id}/')
#     else:
#         form = JobForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'employer/add_job.html', context)

# # def view_job(request, job_id):
# #     job = get_object_or_404(Job, pk=job_id)
# #     return render(request, 'employer/view_job.html', context={'job': job})

# def view_job(request, job_id):
#     if 'user_id' in request.session:
#         cpk = request.session['user_id']
#         user = get_object_or_404(User, pk=cpk)
#         if user.role != 'employer':
#             return redirect('/users')
#     else:
#         return redirect('/users')

#     job = get_object_or_404(Job, pk=job_id)
#     return render(request, 'employer/view_job.html', context={'job': job})


# # def update_job(request, job_id):
# #     job = get_object_or_404(Job, pk=job_id)

# #     if request.method == 'POST':
# #         form = JobForm(request.POST, instance=job)
# #         if form.is_valid():
# #             form.save()
# #             return HttpResponseRedirect(f'/employer/viewJob/{job.id}/')
# #     else:
# #         form = JobForm(instance=job)

# #     context = {
# #         'form': form,
# #         'job': job,
# #     }
# #     return render(request, 'employer/update_job.html', context)

# def update_job(request, job_id):
#     if 'user_id' in request.session:
#         cpk = request.session['user_id']
#         user = get_object_or_404(User, pk=cpk)
#         if user.role != 'employer':
#             return redirect('/users')
#     else:
#         return redirect('/users')

#     job = get_object_or_404(Job, pk=job_id)

#     if request.method == 'POST':
#         form = JobForm(request.POST, instance=job)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(f'/employer/viewJob/{job.id}/')
#     else:
#         form = JobForm(instance=job)

#     context = {
#         'form': form,
#         'job': job,
#     }
#     return render(request, 'employer/update_job.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, HttpResponseRedirect
from .models import User, Job, Employer
from candidate.models import Application
from .forms import JobForm, EmployerForm

# Check login for every request
def check_login(request):
    if 'e_id' in request.session:
        e_id = request.session['e_id']
        try:
            employer = Employer.objects.get(pk=e_id)
            return employer
        # except Exception:
        #     return HttpResponseRedirect('/users/login')
        except Employer.DoesNotExist:
            pass

    # else:
    #     return HttpResponseRedirect('/users/login')
    return None
    
def browse_candidates(request, job_id):
    employer = check_login(request)
    try:
        job = Job.objects.get(pk=job_id)
    except Job.DoesNotExist:
        return HttpResponseRedirect('/users')

    applications = Application.objects.filter(job=job)
    candidates = [application.candidate for application in applications]

    context = {
        'job': job,
        'candidates': candidates
        }
    return render(request, 'employer/browse_candidates.html', context)


# Add a job
def add_job(request):
    # employer = check_login(request)

    # if request.method == 'POST':
    #     form = JobForm(request.POST)
    #     if form.is_valid():
    #         job = form.save(commit=False)
    #         job.employer = employer
    #         job.save()
    #         return HttpResponseRedirect(f'/employer/viewJob/{job.id}/')
    # else:
    #     form = JobForm()

    # context = {
    #     'form': form,
    # }
    # return render(request, 'employer/add_job.html', context)
    employer = check_login(request)

    if employer is None:
        return HttpResponseRedirect('/users/login')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = employer
            job.save()
            return HttpResponseRedirect(f'/employer/viewJob/{job.id}/')
    else:
        form = JobForm()

    context = {
        'form': form,
    }
    return render(request, 'employer/add_job.html', context)

# View job details
def view_job(request, job_id):
    employer = check_login(request)
    if employer is None:
        return HttpResponseRedirect('/users/login')
    try:
        job = Job.objects.get(pk=job_id, employer=employer)
    except Job.DoesNotExist:
        return HttpResponseRedirect('/users')

    context = {
        'job': job,
    }
    return render(request, 'employer/view_job.html', context)

def update_job(request, job_id):
    employer = check_login(request)
    if employer is None:
        return HttpResponseRedirect('/users/login')
    try:
        job = Job.objects.get(pk=job_id, employer=employer)
    except Job.DoesNotExist:
        return HttpResponseRedirect('/users')

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f'/employer/viewJob/{job.id}/')
    else:
        form = JobForm(instance=job)

    context = {
        'form': form,
        'job': job,
    }
    return render(request, 'employer/update_job.html', context)


# Employer Profile CRUD

# View and Save profile data
def create_employer_profile(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return HttpResponseRedirect('/users/register')
    else:
        return HttpResponseRedirect('/users/login')

    if request.method == 'POST':
        form = EmployerForm(request.POST)
        if form.is_valid():
            employer = form.save(commit=False)
            # employer.user = user
            # employer.save()
            # request.session["e_id"] = employer.id
            # del request.session["user_id"]
            # return HttpResponseRedirect('/employer/profile')
            if user is not None:
                employer.userID = user
                employer.save()
                request.session["e_id"] = employer.id
                del request.session["user_id"]
                return HttpResponseRedirect('/employer/profile')
    else:
        form = EmployerForm()

    context = {
        'form': form,
    }

    return render(request, 'employer/profileFormTemplate.html', context)


# Update profile
def update_employer_profile(request):
    employer = check_login(request)
    if employer is None:
        return HttpResponseRedirect('/users/login')

    if request.method == 'POST':
        form = EmployerForm(request.POST, instance=employer)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/employer/profile')
    else:
        form = EmployerForm(instance=employer)

    context = {
        'form': form,
        'employer': employer,
    }

    return render(request, 'employer/updateProfileTemplate.html', context)


# View profile
def view_employer_profile(request):
    employer = check_login(request)
    if employer is None:
        return HttpResponseRedirect('/users/login')

    return render(request, 'employer/profileTemplate.html', context={'employer': employer})

# View all jobs
def view_jobs(request):
    employer = check_login(request)
    if employer is None:
        return HttpResponseRedirect('/users/login')
    jobs = Job.objects.filter(employer=employer)

    context = {
        'jobs': jobs
    }
    return render(request, 'employer/view_jobs.html', context)