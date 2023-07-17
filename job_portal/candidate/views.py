from django.http import FileResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from .models import User, Job, Resume
from django.views import generic
from django.shortcuts import get_object_or_404
from .forms import ResumeForm


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
    # get candidate id from session
    if 'user_id' in request.session:
        cpk = request.session['user_id']
    else:
        return render(request, 'users/login.html')

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


# view Resume
def view_Resume(request):
    # get candidate id from session
    if 'user_id' in request.session:
        cpk = request.session['user_id']
    else:
        return render(request, 'users/login.html')

    user = get_object_or_404(User, pk=cpk)
    # get resume id from candidate
    rpk = 4
    resume = get_object_or_404(Resume, pk=rpk)
    return render(request, 'candidates/resumeDetailTemplate.html', context={'resume': resume})

# download Resume


def download(request):

    # get candidate id from session
    if 'user_id' in request.session:
        cpk = request.session['user_id']
    else:
        return render(request, 'users/login.html')

    user = get_object_or_404(User, pk=cpk)
    # get resume id from candidate
    rpk = 2
    obj = Resume.objects.get(id=rpk)
    filename = obj.file.path
    response = FileResponse(open(filename, 'rb'))
    return response

# Resume Builder Form


def create_Resume(request):

    # get candidate id from session
    if 'user_id' in request.session:
        cpk = request.session['user_id']
    else:
        return render(request, 'users/login.html')

    if request.method == 'POST':

        form = ResumeForm(request.POST, request.FILES)

        if form.is_valid():
            # save profile data
            form.save()
            user = get_object_or_404(User, pk=cpk)
            # add resume to candidate

            user.save()

            # redirect to a new URL:
            return HttpResponseRedirect('/candidates/resume')

    else:

        form = ResumeForm()

    context = {
        'form': form,
    }

    return render(request, 'candidates/resumeFormTemplate.html', context)


# File resume upload
# def upload_Resume(request):

#     # get candidate id from session
#     if 'user_id' in request.session:
#         cpk = request.session['user_id']
#     else:
#         return render(request, 'users/login.html')

#     if request.method == 'POST':

#         form = ResumeForm(request.POST, request.FILES)

#         if form.is_valid():
#             user = get_object_or_404(User, pk=cpk)
#             if user.resume != None:
#                 # get resume id from candidate
#                 rpk = 2
#                 resume = get_object_or_404(Resume, pk=rpk)
#                 resume.delete()
#             # save profile data
#             form.save()
#             # add resume to candidate
#             user.save()

#             # redirect to a new URL:
#             return HttpResponseRedirect('/candidates/resume/')

#     else:

#         form = ResumeForm()

#     context = {
#         'form': form,
#     }

#     return render(request, 'candidates/resumeFileFormTemplate.html', context)


# Update Resume form


def update_Resume(request):

    # get candidate id from session
    if 'user_id' in request.session:
        cpk = request.session['user_id']
    else:
        return render(request, 'users/login.html')

    user = get_object_or_404(User, pk=cpk)
    # get resume id from candidate
    rpk = 3

    resume = get_object_or_404(Resume, pk=rpk)

    if request.method == 'POST':

        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():        
            resume.delete()
            # save profile data
            form.save()
            # add resume to candidate
            user.save()

#             # redirect to a new URL:
            return HttpResponseRedirect('/candidates/resume')

        # if form.is_valid():
        #     # save resume data
        #     resume.graduation_Year = form.cleaned_data['graduation_Year']
        #     resume.save()

        #     # redirect to a new URL:
        #     return HttpResponseRedirect('/candidates/resume/')

    else:

        form = ResumeForm(
            initial={'graduation_Year': resume.graduation_Year, 'file': resume.file})

    context = {
        'form': form,
        'resume': resume,

    }

    return render(request, 'candidates/updateResumeTemplate.html', context)
