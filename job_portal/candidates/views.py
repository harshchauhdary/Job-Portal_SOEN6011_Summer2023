from django.http import FileResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Candidate, Job, Resume
from django.views import generic
from django.shortcuts import get_object_or_404
from .forms import CandidateProfileForm, ResumeForm


# view profile
def view_Profile(request):
    # get candidate id from session
    cpk = 1
    candidate = get_object_or_404(Candidate, pk=cpk)
    return render(request, 'candidateDetailTemplate.html', context={'candidate': candidate})


# View and Save profile data
def create_Profile(request):

    if request.method == 'POST':

        form = CandidateProfileForm(request.POST)

        if form.is_valid():
            # save profile data
            form.save()

            # redirect to a new URL:
            return HttpResponseRedirect('/candidates/profile/')

    else:

        form = CandidateProfileForm()

    context = {
        'form': form,
    }

    return render(request, 'profileFormTemplate.html', context)


# Update profile
def update_profile(request):
    # get candidate id from session
    cpk = 1
    candidate = get_object_or_404(Candidate, pk=cpk)

    if request.method == 'POST':

        form = CandidateProfileForm(request.POST)

        if form.is_valid():
            # save profile data
            candidate.firstname = form.cleaned_data['firstname']
            candidate.lastname = form.cleaned_data['lastname']
            candidate.save()

            # redirect to a new URL:
            return HttpResponseRedirect('/candidates/profile/')

    else:

        form = CandidateProfileForm(
            initial={'firstname': candidate.firstname, 'lastname': candidate.lastname})

    context = {
        'form': form,
        'candidate': candidate,

    }

    return render(request, 'updateProfileTemplate.html', context)


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

    template_name = 'ViewJobTemplate.html'


# Apply Job Offers
def apply_Job(request, jpK):
    # get candidate id from session
    cpk = 1
    candidate = get_object_or_404(Candidate, pk=cpk)
    job = get_object_or_404(Job, pk=jpK)

    # add candidate to job's applied candidates list

    job.save()

    # add job to candidate's applies job

    candidate.save()

    context = {
        'candidate': candidate,
        'job': job
    }

    return render(request, "appliedSuccessTemplate.html", context)


# view Resume
def view_Resume(request):
    # get candidate id from session
    cpk = 1
    candidate = get_object_or_404(Candidate, pk=cpk)
    # get resume id from candidate
    rpk = 2
    resume = get_object_or_404(Resume, pk=rpk)
    return render(request, 'resumeDetailTemplate.html', context={'resume': resume})

# download Resume


def download(request):

    # get candidate id from session
    cpk = 1
    candidate = get_object_or_404(Candidate, pk=cpk)
    # get resume id from candidate
    rpk = 2
    obj = Resume.objects.get(id=rpk)
    filename = obj.file.path
    response = FileResponse(open(filename, 'rb'))
    return response

# Resume Builder Form


def create_Resume(request):

    # get candidate id from session
    cpk = 1

    if request.method == 'POST':

        form = ResumeForm(request.POST, request.FILES)

        if form.is_valid():
            # save profile data
            form.save()
            candidate = get_object_or_404(Candidate, pk=cpk)
            # add resume to candidate

            candidate.save()

            # redirect to a new URL:
            return HttpResponseRedirect('/candidates/resume/')

    else:

        form = ResumeForm()

    context = {
        'form': form,
    }

    return render(request, 'resumeFormTemplate.html', context)


# File resume upload
def upload_Resume(request):

    # get candidate id from session
    cpk = 1

    if request.method == 'POST':

        form = ResumeForm(request.POST, request.FILES)

        if form.is_valid():
            candidate = get_object_or_404(Candidate, pk=cpk)
            if candidate.resume != None:
                # get resume id from candidate
                rpk = 2
                resume = get_object_or_404(Resume, pk=rpk)
                resume.delete()
            # save profile data
            form.save()
            # add resume to candidate
            candidate.save()

            # redirect to a new URL:
            return HttpResponseRedirect('/candidates/resume/')

    else:

        form = ResumeForm()

    context = {
        'form': form,
    }

    return render(request, 'resumeFileFormTemplate.html', context)


# Update Resume form


def update_Resume(request):

    # get candidate id from session
    cpk = 1
    candidate = get_object_or_404(Candidate, pk=cpk)
    # get resume id from candidate
    rpk = 2

    resume = get_object_or_404(Resume, pk=rpk)

    if request.method == 'POST':

        form = ResumeForm(request.POST)

        if form.is_valid():
            # save resume data
            resume.graduation_Year = form.cleaned_data['graduation_Year']
            resume.save()

            # redirect to a new URL:
            return HttpResponseRedirect('/candidates/resume/')

    else:

        form = ResumeForm(
            initial={'graduation_Year': resume.graduation_Year})

    context = {
        'form': form,
        'resume': resume,

    }

    return render(request, 'updateResumeTemplate.html', context)
