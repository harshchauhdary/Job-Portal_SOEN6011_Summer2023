from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from .models import User, Job, Employer
from candidate.models import Application, Notification
from .forms import JobForm, EmployerForm
from candidate.models import Candidate
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import get_template
from xhtml2pdf import pisa


def view_candidate_application(request, applicationId):
    employer = check_login(request)
    if not employer:
        return HttpResponseRedirect('/')

    application = get_object_or_404(Application, pk=applicationId)
    if application.job.employer != employer:
        return HttpResponseForbidden("You do not have permission to perform this action.")

    candidate = Candidate.objects.filter(id=application.candidate.id)[0]
    print(candidate)
    application.status = "Viewed"
    application.save()
    context = {
        'candidate': candidate,
        'application': application,
    }

    message = "Someone viewed your profile for the job: "+application.job.get_job_position()+" at "+application.job.get_company_name()
    notification = Notification(candidate=application.candidate, message=message, read=False)
    notification.save()
    
    return render(request, 'employer/view_candidate_application.html', context)

def export_resume_pdf_view(request, candidate_id):
    employer = check_login(request)
    if not employer:
        return HttpResponseRedirect('/')
    print("---------------------------")
    candidate = Candidate.objects.filter(pk=candidate_id)[0]
    template_path = 'candidates/exportResume.html'  # change to your new template path
    context = {'candidate': candidate}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="resume.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
       html, dest=response, encoding='UTF-8')

    if pisa_status.err:
       return HttpResponse('We had some errors with generating your PDF <pre>' + html + '</pre>')
    return response

def accept_application(request, application_id):
    employer = check_login(request)
    if not employer:
        return HttpResponseRedirect('/')

    application = get_object_or_404(Application, pk=application_id)
    if application.job.employer != employer:
        return HttpResponseForbidden("You do not have permission to perform this action.")

    application.status = "Accepted"
    application.save()

    message = "Congratulations you are accepted for the job: "+application.job.get_job_position()+" at "+application.job.get_company_name()
    notification = Notification(candidate=application.candidate, message=message, read=False)
    notification.save()

    return HttpResponseRedirect(f'/employer/browseCandidates/{application.job.pk}')


def reject_application(request, application_id):
    employer = check_login(request)
    if not employer:
        return HttpResponseRedirect('/users/login')

    application = get_object_or_404(Application, pk=application_id)
    if application.job.employer != employer:
        return HttpResponseForbidden("You do not have permission to perform this action.")

    application.status = "Rejected"
    application.save()

    message = "Try next time for the job: "+application.job.get_job_position()+" at "+application.job.get_company_name()
    notification = Notification(candidate=application.candidate, message=message, read=False)
    notification.save()

    return HttpResponseRedirect(f'/employer/browseCandidates/{application.job.pk}')


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
            return None

    # else:
    #     return HttpResponseRedirect('/users/login')
    return None


def browse_candidates(request, job_id):
    employer = check_login(request)
    try:
        job = Job.objects.get(pk=job_id)
    except Job.DoesNotExist:
        return HttpResponseRedirect('/employer/viewJobs')

    applications = Application.objects.filter(job=job)
    candidates = [application.candidate for application in applications]

    context = {
        'job': job,
        'applications': applications
    }
    return render(request, 'employer/browse_candidates.html', context)


def browse_candidates_all(request):
    employer = check_login(request)

    # if employer is None:
    # return HttpResponseRedirect('/')

    candidates = Candidate.objects.all()

    context = {
        'candidates': candidates
    }
    return render(request, 'employer/browse_candidates_all.html', context)


# Add a job
def add_job(request):
    employer = check_login(request)

    if employer is None:
        return HttpResponseRedirect('/')

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
        return HttpResponseRedirect('/')
    try:
        job = Job.objects.get(pk=job_id, employer=employer)
    except Job.DoesNotExist:
        return HttpResponseRedirect('/employer/viewJobs')

    context = {
        'job': job,
    }
    return render(request, 'employer/view_job.html', context)


def update_job(request, job_id):
    employer = check_login(request)
    if employer is None:
        return HttpResponseRedirect('/')
    try:
        job = Job.objects.get(pk=job_id, employer=employer)
    except Job.DoesNotExist:
        return HttpResponseRedirect('/employer/viewJobs')

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
            return HttpResponseRedirect('/register')
    else:
        return HttpResponseRedirect('/')

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
        return HttpResponseRedirect('/')

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


def view_employee_profile(request):
    employer = check_login(request)

    if employer is None:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        button_id = request.POST.get('button_id')

        try:
            entry = Candidate.objects.get(id=button_id)
        except Candidate.DoesNotExist:
            entry = None

        print(entry.firstName)

    return render(request, 'employer/view_profile.html', context={'candidate': entry})

# View profile


def view_employer_profile(request):
    employer = check_login(request)
    if employer is None:
        return HttpResponseRedirect('/')

    return render(request, 'employer/profileTemplate.html', context={'employer': employer})


def download_employee_resume(request):
    employer = check_login(request)

    if employer is None:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        candidate_id = request.POST.get('resume_id')

        try:
            entry = Candidate.objects.get(id=candidate_id)
            obj = entry.resume
            filename = obj.file.path
            response = FileResponse(open(filename, 'rb'))
        except Candidate.DoesNotExist:
            entry = None
            response = None

    return response


# View all jobs
def view_jobs(request):
    employer = check_login(request)
    if employer is None:
        return HttpResponseRedirect('/')
    jobs = Job.objects.filter(employer=employer)

    context = {
        'jobs': jobs
    }
    return render(request, 'employer/view_jobs.html', context)
