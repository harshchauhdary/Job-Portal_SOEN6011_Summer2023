from django.http import FileResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from .models import User, Job, Candidate
from django.views import generic
from django.shortcuts import get_object_or_404
from .forms import ResumeForm, CandidateForm


# View Job Offers
class Job_List_View(generic.ListView):
    model = Job
    context_object_name = 'job_Instances'

    def get_queryset(self):
        # Can add filter for status open
        return Job.objects.all

    def get_context_data(self, **kwargs):
        context = super(Job_List_View, self).get_context_data(**kwargs)
        return context

    template_name = 'candidates/ViewJobTemplate.html'


# Apply Job Offers
def apply_Job(request, jpK):
    cpk = checkLogin(request)

    user = get_object_or_404(User, pk=cpk)
    job = get_object_or_404(Job, pk=jpK)

    # add candidate to job's applied candidates list

    job.save()

    # add job to candidate's applies job

    user.save()

    context = {
        'user': user,
        'job': job
    }

    return render(request, "candidates/appliedSuccessTemplate.html", context)


# view Resume  DONE!
def view_Resume(request):
    # get candidate from session
    c = checkLogin(request)
    if c.resume is not None:
        return render(request, 'candidates/resumeDetailTemplate.html', context={'resume': c.resume})
    else:
        return HttpResponseRedirect('/candidates/createResume')

# download Resume DONE!


def download(request):

    # get candidate  from session
    c = checkLogin(request)
    obj = c[0].resume
    filename = obj.file.path
    response = FileResponse(open(filename, 'rb'))
    return response

# Resume Builder Form


def create_Resume(request):

    # get candidate  from session
    c = checkLogin(request)
    if c.resume is not None:
        return HttpResponseRedirect('/candidates/resume')

    if request.method == 'POST':

        form = ResumeForm(request.POST, request.FILES)

        if form.is_valid():
            # save profile data
            # Save the form data but don't commit yet
            r = form.save(commit=False)
            r.save()
            c.resume = r
            c.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/candidates/resume')

    else:

        form = ResumeForm()

    context = {
        'form': form,
    }

    return render(request, 'candidates/resumeFormTemplate.html', context)


# Update Resume form


def update_Resume(request):

    # get candidate  from session
    c = checkLogin(request)
    if c.resume is None:
        return HttpResponseRedirect('/candidates/createResume')

    if request.method == 'POST':

        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            c.resume.summary = form.cleaned_data['summary']
            c.resume.file = form.cleaned_data['file']
            c.resume.education = form.cleaned_data['education']
            c.resume.experience = form.cleaned_data['experience']
            c.resume.fileName = form.cleaned_data['fileName']
            c.resume.skills = form.cleaned_data['skills']
            c.resume.save()

            # redirect to a new URL:
            return HttpResponseRedirect('/candidates/resume')

    else:

        form = ResumeForm(
            initial={'summary': c.resume.summary, 'education': c.resume.education, 'experience': c.resume.experience,
                     'fileName': c.resume.fileName, 'skills': c.resume.skills, 'file': c.resume.file})

    context = {
        'form': form,
        'resume': c.resume,

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
        return HttpResponseRedirect('/users/login')

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
            return HttpResponseRedirect('/users/login')

    else:
        return HttpResponseRedirect('/users/login')
