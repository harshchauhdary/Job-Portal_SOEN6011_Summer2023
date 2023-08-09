from django.http import FileResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from .models import User, Job, Candidate, Application, Notification
from django.views import generic
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .forms import ResumeForm, CandidateForm, EducationFormSet, ExperienceFormSet, SkillFormSet, ProjectFormSet
from django.template.loader import get_template
from xhtml2pdf import pisa

# view notifications
def view_notifications(request):
    c = checkLogin(request)

    notifications = Notification.objects.filter(
        candidate=c, read=False).order_by('-id')

    context = {'notifications': notifications}

    return render(request, 'candidates/notifications.html', context)


def closeNotification(request, nId):
    c = checkLogin(request)

    notification = Notification(id=nId)
    notification.read = True
    notification.save()

    return HttpResponseRedirect('/candidates/notifications')

# view jobs


def view_Jobs(request):
   # get candidate from session
    c = checkLogin(request)
    print(c.savedJobs.all)
    j = []
    a = []
    jobs = Job.objects.all()
    for job in jobs:
        if Application.objects.filter(candidate=c).filter(job=job).count() == 0:
            if job.status == "OPEN":
                if c.savedJobs.contains(job):
                    continue
                else:
                    j.append(job)
        else:
            a.append(Application.objects.filter(
                candidate=c).filter(job=job)[0])

    context = {
        'jobs': j,
        'applied': a,
        'candidate': c
    }
    return render(request, 'candidates/viewJobsTemplate.html', context)


# Apply Job Offers
def apply_Job(request, pk):
    # get candidate from session
    c = checkLogin(request)
    try:
        job = Job.objects.filter(id=pk)[0]
    except Exception:
        return HttpResponseRedirect(reverse('view job', args=[pk]))
    if Application.objects.filter(candidate=c).filter(job=job).count() == 0:
        a = Application(candidate=c, job=job, status="Applied")
        if c.savedJobs.contains(job):
            c.savedJobs.remove(job)
            c.save()
        a.save()
    else:
        return HttpResponseRedirect(reverse('view job', args=[pk]))
    context = {
        'candidate': c,
        'job': job
    }

    return render(request, "candidates/appliedSuccessTemplate.html", context)

# View Job Offer


def view_Job(request, pk):
    # get candidate from session
    c = checkLogin(request)
    try:
        job = Job.objects.filter(id=pk)[0]
    except Exception:
        return HttpResponseRedirect('/candidates/')
    
    # check if the candidate has already applied for the job
    has_applied = Application.objects.filter(candidate=c, job=job).exists()

    context = {
        'candidate': c,
        'job': job,
        'has_applied': has_applied,
    }
    return render(request, "candidates/viewJobTemplate.html", context)


# view Resume  DONE!
def view_Resume(request):
    # get candidate from session
    c = checkLogin(request)
    if c.resume is not None:
        return render(request, 'candidates/resumeDetailTemplate.html', context={'candidate': c})
    else:
        return HttpResponseRedirect('/candidates/createResume')

# download Resume DONE!

def export_resume_pdf_view(request, *args, **kwargs):
    template_path = 'candidates/exportResume.html'  # change to your new template path
    context = {'candidate': checkLogin(request)}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="resume.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
       html, dest=response, encoding='UTF-8')

    if pisa_status.err:
       return HttpResponse('We had some errors with generating your PDF <pre>' + html + '</pre>')
    return response



def download(request):

    # get candidate  from session
    c = checkLogin(request)
    obj = c.resume
    filename = obj.file.path
    response = FileResponse(open(filename, 'rb'))
    return response

# Resume Builder Form


def create_Resume(request):
    # get candidate from session
    c = checkLogin(request)
    if c.resume is not None:
        return HttpResponseRedirect('/candidates/resume')

    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        education_formset = EducationFormSet(request.POST, prefix='education')
        experience_formset = ExperienceFormSet(
            request.POST, prefix='experience')
        skill_formset = SkillFormSet(request.POST, prefix='skill')
        project_formset = ProjectFormSet(request.POST, prefix='project')

        if form.is_valid() and education_formset.is_valid() and experience_formset.is_valid() and skill_formset.is_valid() and project_formset.is_valid():
            # Save resume data
            resume = form.save()

            # Update candidate's resume
            c.resume = resume
            c.save()

            # Save education, experience, and skill formsets
            education_formset.instance = resume
            education_formset.save()

            experience_formset.instance = resume
            experience_formset.save()

            skill_formset.instance = resume
            skill_formset.save()

            project_formset.instance = resume
            project_formset.save()

            # redirect to a new URL:
            return HttpResponseRedirect('/candidates/resume')

    else:
        form = ResumeForm()
        education_formset = EducationFormSet(prefix='education')
        experience_formset = ExperienceFormSet(prefix='experience')
        skill_formset = SkillFormSet(prefix='skill')
        project_formset = ProjectFormSet(prefix='project')

    context = {
        'form': form,
        'education_formset': education_formset,
        'experience_formset': experience_formset,
        'skill_formset': skill_formset,
        'project_formset': project_formset,
    }

    return render(request, 'candidates/resumeFormTemplate.html', context)


# Update Resume form


def update_Resume(request):

    # get candidate  from session
    c = checkLogin(request)
    if c.resume is None:
        return HttpResponseRedirect('/candidates/createResume')

    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES, instance=c.resume)
        education_formset = EducationFormSet(
            request.POST, instance=c.resume, prefix='education')
        experience_formset = ExperienceFormSet(
            request.POST, instance=c.resume, prefix='experience')
        skill_formset = SkillFormSet(
            request.POST, instance=c.resume, prefix='skill')
        project_formset = ProjectFormSet(
            request.POST, instance=c.resume, prefix='project')

        if form.is_valid() and education_formset.is_valid() and experience_formset.is_valid() and skill_formset.is_valid() and project_formset.is_valid():
            form.save()
            education_formset.save()
            experience_formset.save()
            skill_formset.save()
            project_formset.save()
            # Redirect to a new URL:
            return HttpResponseRedirect('/candidates/resume')

    else:
        form = ResumeForm(instance=c.resume)
        education_formset = EducationFormSet(
            instance=c.resume, prefix='education')
        experience_formset = ExperienceFormSet(
            instance=c.resume, prefix='experience')
        skill_formset = SkillFormSet(instance=c.resume, prefix='skill')
        project_formset = ProjectFormSet(instance=c.resume, prefix='project')

    context = {
        'form': form,
        'education_formset': education_formset,
        'experience_formset': experience_formset,
        'skill_formset': skill_formset,
        'project_formset': project_formset,
    }

    return render(request, 'candidates/updateResumeTemplate.html', context)


# Candidate Profile CRUD

# View and Save profile data
def create_Candidate_Profile(request):

    # get user from session
    if 'user_id' in request.session:
        id = request.session['user_id']
        try:
            u = User.objects.filter(id=id)[0]
        except Exception:
            return HttpResponseRedirect('/users/register')

    else:
        return HttpResponseRedirect('')

    if request.method == 'POST':

        form = CandidateForm(request.POST)

        if form.is_valid():
            # save profile data
            ca = form.save(commit=False)
            ca.user = u
            ca.save()
            request.session["c_id"] = ca.id
            del request.session["user_id"]
            # redirect to a new URL:
            return HttpResponseRedirect('/candidates/profile')

    else:

        form = CandidateForm()

    context = {
        'form': form,
    }

    return render(request, 'candidates/profileFormTemplate.html', context)


# Update profile
def update_candidate_profile(request):
    # get candidate  from session
    c = checkLogin(request)

    if request.method == 'POST':

        form = CandidateForm(request.POST)

        if form.is_valid():
            # save profile data
            c.firstName = form.cleaned_data['firstName']
            c.lastName = form.cleaned_data['lastName']
            c.phone = form.cleaned_data['phone']
            c.save()

            # redirect to a new URL:
            return HttpResponseRedirect('/candidates/profile')

    else:

        form = CandidateForm(
            initial={'firstName': c.firstName, 'lastName': c.lastName, 'phone': c.phone})

    context = {
        'form': form,
        'candidate': c,

    }

    return render(request, 'candidates/updateProfileTemplate.html', context)


# view profile
def view_candidate_profile(request):
    # get candidate  from session
    c = checkLogin(request)

    return render(request, 'candidates/profileTemplate.html', context={'candidate': c})


# check login for every request
def checkLogin(request):

    if 'c_id' in request.session:
        id = request.session['c_id']
        try:
            c = Candidate.objects.filter(id=id)[0]
            return c
        except Exception:
            return HttpResponseRedirect('')

    else:
        return HttpResponseRedirect('')

# Add jobs to saved list


def addToFavoriteJobs(request, jobId):
    # get candidate  from session
    c = checkLogin(request)
    job = Job.objects.filter(id=jobId)[0]
    if Application.objects.filter(candidate=c).filter(job=job).count() == 0:
        c.savedJobs.add(Job.objects.filter(id=jobId)[0])
        c.save()

    return HttpResponseRedirect("/candidates")


# remove jobs from list

def removeFromFavoriteJobs(request, jobId):
    # get candidate  from session
    c = checkLogin(request)

    c.savedJobs.remove(Job.objects.filter(id=jobId)[0])
    c.save()

    return HttpResponseRedirect("/candidates#saved")




